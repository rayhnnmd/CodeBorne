from app import db
from datetime import datetime


class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(10), nullable=False)
    rarity = db.Column(db.String(20), nullable=False)
    xp_reward = db.Column(db.Integer, default=0)
    flavor_text = db.Column(db.String(200), nullable=True)

    unlocks = db.relationship("UserAchievement", backref="achievement", lazy=True)

    def __repr__(self):
        return f"<Achievement {self.name} [{self.rarity}]>"
    
class UserAchievement(db.Model):
    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey("achievements.id"), nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserAchievement user={self.user_id} achievement={self.achievement_id}>"
