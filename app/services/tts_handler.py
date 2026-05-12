import io
import base64
from gtts import gTTS

class TTSHandler:
    def generate_speech_base64(self, text, lang='ja'):
        try:
            # Save audio to a memory buffer instead of a file
            mp3_fp = io.BytesIO()
            tts = gTTS(text=text, lang=lang)
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            # Encode to base64 string
            b64_data = base64.b64encode(mp3_fp.read()).decode('utf-8')
            return f"data:audio/mp3;base64,{b64_data}"
        except Exception as e:
            print(f">>> [TTS ERROR] {e}")
            return None