from app import create_app, socketio
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

app = create_app()

if __name__ == '__main__':
    # Using socketio.run instead of app.run for real-time STT features
    socketio.run(app, debug=False)