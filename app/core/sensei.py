class Sensei:
    def __init__(self, name="Sensei"):
        self.name = name

    def get_feedback(self, score):
        """
        Maps numerical scores to stylized Japanese feedback messages.
        """
        if score >= 0.95:
            return {
                "message": "素晴らしい！ (Subarashii!) Perfect pronunciation.",
                "status": "success",
                "color": "#28a745"
            }
        elif score >= 0.80:
            return {
                "message": "いいですね (Ii desu ne). Very good, almost there.",
                "status": "good",
                "color": "#17a2b8"
            }
        elif score >= 0.50:
            return {
                "message": "頑張って！ (Ganbatte!) You are close, try to speak clearer.",
                "status": "retry",
                "color": "#ffc107"
            }
        else:
            return {
                "message": "もう一度お願いします (Mou ichido onegaishimasu). Please try again.",
                "status": "fail",
                "color": "#dc3545"
            }

    def format_response(self, score, word_obj):
        """
        Combines evaluation data into a structured response for the UI.
        """
        feedback = self.get_feedback(score)
        return {
            "score": score,
            "original": word_obj.original,
            "furigana": word_obj.furigana,
            "english": word_obj.english,
            "feedback_msg": feedback["message"],
            "status": feedback["status"]
        }