import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

class User:
    @staticmethod
    def create(username, password_hash):
        db = get_db()
        try:
            db.execute(
                "INSERT INTO user (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def get_by_username(username):
        db = get_db()
        return db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        return db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

class EmotionLog:
    @staticmethod
    def create(user_id, emotion, confidence):
        db = get_db()
        db.execute(
            "INSERT INTO emotion_log (user_id, emotion, confidence) VALUES (?, ?, ?)",
            (user_id, emotion, confidence)
        )
        db.commit()

    @staticmethod
    def get_recent(user_id, limit=20):
        db = get_db()
        return db.execute(
            "SELECT * FROM emotion_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
