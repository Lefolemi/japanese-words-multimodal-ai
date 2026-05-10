from flask import Blueprint, render_template, abort
from app.core.session_manager import SessionManager

session_bp = Blueprint('session', __name__)

# The URL must match: /session/start/<level>/<session_idx>
@session_bp.route('/start/<int:level>/<int:session_idx>')
def start_session(level, session_idx):
    if level < 1 or level > 5:
        abort(404)

    # We pass session_idx to the manager to get the specific slice
    words_objects = SessionManager.get_session_words(level=level, session_idx=session_idx)
    
    if not words_objects:
        return "Session index out of range for this level.", 404

    # Convert to dict for the frontend
    words_data = [word.to_dict() for word in words_objects]

    return render_template('session.html', 
                           words=words_data, 
                           level=level, 
                           session_idx=session_idx)