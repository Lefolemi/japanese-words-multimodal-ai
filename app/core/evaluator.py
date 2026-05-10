import jaconv
import re
import Levenshtein
import pykakasi

class Evaluator:
    def __init__(self):
        """
        Initialize the converter once to keep scoring fast.
        """
        self.kks = pykakasi.kakasi()

    def normalize_text(self, text):
        """
        Standardizes input text for phonetic comparison.
        Converts Kanji to Hiragana, Katakana to Hiragana, and cleans symbols.
        """
        if not text:
            return ""

        # 1. Convert Kanji and Katakana to Hiragana using pykakasi
        # Example: "青いシンド" -> "あおいしんど"
        kks_result = self.kks.convert(text)
        normalized = "".join([item['hira'] for item in kks_result])

        # 2. Redundant check: ensure all Katakana are Hiragana (jaconv is safer for edge cases)
        normalized = jaconv.kata2hira(normalized)

        # 3. Convert Full-width alphanumeric to Half-width (e.g., １０ -> 10)
        normalized = jaconv.z2h(normalized, kana=False, digit=True, ascii=True)

        # 4. Remove punctuation and symbols using Regex
        normalized = re.sub(r'[。\s、？！?.!,…「」]', '', normalized)

        return normalized.strip()

    def get_score(self, input_text, target_furigana):
        """
        Calculates similarity after script normalization.
        Uses Levenshtein distance: 1.0 is a perfect match, 0.0 is completely different.
        """
        norm_input = self.normalize_text(input_text)
        norm_target = self.normalize_text(target_furigana)

        if not norm_target:
            return 0.0

        # Calculate Levenshtein distance
        distance = Levenshtein.distance(norm_input, norm_target)
        max_len = max(len(norm_input), len(norm_target))
        
        # Scoring Formula:
        # score = 1.0 - (distance / max_len)
        if max_len == 0:
            return 0.0
            
        score = 1.0 - (distance / max_len)
        return round(max(0.0, score), 2)