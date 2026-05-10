import os
import time
import uuid
from gtts import gTTS

class TTSHandler:
    def __init__(self):
        self.output_dir = os.path.join('app', 'static', 'audio_responses')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def cleanup_old_files(self, max_age_seconds=30):
        """Deletes files in the output directory older than max_age_seconds."""
        now = time.time()
        for f in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, f)
            if os.path.isfile(file_path):
                if os.stat(file_path).st_mtime < (now - max_age_seconds):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Cleanup error: {e}")

    def generate_speech(self, text, lang='ja'):
        # Clean up before generating a new one
        self.cleanup_old_files()

        filename = f"tts_{uuid.uuid4()}.mp3"
        file_path = os.path.join(self.output_dir, filename)
        
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(file_path)
            return f"/static/audio_responses/{filename}"
        except Exception as e:
            print(f">>> [TTS ERROR] {e}")
            return None