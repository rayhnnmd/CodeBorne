import json
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from models.stats import UserStats
from services.hackatime_api import fetch_stats, fetch_projects, should_refresh
from services.xp_system import calculate_xp, calculate_level, get_rank, xp_to_next_level
from services.achievement_engine import evaluate_achievements, seed_achievements
from utils.helpers import seconds_to_hours, seconds_to_display

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    _sync_if_needed(current_user)

    stats = current_user.stats
    projects = json.loads(stats.projects_json)
    languages = json.loads(stats.languages_json)

    xp_needed = xp_to_next_level(current_user.xp)
    next_level = current_user.level + 1

    # build achievement list with locked/unlocked state for the template
    unlocked_ids = {ua.achievement_id for ua in current_user.achievements}
    from models.achievement import Achievement
    all_achievements = Achievement.query.all()
    achievement_data = []
    for a in all_achievements:
        achievement_data.append({
            "achievement": a,
            "unlocked": a.id in unlocked_ids,
            "unlocked_at": next(
                (ua.unlocked_at for ua in current_user.achievements if ua.achievement_id == a.id),
                None
            ),
        })

    return render_template(
        "dashboard.html",
        user=current_user,
        stats=stats,
        projects=projects,
        languages=languages,
        achievements=achievement_data,
        xp_needed=xp_needed,
        next_level=next_level,
        total_hours=seconds_to_hours(stats.total_seconds),
        best_day=seconds_to_display(stats.best_day_seconds),
    )


def _sync_if_needed(user):
    # skip API call if data is still fresh
    if not should_refresh(user.last_synced):
        return

    try:
        raw_stats = fetch_stats(user.access_token)
        raw_projects = fetch_projects(user.access_token)

        stats = user.stats or UserStats(user_id=user.id)

        stats.total_seconds = raw_stats.get("total_seconds", 0)
        stats.best_day_seconds = raw_stats.get("best_day", {}).get("total_seconds", 0)
        stats.streak_days = raw_stats.get("streak", {}).get("length", 0)
        stats.languages_count = len(raw_stats.get("languages", []))
        stats.languages_json = json.dumps(raw_stats.get("languages", []))
        stats.projects_count = len(raw_projects)
        stats.projects_json = json.dumps(raw_projects)
        stats.fetched_at = datetime.utcnow()

        db.session.add(stats)

        # recalculate RPG stats from fresh data
        stats_dict = {
            "total_seconds": stats.total_seconds,
            "best_day_seconds": stats.best_day_seconds,
            "streak_days": stats.streak_days,
            "languages_count": stats.languages_count,
            "projects_count": stats.projects_count,
        }

        user.xp = calculate_xp(
            stats.total_seconds,
            stats.streak_days,
            stats.projects_count
        )
        user.level = calculate_level(user.xp)
        user.rank = get_rank(user.level)
        user.last_synced = datetime.utcnow()

        seed_achievements()
        evaluate_achievements(user, stats_dict)

        db.session.commit()

    except Exception as e:
        # don't crash the dashboard if the API is down
        print(f"[sync error] {e}")