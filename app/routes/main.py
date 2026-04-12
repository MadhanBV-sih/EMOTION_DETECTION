from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.services.emotion import detect_emotion_from_frame
from app.models import EmotionLog

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('landing.html')

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', username=session.get('username'))

@bp.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400
    
    emotion, details = detect_emotion_from_frame(data['image'])
    
    if emotion is None:
        return jsonify({'error': details}), 500
        
    # Log to DB
    confidence = details.get(emotion, 0.0)
    EmotionLog.create(session['user_id'], emotion, confidence)
    
    return jsonify({'emotion': emotion, 'details': details})

@bp.route('/api/history')
def history():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    logs = EmotionLog.get_recent(session['user_id'])
    data = [{
        'emotion': log['emotion'],
        'confidence': log['confidence'],
        'timestamp': log['timestamp']
    } for log in logs]
    
    return jsonify(data)
