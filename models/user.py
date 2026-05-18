from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    hackatime_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(300), nullable=True)

    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    rank = db.Column(db.String(100), default="Novice Coder")

    access_token = db.Column(db.String(300), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_synced = db.Column(db.DateTime, nullable=True)

    achievements = db.relationship("UserAchievement", backref="user", lazy=True)
    stats = db.relationship("UserStats", backref="user", uselist=False, lazy=True)
    quests = db.relationship("DailyQuest", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username} | Level {self.level} | {self.xp} XP>"