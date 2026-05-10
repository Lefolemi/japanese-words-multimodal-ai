import jaconv
import re
import Levenshtein

class Evaluator:
    @staticmethod
    def normalize_text(text):
        """
        Standardizes input text for phonetic comparison.
        """
        if not text:
            return ""

        # 1. Convert Katakana to Hiragana (e.g., シンド -> しんど)
        normalized = jaconv.kata2hira(text)

        # 2. Convert Full-width alphanumeric to Half-width (e.g., １０ -> 10)
        normalized = jaconv.z2h(normalized, kana=False, digit=True, ascii=True)

        # 3. Remove punctuation and symbols using Regex
        # Matches: 。、？！, .?!, and whitespace
        normalized = re.sub(r'[。\s、？！?.!,…「」]', '', normalized)

        return normalized.strip()

    def get_score(self, input_text, target_furigana):
        """
        Calculates similarity after script normalization.
        """
        norm_input = self.normalize_text(input_text)
        norm_target = self.normalize_text(target_furigana)

        if not norm_target:
            return 0.0

        # Calculate Levenshtein distance
        distance = Levenshtein.distance(norm_input, norm_target)
        max_len = max(len(norm_input), len(norm_target))
        
        score = 1.0 - (distance / max_len) if max_len > 0 else 0.0
        return round(max(0.0, score), 2)