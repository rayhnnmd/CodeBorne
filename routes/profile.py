import json
from flask import Blueprint, render_template, abort, send_file
from flask_login import login_required, current_user
from models.user import User
from models.achievement import Achievement
from services.card_generator import generate_card
from utils.helpers import seconds_to_hours, get_rarity_color

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def me():
    # redirect to the current user's public profile
    return profile(current_user.username)


@profile_bp.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    unlocked_ids = {ua.achievement_id for ua in user.achievements}
    all_achievements = Achievement.query.all()

    showcase = []
    for a in all_achievements:
        if a.id in unlocked_ids:
            showcase.append({
                "achievement": a,
                "color": get_rarity_color(a.rarity),
                "unlocked_at": next(
                    (ua.unlocked_at for ua in user.achievements if ua.achievement_id == a.id),
                    None
                ),
            })

    projects = json.loads(user.stats.projects_json) if user.stats else []
    top_projects = sorted(projects, key=lambda p: p.get("total_seconds", 0), reverse=True)[:5]

    return render_template(
        "profile.html",
        profile_user=user,
        showcase=showcase,
        top_projects=top_projects,
        total_hours=seconds_to_hours(user.stats.total_seconds if user.stats else 0),
        is_own_profile=current_user.is_authenticated and current_user.id == user.id,
    )


@profile_bp.route("/profile/<username>/card")
def download_card(username):
    user = User.query.filter_by(username=username).first()
    if not user or not user.stats:
        abort(404)

    path = generate_card(user, user.stats)
    return send_file(path, mimetype="image/png", as_attachment=True, download_name=f"{username}_codeborne.png")