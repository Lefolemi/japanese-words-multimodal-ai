import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sensei-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'data', 'jp_game.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('app', 'static', 'audio_temp')
    # Whisper settings
    WHISPER_MODEL = "base"