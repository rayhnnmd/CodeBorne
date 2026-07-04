import requests
from datetime import datetime, timedelta
from flask import current_app


def _headers(token):
    return {"Authorization": f"Bearer {token}"}


def should_refresh(last_synced):
    if last_synced is None:
        return True
    return datetime.utcnow() - last_synced > timedelta(minutes=15)

def fetch_user_profile(token):
    resp = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/me",
        headers=_headers(token)
    )
    resp.raise_for_status()
    return resp.json()

def fetch_stats(token):
    profile = fetch_user_profile(token)
    user_id = str(profile.get("id"))

    stats_resp = requests.get(
        f"https://hackatime.hackclub.com/api/v1/users/{user_id}/stats",
        headers=_headers(token)
    )
    stats_resp.raise_for_status()
    stats_data = streak_resp.json().get("data", {})

    streak_resp = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/streak",
        headers=_headers(token)
    )
    streak_resp.raise_for_status()
    streak_days = streak_resp.json().get("streak_days", 0)

    languages = []
    for l in stats_data.get("languages", []):
        languages.append({
            "name": l.get("name"),
            "total_seconds": l.get("total_seconds", 0)
        })

    return {
        "total_seconds": stats_data.get("total_seconds", 0),
        "best_day": {"total_seconds": 0},
        "streak": {"length": streak_days},
        "languages": languages,
    }


def fetch_projects(token):
    resp = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/projects",
        headers=_headers(token)
    )
    resp.raise_for_status()
    return resp.json().get("projects", [])
   