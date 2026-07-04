from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.join("static", "cards")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BG          = (10, 9, 7)
PANEL       = (21, 18, 16)
GOLD        = (200, 168, 75)
GOLD_DIM    = (139, 105, 20)
OFF_WHITE   = (232, 220, 200)
MUTED       = (106, 90, 64)
BURN        = (139, 58, 15)

RARITY_COLORS = {
    "common":    (160, 144, 112),
    "rare":      (79, 195, 247),
    "epic":      (206, 147, 216),
    "legendary": (200, 168, 75),
    "mythic":    (255, 107, 107),
}


def _load_font(size):
    attempts = [
        "Georgia.ttf",
        "georgia.ttf",
        "DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "C:/Windows/Fonts/georgia.ttf",
    ]
    for path in attempts:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def generate_card(user, stats):
    W, H = 700, 380
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W - 1, H - 1], outline=GOLD_DIM, width=1)

    draw.rectangle([12, 12, W - 13, H - 13], fill=PANEL)

    for x, y, dx, dy in [(12, 12, 1, 1), (W-13, 12, -1, 1), (12, H-13, 1, -1), (W-13, H-13, -1, -1)]:
        draw.line([(x, y), (x + dx * 18, y)], fill=GOLD, width=2)
        draw.line([(x, y), (x, y + dy * 18)], fill=GOLD, width=2)

    f_title  = _load_font(32)
    f_rank   = _load_font(13)
    f_label  = _load_font(12)
    f_value  = _load_font(20)
    f_small  = _load_font(11)

    draw.text((36, 32), user.username, font=f_title, fill=OFF_WHITE)

    rank_text = user.rank.upper()
    draw.text((36, 76), rank_text, font=f_rank, fill=GOLD)

    draw.line([(36, 100), (W - 36, 100)], fill=GOLD_DIM, width=1)

    stats_data = [
        ("LEVEL",   str(user.level)),
        ("TOTAL XP", f"{user.xp:,}"),
        ("HOURS",   f"{round(stats.total_seconds / 3600, 1)}h"),
        ("STREAK",  f"{stats.streak_days}d"),
    ]

    col_w = (W - 72) // 4
    for i, (label, value) in enumerate(stats_data):
        x = 36 + i * col_w
        draw.text((x, 122), label, font=f_label, fill=MUTED)
        draw.text((x, 140), value, font=f_value, fill=GOLD)

    # divider
    draw.line([(36, 186), (W - 36, 186)], fill=GOLD_DIM, width=1)

    draw.text((36, 200), "ACHIEVEMENTS", font=f_label, fill=MUTED)

    from models.achievement import Achievement, UserAchievement
    from app import db
    unlocked = (
        db.session.query(Achievement)
        .join(UserAchievement)
        .filter(UserAchievement.user_id == user.id)
        .order_by(UserAchievement.unlocked_at.desc())
        .limit(4)
        .all()
    )

    if unlocked:
        for i, ach in enumerate(unlocked):
            x = 36 + i * 160
            color = RARITY_COLORS.get(ach.rarity, MUTED)
            draw.rectangle([x, 222, x + 148, 280], outline=color, width=1)
            draw.text((x + 10, 232), ach.name, font=f_small, fill=OFF_WHITE)
            draw.text((x + 10, 252), ach.rarity.upper(), font=f_small, fill=color)
    else:
        draw.text((36, 230), "No achievements yet.", font=f_small, fill=MUTED)

    draw.line([(36, 300), (W - 36, 300)], fill=GOLD_DIM, width=1)
    draw.text((36, 314), "CodeBorne", font=f_rank, fill=GOLD)
    draw.text((W - 36, 314), "hackatime.hackclub.com", font=f_small, fill=MUTED, anchor="ra")

    path = os.path.join(OUTPUT_DIR, f"{user.username}.png")
    img.save(path)
    return path