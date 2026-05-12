import os
import uuid
import time
from flask_socketio import emit
from app import db
from app.core.evaluator import Evaluator
from app.core.sensei import Sensei
from app.services.stt_handler import STTHandler
from app.services.tts_handler import TTSHandler
from app.models.vocabulary import Vocabulary

def register_socket_events(socketio):
    # Initialize handlers INSIDE the registration function
    # This ensures they are created within the app context
    stt = STTHandler()
    evaluator = Evaluator()
    sensei = Sensei() # Now it will see the API key!
    tts = TTSHandler()

    def handle_audio(data):
        start_time = time.time()
        
        audio_data = data.get('audio')
        raw_word_id = data.get('word_id')
        
        if not audio_data:
            emit('error', {'message': 'No audio data received.'})
            return

        filename = f"{uuid.uuid4()}.webm"
        temp_dir = os.path.join('app', 'static', 'audio_temp')
        
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        file_path = os.path.join(temp_dir, filename)
        
        try:
            with open(file_path, 'wb') as f:
                f.write(audio_data)
                f.flush()
                os.fsync(f.fileno()) 

            # 1. Transcribe
            transcription = stt.transcribe(file_path)

            # 2. Evaluation
            word_id = int(raw_word_id)
            word_obj = db.session.get(Vocabulary, word_id)

            if not word_obj:
                raise ValueError(f"Word ID {word_id} not found.")

            score = evaluator.get_score(transcription, word_obj.furigana)

            # 3. Brain (Gemini Feedback)
            response = sensei.format_response(score, word_obj, transcription)
            
            # 4. Multimodal Output (Base64 TTS)
            audio_data_uri = tts.generate_speech_base64(response['voice_text'])
            
            # 5. Construct Final Payload
            response.update({
                'user_transcription': transcription,
                'audio_url': audio_data_uri,
                'debug': {
                    'raw_stt': transcription,
                    'normalized_input': evaluator.normalize_text(transcription),
                    'target_phonetic': evaluator.normalize_text(word_obj.furigana),
                    'proc_time': f"{round(time.time() - start_time, 3)}s"
                }
            })

            # 6. Database Update
            word_obj.times_practiced += 1
            word_obj.last_score = score
            db.session.commit()

            emit('evaluation_result', response)

        except Exception as e:
            print(f">>> [SERVER ERROR] {str(e)}")
            emit('error', {'message': f"Sensei had trouble: {str(e)}"})
        
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    socketio.on_event('submit_audio', handle_audio)