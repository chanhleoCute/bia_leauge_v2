import streamlit as st
import pandas as pd
import altair as alt
from models import Player, Rank
from logic import load_players, save_players, assign_points, update_ranks

st.set_page_config(page_title="🎱 Bảng xếp hạng Bi-a", layout="centered")

st.title("🎱 Bảng Xếp Hạng Bi-a 10 Người")
st.markdown("""
    <style>
    body {
        background-color: #f0f4f8;
    }
    </style>
""", unsafe_allow_html=True)
players = load_players()

if "initialized" not in st.session_state:
    st.session_state.initialized = True

# ===================== KHỞI TẠO NGƯỜI CHƠI =====================
if not players:
    st.subheader("📥 Nhập danh sách người chơi lần đầu:")
    names = []
    for i in range(10):
        name = st.text_input(f"Tên người chơi {i+1}", key=f"player_{i}")
        names.append(name)

    if st.button("✅ Tạo danh sách"):
        players = [Player(name.strip()) for name in names if name.strip()]
        save_players(players)
        st.rerun()
    st.stop()

# ===================== LEADERBOARD =====================
st.subheader("📊 Bảng xếp hạng (Leaderboard)")

# Tạo bảng xếp hạng
players_sorted = sorted(players, key=lambda x: x.points, reverse=True)

df = pd.DataFrame([{
    "Tên": p.name,
    "Cấp bậc": str(p.rank),
    "Điểm": p.points
} for p in players_sorted])

# Bộ lọc cấp bậc
selected_ranks = st.multiselect(
    "🔎 Lọc theo cấp bậc",
    options=["Cao cấp", "Trung cấp", "Sơ cấp"],
    default=["Cao cấp", "Trung cấp", "Sơ cấp"]
)
df_filtered = df[df["Cấp bậc"].isin(selected_ranks)]

# Hiển thị bảng có màu cấp bậc
def highlight_rank(row):
    color_map = {
        "Cao cấp": "background-color: #ffd700",  # vàng
        "Trung cấp": "background-color: #add8e6",  # xanh nhạt
        "Sơ cấp": "background-color: #f08080"  # đỏ nhạt
    }
    return [color_map.get(row["Cấp bậc"], "")] * len(row)

st.dataframe(
    df_filtered.style.apply(highlight_rank, axis=1),
    use_container_width=True,
    height=400
)

# ===================== BIỂU ĐỒ SO SÁNH =====================
st.subheader("📈 Biểu đồ so sánh điểm")

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("Tên", sort="-y"),
        y="Điểm:Q",
        color="Cấp bậc:N"
    )
    .properties(width=700, height=400)
)
st.altair_chart(chart, use_container_width=True)

# ===================== NHẬP KẾT QUẢ BUỔI CHƠI =====================
st.markdown("---")
st.subheader("🎮 Nhập kết quả buổi chơi")

results = {}
for table in ["Cao cấp", "Trung cấp", "Sơ cấp"]:
    st.markdown(f"**Bàn {table}**")
    n = st.number_input(f"Số người chơi tại bàn {table}", 0, 5, key=f"num_{table}")
    table_results = []
    for i in range(n):
        name = st.selectbox(f"Vị trí {i+1} tại bàn {table}", [p.name for p in players], key=f"{table}_{i}")
        table_results.append(name)
    results[table] = table_results

if st.button("📥 Cập nhật kết quả"):
    for table, order in results.items():
        for name, pts in assign_points(table, order):
            for p in players:
                if p.name == name:
                    p.points += pts  # ✅ Cập nhật điểm
                    break
    update_ranks(players, results)
    save_players(players)
    st.success("✅ Đã cập nhật kết quả và xếp hạng!")
    st.rerun()
