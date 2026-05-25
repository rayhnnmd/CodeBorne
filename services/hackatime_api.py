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
    base = current_app.config["HACKATIME_BASE_URL"]
    resp = requests.get(f"{base}/users/current", headers=_headers(token))
    resp.raise_for_status()
    return resp.json().get("data", {})


def fetch_stats(token):
    base = current_app.config["HACKATIME_BASE_URL"]
    resp = requests.get(
        f"{base}/users/current/stats/all_time",
        headers=_headers(token)
    )
    resp.raise_for_status()
    return resp.json().get("data", {})

def fetch_projects(token):
    base = current_app.config["HACKATIME_BASE_URL"]
    resp = requests.get(

        f"{base}/users/current/projects",
        headers=_headers(token)
    )
    resp.raise_for_status()
    return resp.json().get("data", [])