class Sensei:
    def __init__(self, name="Sensei"):
        self.name = name

    def get_feedback(self, score):
        if score >= 0.95:
            return {
                "voice": "素晴らしい！", 
                "display": "素晴らしい！ (Subarashii!) Perfect pronunciation.",
                "status": "success"
            }
        elif score >= 0.80:
            return {
                "voice": "いいですね。", 
                "display": "いいですね (Ii desu ne). Very good, almost there.",
                "status": "good"
            }
        elif score >= 0.50:
            return {
                "voice": "頑張って！", 
                "display": "頑張って！ (Ganbatte!) You are close, try to speak clearer.",
                "status": "retry"
            }
        else:
            return {
                "voice": "もう一度お願いします。", 
                "display": "もう一度お願いします (Mou ichido onegaishimasu). Please try again.",
                "status": "fail"
            }

    def format_response(self, score, word_obj):
        feedback = self.get_feedback(score)
        return {
            "score": score,
            "original": word_obj.original,
            "furigana": word_obj.furigana,
            "english": word_obj.english,
            "message": feedback["display"], # For the UI
            "voice_text": feedback["voice"], # For the TTS
            "status": feedback["status"]
        }