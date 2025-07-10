import gspread
from oauth2client.service_account import ServiceAccountCredentials
from models import Player, Rank
import streamlit as st
import json

# Kết nối Google Sheets bằng secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])  # Đọc từ secrets
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Tên Sheet
SHEET_NAME = "bialeague"
sheet = client.open(SHEET_NAME).sheet1

def load_players():
    records = sheet.get_all_records()
    players = []

    for i, r in enumerate(records):
        try:
            name = r['name']
            rank = Rank.from_str(r['rank'])
            points = int(r['points'])
            players.append(Player(name, rank, points))
        except KeyError as e:
            print(f"Dòng {i+2} thiếu khóa: {e} - Giá trị r: {r}")
        except Exception as e:
            print(f"Dòng {i+2} lỗi không xác định: {e} - Giá trị r: {r}")

    return players


def save_players(players):
    sheet.clear()
    sheet.append_row(["name", "rank", "points"])
    for p in players:
        sheet.append_row([p.name, str(p.rank), p.points])
