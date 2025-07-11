from models import Player, Rank
from sheets import load_players, save_players

games_played = 0  # bạn có thể lưu biến này vào Google Sheet nếu muốn duy trì

def assign_points(rank_name, placements):
    pts = []
    if rank_name == "Cao cấp":
        scores = [3, 2, 1] + [0] * (len(placements) - 3)
    elif rank_name == "Trung cấp":
        scores = [2, 1] + [0] * (len(placements) - 2)
    else:
        scores = [1] + [0] * (len(placements) - 1)
    for i, name in enumerate(placements):
        pts.append((name, scores[i]))
    return pts

def update_players_scores(players, results_by_table, ranks_by_table):
    global games_played
    games_played += 1
    for table, placements in results_by_table.items():
        rank_name = ranks_by_table.get(table)
        if not placements or not rank_name:
            continue
        points = assign_points(rank_name, placements)
        for name, pts in points:
            player = next((p for p in players if p.name == name), None)
            if player:
                player.session_points += pts
                player.total_points += pts
    if games_played % 2 == 0:
        process_rank_changes(players)
    save_players(players)

def process_rank_changes(players):
    rank_names = ["Cao cấp", "Trung cấp", "Sơ cấp"]
    for i in range(len(rank_names) - 1):
        upper = rank_names[i]
        lower = rank_names[i + 1]
        upper_players = [p for p in players if str(p.rank) == upper]
        lower_players = [p for p in players if str(p.rank) == lower]
        if not upper_players or not lower_players:
            continue
        lowest_upper = min(upper_players, key=lambda p: p.session_points)
        highest_lower = max(lower_players, key=lambda p: p.session_points)
        lowest_upper.rank = lowest_upper.rank.down()
        highest_lower.rank = highest_lower.rank.up()
    for p in players:
        p.session_points = 0
