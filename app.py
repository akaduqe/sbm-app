
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Soccer Betting AI v5.2", layout="wide")
st.title("Soccer Betting Model v5.2")
st.subheader("5대리그 통합 · 실전 자동 조합 · 시각화 웹앱")

matches = pd.DataFrame([
    {"Match": "Man City vs Arsenal", "League": "EPL", "Prediction": "Home", "Odds": 1.95, "ml_value": 0.16},
    {"Match": "Barcelona vs Sevilla", "League": "LaLiga", "Prediction": "Home", "Odds": 1.80, "ml_value": 0.14},
    {"Match": "Juventus vs Napoli", "League": "SerieA", "Prediction": "Draw", "Odds": 3.2, "ml_value": 0.15},
    {"Match": "Dortmund vs Bayern", "League": "Bundesliga", "Prediction": "Away", "Odds": 2.05, "ml_value": 0.13},
    {"Match": "PSG vs Lyon", "League": "Ligue1", "Prediction": "Home", "Odds": 1.70, "ml_value": 0.18},
])

top_matches = matches.sort_values("ml_value", ascending=False).head(4).reset_index(drop=True)
total_odds = round(np.prod(top_matches["Odds"]), 2)
expected_return = round(total_odds * 1000)

st.markdown("### 고적중 전략 조합 (Top 4 Value)")
st.dataframe(top_matches)

st.markdown(f"**조합 총 배당:** {total_odds}배")
st.markdown(f"**예상 수익 (1,000원 베팅 시):** {expected_return}원")

with st.sidebar:
    st.header("설정")
    stake = st.slider("베팅 금액 (원)", 1000, 10000, 1000, 500)
    st.markdown("---")
    st.write(f"현재 조합 수익 시뮬레이션: {round(total_odds * stake)}원")

st.success("Streamlit 기반 웹앱입니다. 홈화면에 추가하면 앱처럼 실행할 수 있습니다.")
