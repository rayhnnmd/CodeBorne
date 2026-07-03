def seconds_to_hours(seconds, decimals=1):
    return round(seconds / 3600, decimals)

def seconds_to_display(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"
        
def get_rarity_color(rarity):
    colors = {
        "common":    "#aaaaaa",
        "rare":      "#4fc3f7",
        "epic":      "#ce93d8",
        "legendary":  "#f0c040",
        "mythic":    "#ff6b6b",
    }
    return colors.get(rarity, "#aaaaaa")