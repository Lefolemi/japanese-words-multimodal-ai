from app.models.vocabulary import Vocabulary
from app import db

class SessionManager:
    @staticmethod
    def get_total_sessions(level, limit=20):
        """
        Calculates the total number of sessions available for a specific JLPT level.
        Example: 105 words / 20 = 5 sessions (with the last session holding 25 words).
        """
        count = Vocabulary.query.filter_by(jlpt_level=level).count()
        if count == 0: 
            return 0
        
        # Use floor division to determine how many full 20-word blocks exist.
        # We use max(1, ...) to ensure at least one session exists if there are words.
        return max(1, count // limit)

    @staticmethod
    def get_session_words(level, session_idx, limit=20):
        """
        Retrieves a specific 20-word slice from the database.
        """
        query = Vocabulary.query.filter_by(jlpt_level=level).order_by(Vocabulary.id)
        total_count = query.count()
        total_sessions = max(1, total_count // limit)

        offset = session_idx * limit
        
        # Final session handling: return all remaining words
        if session_idx >= total_sessions - 1:
            return query.offset(offset).all()
        
        # Standard session handling: return exactly 20 words
        return query.offset(offset).limit(limit).all()