import google.generativeai as genai
from flask import current_app
import os

class Sensei:
    def __init__(self, name="Sensei"):
        self.name = name
        # Get key from Flask's config
        api_key = current_app.config.get("GEMINI_API_KEY")
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-3.1-flash-lite')
            print("✅ Sensei is now Online and Intelligent.")
        else:
            self.model = None
            print("⚠️ WARNING: GEMINI_API_KEY not found in config.")

    def get_dynamic_feedback(self, score, user_text, target_text, english):
        if not self.model:
            return "頑張って！ (Ganbatte!)", "頑張って！"

        # Handle empty transcription early
        if not user_text or user_text.strip() == "[Silence]":
            return "声が聞こえませんでした。もう一度お願いします。(Koe ga kikoemasen deshita. Mou ichido onegaishimasu.)", "声が聞こえませんでした。もう一度お願いします。"

        # Instructions for the AI
        if score < 0.7:
            instruction = f"The user said '{user_text}' but should have said '{target_text}'. Focus on the phonetic mistake."
        elif score < 0.9:
            instruction = "Almost there. Give a small tip for improvement."
        else:
            instruction = "Perfect. Give a short compliment."

        prompt = f"""
        Act as a Japanese teacher. 
        Target: {target_text}
        User said: {user_text}
        Score: {score}
        Task: {instruction}
        Format: Japanese (Romaji)
        Max 12 words.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Use getattr to safely handle the response object
            full_text = getattr(response, 'text', '').strip().replace('*', '')
            
            if not full_text:
                raise ValueError("Empty response from Gemini")

            # Robust parsing for voice_text
            if '(' in full_text:
                voice_text = full_text.split('(')[0].strip()
            else:
                voice_text = full_text

            return full_text, voice_text

        except Exception as e:
            # THIS IS CRITICAL: This will tell you the ACTUAL error in your terminal
            print(f"DEBUG: Gemini call failed: {e}")
            return "上手ですね！ (Jouzu desu ne!)", "上手ですね！"

    def format_response(self, score, word_obj, user_transcription):
        """
        The central method called by socket_events. 
        Maps the raw data to the final Multimodal payload.
        """
        # If user said absolutely nothing
        input_text = user_transcription if user_transcription.strip() else "[Silence]"
        
        display_msg, voice_msg = self.get_dynamic_feedback(
            score, input_text, word_obj.furigana, word_obj.english
        )
        
        # Determine status for UI coloring
        status = "fail"
        if score >= 0.9: status = "success"
        elif score >= 0.7: status = "good"
        elif score >= 0.4: status = "retry"

        return {
            "score": score,
            "original": word_obj.original,
            "furigana": word_obj.furigana,
            "english": word_obj.english,
            "message": display_msg,
            "voice_text": voice_msg,
            "status": status
        }