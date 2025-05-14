
import streamlit as st
import datetime

st.set_page_config(layout="wide")
st.title("축구 베팅 모델 v7.0 - 리그 변경 시 드롭다운 반영 완전 수정판")

league_teams = {
    "EPL": ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
        "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham",
        "Liverpool", "Luton", "Man City", "Man United", "Newcastle",
        "Nottingham Forest", "Sheffield United", "Tottenham", "West Ham", "Wolves"],
    "La Liga": ["Alavés", "Athletic Club", "Atlético Madrid", "Barcelona", "Cádiz",
        "Celta Vigo", "Getafe", "Girona", "Granada", "Las Palmas",
        "Mallorca", "Osasuna", "Rayo Vallecano", "Real Betis", "Real Madrid",
        "Real Sociedad", "Sevilla", "Valencia", "Villarreal", "Leganés"],
    "Serie A": ["Atalanta", "Bologna", "Cagliari", "Empoli", "Fiorentina",
        "Frosinone", "Genoa", "Inter", "Juventus", "Lazio",
        "Lecce", "AC Milan", "Monza", "Napoli", "Roma",
        "Salernitana", "Sassuolo", "Torino", "Udinese", "Verona"],
    "Bundesliga": ["Augsburg", "Bayer Leverkusen", "Bayern Munich", "Bochum", "Darmstadt",
        "Dortmund", "Eintracht Frankfurt", "Freiburg", "Heidenheim", "Hoffenheim",
        "Köln", "Mainz", "Mönchengladbach", "RB Leipzig", "Union Berlin",
        "Stuttgart", "Werder Bremen", "Wolfsburg"],
    "Ligue 1": ["Brest", "Clermont", "Le Havre", "Lens", "Lille",
        "Lorient", "Lyon", "Marseille", "Metz", "Monaco",
        "Montpellier", "Nantes", "Nice", "Paris SG", "Reims",
        "Rennes", "Strasbourg", "Toulouse"]
}

st.header("1. 경기 수동 등록")
if "matches" not in st.session_state:
    st.session_state.matches = []

with st.form("match_form"):
    league = st.selectbox("리그 선택", list(league_teams.keys()), key="league_select")
    home = st.selectbox("홈 팀", league_teams[league], key=f"home_{league}")
    away = st.selectbox("원정 팀", [t for t in league_teams[league] if t != home], key=f"away_{league}")
    date_input = st.date_input("경기 날짜", value=datetime.date.today(), key="date_select")
    col1, col2 = st.columns(2)
    with col1:
        hour = st.selectbox("시", list(range(0, 24)), key="hour_select")
    with col2:
        minute = st.selectbox("분", [0, 15, 30, 45], key="minute_select")
    submit = st.form_submit_button("경기 추가")
    if submit:
        st.session_state.matches.append({
            "Date": str(date_input),
            "Time": f"{hour:02}:{minute:02}",
            "League": league,
            "Home": home,
            "Away": away
        })

st.header("2. 예측 생성 및 조합 추천")
if st.button("예측 생성"):
    for match in st.session_state.matches:
        elo_diff = len(match["Home"]) - len(match["Away"])
        if elo_diff > 0:
            match["Prediction"] = "승"
            match["Value"] = 0.06
        elif elo_diff == 0:
            match["Prediction"] = "무"
            match["Value"] = 0.02
        else:
            match["Prediction"] = "패"
            match["Value"] = -0.05

if st.session_state.matches:
    st.subheader("전체 경기 및 예측 결과")
    st.dataframe(st.session_state.matches)

if st.button("조합 추천"):
    filtered = [m for m in st.session_state.matches if m.get("Value", -1) >= 0]
    st.markdown("### ✅ 4폴 조합 (수익 전략)")
    for m in filtered[:4]:
        st.write(f"{m['Home']} vs {m['Away']} → {m['Prediction']} (value: {m['Value']})")
    st.markdown("### 🎯 10폴 조합 (재미 전략)")
    for m in filtered[:10]:
        st.write(f"{m['Home']} vs {m['Away']} → {m['Prediction']} (value: {m['Value']})")
    st.markdown("### ⚡ 고적중 전략")
    if filtered:
        top = max(filtered, key=lambda x: x["Value"])
        st.write(f"{top['Home']} vs {top['Away']} → {top['Prediction']} (value: {top['Value']})")
    else:
        st.write("value ≥ 0인 예측이 없습니다.")
