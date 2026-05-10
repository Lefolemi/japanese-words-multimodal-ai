import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import Config

# 1. Initialize extensions globally
db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*", async_mode='gevent')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 2. Bind extensions to the app instance
    db.init_app(app)
    socketio.init_app(app)

    # 3. Import and Register EVERYTHING ELSE inside the app_context
    with app.app_context():
        # Models must be imported before blueprints if they are used there
        from app.models import vocabulary 
        
        # Blueprints
        from app.routes.main import main_bp
        from app.routes.session import session_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(session_bp, url_prefix='/session')

        # Socket Events
        from app.socket_events import register_socket_events
        register_socket_events(socketio)

    return app