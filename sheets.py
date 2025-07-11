import gspread
from oauth2client.service_account import ServiceAccountCredentials
from models import Player, Rank
import streamlit as st
import json

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

SHEET_NAME = "bialeague"
sheet = client.open(SHEET_NAME).sheet1

def load_players():
    records = sheet.get_all_records()
    players = []
    for i, r in enumerate(records):
        try:
            name = r['name']
            rank = Rank.from_str(r['rank'])
            total_points = int(r.get('total_points', 0))
            session_points = int(r.get('session_points', 0))
            players.append(Player(name, rank, total_points, session_points))
        except Exception as e:
            print(f"Dòng {i+2} lỗi: {e} - Giá trị r: {r}")
    return players

def save_players(players):
    sheet.clear()
    sheet.append_row(["name", "rank", "total_points", "session_points"])
    for p in players:
        sheet.append_row([p.name, str(p.rank), p.total_points, p.session_points])