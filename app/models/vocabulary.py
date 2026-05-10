from app import db

class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'
    
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(100), nullable=False)
    furigana = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(200), nullable=False)
    jlpt_level = db.Column(db.Integer, nullable=False)
    
    is_marked = db.Column(db.Boolean, default=False)
    times_practiced = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Float, default=0.0)

    def to_dict(self):
        """Converts the SQLAlchemy object into a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'original': self.original,
            'furigana': self.furigana,
            'english': self.english,
            'jlpt_level': self.jlpt_level,
            'is_marked': self.is_marked,
            'times_practiced': self.times_practiced,
            'last_score': self.last_score
        }

    def __repr__(self):
        return f'<Word {self.original} ({self.jlpt_level})>'