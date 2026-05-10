import os
import json
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

class STTHandler:
    def __init__(self):
        # Locate vosk_weights relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "vosk_weights")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk weights not found at {model_path}")
        self.model = Model(model_path)

    def transcribe(self, audio_path):
        # 1. Convert WebM to WAV (PCM 16kHz Mono)
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        
        wav_path = audio_path.replace(".webm", ".wav")
        audio.export(wav_path, format="wav")

        # 2. Process with Vosk
        with open(wav_path, "rb") as f:
            rec = KaldiRecognizer(self.model, 16000)
            while True:
                data = f.read(4000)
                if len(data) == 0:
                    break
                rec.AcceptWaveform(data)
        
        # 3. Cleanup and Result
        result = json.loads(rec.FinalResult())
        if os.path.exists(wav_path):
            os.remove(wav_path)
            
        return result.get("text", "").replace(" ", "")