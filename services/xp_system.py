import math

LEVEL_THRESHOLDS = [
    0, 500, 1200, 2500, 5000, 9000, 15000, 
    23000, 35000, 50000, 70000, 95000, 125000
]

RANKS = [
    (0, "Novice Coder"),
    (5, "Code Warrior"),
    (11, "Shadow Engineer"),
    (21, "Arcane Developer"),
    (31, "Legendary Architect"),
    (51, "Mythic Overlord"),
]

def calculate_xp(total_seconds, streak_days, projects_count):
    total_hours = total_seconds / 3600
    return int(
        total_hours * 100
        + streak_days * 50
        + projects_count * 200
    )

def calculate_level(xp):
    for i, threshold in enumerate(reversed(LEVEL_THRESHOLDS)):
        return len(LEVEL_THRESHOLDS) - i
    return 1

def get_rank(level):
    rank = RANKS[0][1]
    for min_level, title in RANKS:
        if level >= min_level:
            rank = title
    return rank

def xp_to_next_level(current_xp):
    for threshold in LEVEL_THRESHOLDS:
        if current_xp < threshold:
            return threshold - current_xp
    return 10000
