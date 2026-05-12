from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def menu():
    return render_template('menu.html')

@main_bp.route('/levels')
def level_select():
    from app.core.session_manager import SessionManager
    
    # We only care about N5
    n5_data = {
        'num': 5,
        'total_sessions': SessionManager.get_total_sessions(level=5)
    }
    
    return render_template('level_select.html', levels=[n5_data])