from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def menu():
    return render_template('menu.html')

@main_bp.route('/levels')
def level_select():
    from app.core.session_manager import SessionManager
    levels = []
    for n in range(1, 6):
        levels.append({
            'num': n,
            'total_sessions': SessionManager.get_total_sessions(level=n)
        })
    return render_template('level_select.html', levels=levels)