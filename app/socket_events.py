import os
import uuid
from flask_socketio import emit
from app import db
from app.core.evaluator import Evaluator
from app.core.sensei import Sensei
from app.services.stt_handler import STTHandler
from app.models.vocabulary import Vocabulary

# Initialize handlers at module level
stt = STTHandler(model_name="base") 
evaluator = Evaluator()
sensei = Sensei()

def register_socket_events(socketio):
    """
    Registers socket events explicitly to avoid Pylance 'not accessed' warnings.
    """
    
    def handle_audio(data):
        print(">>> [RECEIVE] Audio packet received from client.")
        
        audio_data = data.get('audio')
        raw_word_id = data.get('word_id')
        
        if not audio_data:
            print(">>> [ERROR] No audio data found in the payload.")
            emit('error', {'message': 'No audio data received.'})
            return

        # 1. Prepare Path
        filename = f"{uuid.uuid4()}.webm"
        temp_dir = os.path.join('app', 'static', 'audio_temp')
        
        # Ensure directory exists
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        file_path = os.path.join(temp_dir, filename)
        
        try:
            # 2. Save binary data
            with open(file_path, 'wb') as f:
                f.write(audio_data)
            print(f">>> [DISK] Audio saved: {file_path}")

            # 3. Transcribe (This is usually where 'Evaluating' hangs)
            print(">>> [STT] Starting Whisper transcription...")
            transcription = stt.transcribe(file_path)
            print(f">>> [STT] Whisper heard: '{transcription}'")

            # 4. Evaluation
            word_id = int(raw_word_id)
            word_obj = db.session.get(Vocabulary, word_id)
            
            if not word_obj:
                raise ValueError(f"Word ID {word_id} not found in database.")

            score = evaluator.get_score(transcription, word_obj.furigana)
            response = sensei.format_response(score, word_obj)
            response['user_transcription'] = transcription

            # 5. Database Update
            word_obj.times_practiced += 1
            word_obj.last_score = score
            db.session.commit()

            # 6. Emit Result
            print(f">>> [EMIT] Result sent back. Score: {score}")
            emit('evaluation_result', response)

        except Exception as e:
            print(f">>> [SERVER ERROR] {str(e)}")
            emit('error', {'message': f"Sensei had trouble: {str(e)}"})
        
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(">>> [CLEANUP] Temp file removed.")

    # Explicitly register the handler to the event name
    # This removes the Pylance warning
    socketio.on_event('submit_audio', handle_audio)