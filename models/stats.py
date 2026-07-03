from app import db
from datetime import datetime

class UserStats(db.Model):
    __tablename__ = "user_stats"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    total_seconds = db.Column(db.Integer, default=0)
    best_day_seconds = db.Column(db.Integer, default=0)
    streak_days = db.Column(db.Integer, default=0)
    languages_count = db.Column(db.Integer, default=0)
    projects_count = db.Column(db.Integer, default=0)

    languages_json = db.Column(db.Text, default="[]")
    projects_json = db.Column(db.Text, default="[]")

    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return f"<UserStats user={self.user_id} total={self.total_seconds}s>"