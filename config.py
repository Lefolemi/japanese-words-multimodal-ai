import os
from dotenv import load_dotenv

# Load the .env file from the root directory
load_dotenv()

class Config:
    # --- Security & Core ---
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sensei-secret-key'
    
    # --- Database ---
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'data', 'jp_game.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- Multimodal AI Keys ---
    # This will pull from your .env file
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # --- File Handling ---
    # Directories for temporary STT and TTS processing
    UPLOAD_FOLDER = os.path.join('app', 'static', 'audio_temp')
    TTS_FOLDER = os.path.join('app', 'static', 'audio_responses')
    
    # --- Removed Whisper (Legacy) ---
    # Whisper code removed as we are now using Vosk + Gemini for the brain.