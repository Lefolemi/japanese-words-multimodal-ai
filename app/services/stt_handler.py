import whisper
import os

class STTHandler:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path):
        if not os.path.exists(audio_path):
            return ""
        
        # We use a very short, non-instructional prompt.
        # This just sets the language/context without giving "orders" to repeat.
        result = self.model.transcribe(
            audio_path, 
            language="ja",
            initial_prompt="こんにちは、日本語の練習です。", 
            fp16=False # Set to False if you don't have a GPU to avoid extra noise
        )
        return result.get("text", "").strip()