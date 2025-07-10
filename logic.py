from models import Player, Rank
from sheets import load_players, save_players

def assign_points(rank_name, placements):
    pts = []
    if rank_name == "Cao cấp":
        scores = [3, 2, 1] + [0] * (len(placements) - 3)
    elif rank_name == "Trung cấp":
        scores = [2, 1] + [0] * (len(placements) - 2)
    else:  # Sơ cấp
        scores = [1] + [0] * (len(placements) - 1)

    for i, name in enumerate(placements):
        pts.append((name, scores[i]))
    return pts

def update_ranks(players, results_by_table):
    for table, names in results_by_table.items():
        if not names:
            continue
        top = names[0]
        bottom = names[-1]

        p_top = next((p for p in players if p.name == top), None)
        p_bot = next((p for p in players if p.name == bottom), None)

        if p_top:
            p_top.rank = p_top.rank.up()
        if p_bot:
            p_bot.rank = p_bot.rank.down()
