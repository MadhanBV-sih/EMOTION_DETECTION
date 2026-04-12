from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for('auth.signup'))
            
        if User.create(username, generate_password_hash(password)):
            flash("Account created! Please log in.")
            return redirect(url_for('auth.login'))
        else:
            flash("Username already exists.")
            
    return render_template('auth.html', mode='signup')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid username or password.")
            
    return render_template('auth.html', mode='login')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
