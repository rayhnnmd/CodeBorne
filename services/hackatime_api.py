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
    # get total hours all time
    hours_resp = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/hours",
        headers=_headers(token)
    )
    streak_resp = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/streak",
        headers=_headers(token)
    )
    hours_resp.raise_for_status()
    streak_resp.raise_for_status()

    hours_data = hours_resp.json()
    streak_data = streak_resp.json()

    return {
        "total_seconds": hours_data.get("total_seconds", 0),
        "best_day": {"total_seconds": 0},
        "streak": {"length": streak_data.get("streak_days", 0)},
        "languages": [],
    }


def fetch_projects(token):
    resp = requests.get(
        "https://hackatime.hackclub.com/api/v1/authenticated/projects",
        headers=_headers(token)
    )
    resp.raise_for_status()
    return resp.json().get("projects", [])
   