import requests
from flask import Blueprint, redirect, request, url_for, current_app
from flask_login import login_user, logout_user, login_required
from app import db
from models.user import User
from models.stats import UserStats
from services.hackatime_api import fetch_user_profile

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    params = {
        "client_id": current_app.config["HACKATIME_CLIENT_ID"],
        "redirect_uri": current_app.config["HACKATIME_REDIRECT_URI"],
        "response_type": "code",
        "scope": "profile read",
    }
    auth_url = current_app.config["HACKATIME_AUTH_URL"]
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return redirect(f"{auth_url}?{query}")


@auth_bp.route("/auth/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return redirect(url_for("auth.login"))

    token = _exchange_code_for_token(code)
    if not token:
        return "OAuth failed — could not get access token.", 400

    profile = fetch_user_profile(token)
    if not profile:
        return "Could not fetch Hackatime profile.", 400

    user = _get_or_create_user(profile, token)
    login_user(user)
    return redirect(url_for("dashboard.index"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


def _exchange_code_for_token(code):
    resp = requests.post(
        current_app.config["HACKATIME_TOKEN_URL"],
        data={
            "client_id": current_app.config["HACKATIME_CLIENT_ID"],
            "client_secret": current_app.config["HACKATIME_CLIENT_SECRET"],
            "redirect_uri": current_app.config["HACKATIME_REDIRECT_URI"],
            "grant_type": "authorization_code",
            "code": code,
        },
    )
    if resp.status_code != 200:
        return None
    return resp.json().get("access_token")


def _get_or_create_user(profile, token):
    # find existing user or create a fresh one on first login
    user = User.query.filter_by(hackatime_id=str(profile["id"])).first()
    if user:
        user.access_token = token
        db.session.commit()
        return user

    user = User(
        hackatime_id=str(profile["id"]),
        username=profile.get("username", "unknown"),
        avatar=profile.get("photo", None),
        access_token=token,
    )
    db.session.add(user)
    db.session.flush()

    # create empty stats row for this user right away
    db.session.add(UserStats(user_id=user.id))
    db.session.commit()
    return user