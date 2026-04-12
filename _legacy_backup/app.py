import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import cv2
import numpy as np
import base64
from flask import jsonify
from fer.fer import FER

# Initialize FER with MTCNN for better accuracy
try:
    detector = FER(mtcnn=True)
except:
    print("MTCNN failed, falling back to default")
    detector = FER()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key
DB_NAME = "users.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', username=session.get('username'))
    return render_template('index.html')

@app.route('/app')
def emotion_app():
    if 'user_id' not in session:
        flash("Please log in to access the Calm Mirror.")
        return redirect(url_for('index'))
    return render_template('app.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Username and password are required.")
        return redirect(url_for('index'))

    password_hash = generate_password_hash(password)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
        flash("Account created! Please log in.")
    except sqlite3.IntegrityError:
        flash("Username already exists.")
    
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect(url_for('index'))
    else:
        flash("Login Failed")
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400
    
    image_data = data['image']
    try:
        # Remove header if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
             return jsonify({'error': 'Failed to decode image'}), 400

        # Detect
        result = detector.detect_emotions(img)
        
        if result:
            # Get dominant emotion of the first face
            emotions = result[0]['emotions']
            dominant_emotion = max(emotions, key=emotions.get)
            return jsonify({'emotion': dominant_emotion, 'details': emotions})
        else:
            return jsonify({'emotion': 'neutral', 'details': {}})
            
    except Exception as e:
        print(f"Error in detection: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
