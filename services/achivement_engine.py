import json
from datetime import datetime
from models.achievement import Achievement, UserAchievement
from app import db


ACHIEVEMENTS = [
    {
        "slug": "first_blood",
        "name": "First Blood",
        "icon": "sword",
        "description": "Log your first hour of coding",
        "rarity": "common",
        "xp_reward": 50,
        "flavor_text": "Every legend has a beginning.",
        "condition": lambda s: s["total_seconds"] >= 3600,
    },
    {
        "slug": "grinder",
        "name": "Grinder",
        "icon": "gear",
        "description": "Code for 100 total hours",
        "rarity": "rare",
        "xp_reward": 500,
        "flavor_text": "The forge never sleeps.",
        "condition": lambda s: s["total_seconds"] >= 360000,
    },
    {
        "slugs": "addicted",
        "name": "Addicted",
        "icon": "skull",
        "description": "Code for 500 total hours",
        "rarity": "epic",
        "xp_reward": 2000,
        "flavor_text": "There is no CUURRAEE(cure).",
        "condition": lambda s: s["total_seconds"] >= 1800000,
    },
    {
        "slug": "no_lifer",
        "name": "No Lifer",
        "icon": "moon",
        "description": "Code for 8 hours in a single day",
        "rarity": "rare",
        "xp_reward": 300,
        "flavor_text": "Sleep is for the weakks.",
        "condition": lambda s: s["best_day_seconds"] >= 28800,
    },
    {
        "slug": "unbroken_flame",
        "name": "Unbroken Flame",
        "icon": "flame",
        "description": "Maintain a 7-day streak",
        "rarity": "rare",
        "xp_reward": 350,
        "flavor_text": "With the power of Consistency.",
        "condition": lambda s: s["streak_days"] >= 7,
    },
    {
        "slug": "discipline",
        "name": "Discipline",
        "icon": "shield",
        "description": "Maintain a 30-day streak",
        "rarity": "epic", 
        "xp_reward": 1500,
        "flavor_text": "Iron will, iron code.",
        "condition": lambda s: s["streak_days"] >= 30,
    },
    {
        "slug": "polyglot",
        "name": "Polyglot",
        "icon": "globe",
        "description": "Write code in 5 or more languages",
        "rarity": "rare",
        "xp_reward": 400,
        "flavor_text": "You got that Duolingo bird in you.",
        "condition": lambda s: s["languages_count"] >= 5,
    },
    {
        "slug": "archmage",
        "name": "Archmage",
        "icon": "staff",
        "description": "Reach 100 total hours",
        "rarity": "legendary",
        "xp_reward": 1000,
        "flavor_text": "The arcane arts bow to you.",
        "condition": lambda s: s["total_seconds"] >= 360000,
    },
    {
        "slug": "builder",
        "name": "Builder",
        "icon": "hammer",
        "description": "Work on your first project",
        "rarity": "common",
        "xp_reward": 100,
        "flavor_text": "From nothing, something.",
        "condition": lambda s: s["projects_count"] >= 1,
    },
    {
        "slug": "architect",
        "name": "Architect",
        "icon": "castle",
        "description": "Work on 10 different projects",
        "rarity": "epic",
        "xp_reward": 800,
        "flavor_text": "An Empire of Repos.",
        "condition": lambda s: s["projects_count"] >= 10,
    },
    {
        "slug": "touched_grass",
        "name": "Touched Grass",
        "icon": "leaf",
        "edscription": "Haven't coded for 7 days straight",
        "rarity": "common",
        "xp_reward": 10,
        "flavor_text": "Verified outside person. Disapponting(not quite, jk ;()",
        "condition": lambda s: s.get("days_inactive", 0) >= 7,
    },
]

def seed_achievements():
    for a in ACHIEVEMENTS:
        exists = Achievement.query.filter_by(slug=a["slug"]).first()
        if not exists:
            db.session.add(Achievement(
                slug=a["slug"],
                name=a["name"],
                icon=a["icon"],
                description=a["description"],
                rarity=a["rarity"],
                xp_reward=a["xp_reward"],
                flavor_text=a["flavor_text"],
            ))
    db.session.commit()

def evaluate_achievements(user, stats_dict):
    newly_unlocked = []

    already_unlocked = {
        ua.achievement_id for ua in user.achievements
    }

    for a in ACHIEVEMENTS:
        achievement = Achievement.query.filter_by(slug=a["slug"]).first()
        if not achievement:
            continue
        if achievement.id in already_unlocked:
            continue
        if a["condition"](stats_dict):
            db.session.add(UserAchievement(
                user_id=user.id,
                achievement_id=achievement.id,
                unlocked_at=datetime.utcnow()
            ))
            newly_unlocked.append(achievement)
    
    db.session.commit()
    return newly_unlocked