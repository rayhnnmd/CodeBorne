from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.achievement import Achievement
from utils.helpers import get_rarity_color

achievements_bp = Blueprint("achievements", __name__)


@achievements_bp.route("/achievements")
@login_required
def index():
    unlocked_ids = {ua.achievement_id for ua in current_user.achievements}
    all_achievements = Achievement.query.all()

    unlocked = []
    locked = []

    for a in all_achievements:
        entry = {
            "achievement": a,
            "color": get_rarity_color(a.rarity),
            "unlocked_at": next(
                (ua.unlocked_at for ua in current_user.achievements if ua.achievement_id == a.id),
                None
            ),
        }
        if a.id in unlocked_ids:
            unlocked.append(entry)
        else:
            locked.append(entry)

    return render_template(
        "achievements.html",
        user=current_user,
        unlocked=unlocked,
        locked=locked,
        unlocked_count=len(unlocked),
        total_count=len(all_achievements),
    )