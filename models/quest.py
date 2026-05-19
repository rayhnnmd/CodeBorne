from app import db
from datetime import date


class DailyQuest(db.Model):
    __tablename__ = "daily_quests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    target_seconds = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    quest_date = db.Column(db.Date, default=date.today)
    xp_reward = db.Column(db.Integer, default=100)

    def __repr__(self):
        status = "done" if self.completed else "pending"
        return f"<DailyQuest {self.title} [{status}]>"