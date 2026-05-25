from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.join("static", "cards")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_card(user, stats):
    width, height = 800, 400
    bg_color = (13, 13, 13)
    gold = (240, 192, 64)
    white = (255, 255, 255)
    gray = (150, 150, 150)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)


    draw.rectangle([2, 2, width - 3, height - 3], outline=gold, width=2)

    draw.text((40, 40), user.username, fill=gold, font=ImageFont.load_default())

    draw.text((40, 80), f"Level {user.level} - {user.rank}", fill=white, font=ImageFont.load_default())

    total_hours = round(stats.total_seconds / 3600, 1)
    draw.text((40, 130), f"{total_hours} hours coded", fill=gray, font=ImageFont.load_default())

    draw.text((40, 160), f"{stats.streak_days} day streak", fill=gray, font=ImageFont.load_default())

    path = os.path.join(OUTPUT_DIR, f"{user.username}.png")
    img.save(path)
    return path