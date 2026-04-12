from flask import Flask
import sqlite3
import os

DB_NAME = "users.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['DATABASE'] = os.path.join(os.getcwd(), DB_NAME)

    from .routes import auth, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    from .models import close_db
    app.teardown_appcontext(close_db)

    init_db(app)

    return app

def init_db(app):
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS emotion_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                emotion TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            );
        ''')
        conn.commit()
