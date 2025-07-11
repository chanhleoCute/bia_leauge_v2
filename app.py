# === main.py ===
import streamlit as st
import pandas as pd
import altair as alt
from models import Player, Rank
from sheets import load_players
from logic import assign_points, update_players_scores

st.set_page_config(page_title="🎱 Bảng xếp hạng Bi-a", layout="centered")

st.title("🎱 Bảng Xếp Hạng Bi-a 10 Người")

if "players" not in st.session_state:
    st.session_state.players = load_players()
players = st.session_state.players

# Khởi tạo nếu chưa có danh sách
if not players:
    st.subheader("📥 Nhập danh sách người chơi lần đầu:")
    names = [st.text_input(f"Tên người chơi {i+1}", key=f"player_{i}") for i in range(10)]
    if st.button("✅ Tạo danh sách"):
        players = [Player(name.strip()) for name in names if name.strip()]
        from sheets import save_players
        save_players(players)
        st.session_state.players = load_players()
        st.rerun()
    st.stop()

# === Leaderboard ===
st.subheader("📊 Bảng xếp hạng (Leaderboard)")
players_sorted = sorted(players, key=lambda x: x.total_points, reverse=True)
df = pd.DataFrame([{
    "Tên": p.name,
    "Cấp bậc": str(p.rank),
    "Điểm 2 buổi": p.session_points,
    "Tổng điểm": p.total_points
} for p in players_sorted])

selected_ranks = st.multiselect("🔎 Lọc theo cấp bậc", ["Cao cấp", "Trung cấp", "Sơ cấp"], default=["Cao cấp", "Trung cấp", "Sơ cấp"])
df_filtered = df[df["Cấp bậc"].isin(selected_ranks)]

def highlight_rank(row):
    color_map = {
        "Cao cấp": "background-color: #ffd700",
        "Trung cấp": "background-color: #add8e6",
        "Sơ cấp": "background-color: #f08080"
    }
    return [color_map.get(row["Cấp bậc"], "")] * len(row)

st.dataframe(df_filtered.style.apply(highlight_rank, axis=1), use_container_width=True, height=400)

# === Biểu đồ ===
st.subheader("📈 Biểu đồ so sánh điểm")
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("Tên", sort="-y"),
    y="Tổng điểm:Q",
    color="Cấp bậc:N"
).properties(width=700, height=400)
st.altair_chart(chart, use_container_width=True)

# === Nhập kết quả ===
st.markdown("---")
st.subheader("🎮 Nhập kết quả buổi chơi")
results = {}
for table in ["Cao cấp", "Trung cấp", "Sơ cấp"]:
    st.markdown(f"**Bàn {table}**")
    n = st.number_input(f"Số người chơi tại bàn {table}", 0, 5, key=f"num_{table}")
    players_in_rank = [p.name for p in players if str(p.rank) == table]
    selected = []
    table_results = []
    for i in range(n):
        available = [name for name in players_in_rank if name not in selected]
        if available:
            choice = st.selectbox(f"Vị trí {i+1} tại bàn {table}", available, key=f"{table}_{i}")
            selected.append(choice)
            table_results.append(choice)
    results[table] = table_results

if st.button("📥 Cập nhật kết quả"):
    results_by_table = {table: order for table, order in results.items() if order}
    ranks_by_table = {table: table for table in results_by_table}
    update_players_scores(players, results_by_table, ranks_by_table)
    st.session_state.players = load_players()
    st.success("✅ Đã cập nhật kết quả và xếp hạng sau buổi chơi!")
    st.rerun()
