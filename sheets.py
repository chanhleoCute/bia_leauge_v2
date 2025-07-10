import gspread
from oauth2client.service_account import ServiceAccountCredentials
from models import Player, Rank

# Kết nối Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Tên Sheet
SHEET_NAME = "bialeague"
sheet = client.open(SHEET_NAME).sheet1

def load_players():
    records = sheet.get_all_records()
    players = []
    for r in records:
        name = r['name']
        rank = Rank.from_str(r['rank'])
        points = int(r['points'])
        players.append(Player(name, rank, points))
    return players

def save_players(players):
    sheet.clear()
    sheet.append_row(["name", "rank", "points"])
    for p in players:
        sheet.append_row([p.name, str(p.rank), p.points])
