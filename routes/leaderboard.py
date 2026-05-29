from flask import Blueprint, render_template
from flask_login import current_user
from models.user import User
from utils.helpers import seconds_to_hours

leaderboard_bp = Blueprint("leaderboard", __name__)

@leaderboard_bp.route("/leaderboard")
def index():
    top_xp = User.query.order_by(User.xp.ddesc()).limit(50).all()
    top_streak = (
        User.query
        .join(User.stats)
        .order_by(User.stats.property.mapper.class_.streak_days.desc())
        .limit(50)
        .all()
    )

    top_hours = (
        User.query
        .join(User.stats)
        .order_by(User.stats.property.mapper.class_.total_seconds.desc())
        .all()
    )

    return render_template(
        "leaderboard.html",
        top_xp=top_xp,
        top_streak=top_streak,
        top_hours=top_hours,
        current_user=current_user,
        seconds_to_hours=seconds_to_hours,
    )