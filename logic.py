from models import Player, Rank
from sheets import load_players, save_players

def assign_points(rank_name, placements):
    pts = []
    scores = [3, 2, 1] + [0] * (len(placements) - 3)  # áp dụng chung cho mọi bàn
    for i, name in enumerate(placements):
        pts.append((name, scores[i]))
    return pts

def update_players_scores(players, results_by_table, ranks_by_table):
    for table, placements in results_by_table.items():
        rank_name = ranks_by_table.get(table)
        if not placements or not rank_name:
            continue
        points = assign_points(rank_name, placements)
        for name, pts in points:
            player = next((p for p in players if p.name == name), None)
            if player:
                player.session_points += pts
    save_players(players)

def update_ranks_after_session(players):
    rank_names = ["Cao cấp", "Trung cấp", "Sơ cấp"]
    for i in range(len(rank_names) - 1):
        upper = rank_names[i]
        lower = rank_names[i + 1]
        upper_players = [p for p in players if str(p.rank) == upper]
        lower_players = [p for p in players if str(p.rank) == lower]
        if not upper_players or not lower_players:
            continue

        # Người thấp điểm nhất ở rank cao → xuống hạng
        lowest_upper = min(upper_players, key=lambda p: p.session_points)
        lowest_upper.rank = lowest_upper.rank.down()

        # Người cao điểm nhất ở rank thấp → lên hạng
        highest_lower = max(lower_players, key=lambda p: p.session_points)
        highest_lower.rank = highest_lower.rank.up()

    # Reset lại điểm session sau khi xét hạng
    for p in players:
        p.session_points = 0

    save_players(players)

def finalize_session(players):
    # Cộng điểm session vào total trước khi xét rank
    for p in players:
        p.total_points += p.session_points
    update_ranks_after_session(players)
