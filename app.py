
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Soccer Betting AI v5.3", layout="wide")
st.title("Soccer Betting Model v5.3")
st.subheader("전략별 조합 + ROI 분석 + 수동 결과 입력")

matches = pd.DataFrame([
    {"Match": "Man City vs Arsenal", "League": "EPL", "Prediction": "Home", "Odds": 1.95, "ml_value": 0.16},
    {"Match": "Barcelona vs Sevilla", "League": "LaLiga", "Prediction": "Home", "Odds": 1.80, "ml_value": 0.14},
    {"Match": "Juventus vs Napoli", "League": "SerieA", "Prediction": "Draw", "Odds": 3.2, "ml_value": 0.15},
    {"Match": "Dortmund vs Bayern", "League": "Bundesliga", "Prediction": "Away", "Odds": 2.05, "ml_value": 0.13},
    {"Match": "PSG vs Lyon", "League": "Ligue1", "Prediction": "Home", "Odds": 1.70, "ml_value": 0.18},
    {"Match": "Atletico vs Betis", "League": "LaLiga", "Prediction": "Home", "Odds": 1.90, "ml_value": 0.12},
    {"Match": "AC Milan vs Roma", "League": "SerieA", "Prediction": "Home", "Odds": 2.0, "ml_value": 0.14},
    {"Match": "Leverkusen vs Frankfurt", "League": "Bundesliga", "Prediction": "Home", "Odds": 1.85, "ml_value": 0.15},
    {"Match": "Marseille vs Rennes", "League": "Ligue1", "Prediction": "Draw", "Odds": 3.0, "ml_value": 0.11},
    {"Match": "Liverpool vs Chelsea", "League": "EPL", "Prediction": "Draw", "Odds": 3.1, "ml_value": 0.12},
])

# 고적중 전략 (Top 4 ml_value)
top4 = matches.sort_values("ml_value", ascending=False).head(4).reset_index(drop=True)
top4_odds = round(np.prod(top4["Odds"]), 2)
top4_return = round(top4_odds * 1000)

# 4폴 전략 조합 (ml_value ≥ 0.13 중 무작위 4개)
pick4 = matches[matches["ml_value"] >= 0.13].sample(4, random_state=1).reset_index(drop=True)
pick4_odds = round(np.prod(pick4["Odds"]), 2)
pick4_return = round(pick4_odds * 1000)

# 10폴 전략 조합 (ml_value ≥ 0.11 전체 사용)
pick10 = matches[matches["ml_value"] >= 0.11].reset_index(drop=True)
pick10_odds = round(np.prod(pick10["Odds"]), 2)
pick10_return = round(pick10_odds * 1000)

# 수동 결과 입력
result_options = ["", "Home", "Draw", "Away"]
user_results = []
st.markdown("### 수동 결과 입력")
for i, row in matches.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"{row['Match']} ({row['Prediction']} @ {row['Odds']})")
    with col2:
        result = st.selectbox(f"결과 입력", result_options, key=f"res_{i}")
        user_results.append(result)

matches["Result"] = user_results
matches["Hit"] = matches["Prediction"] == matches["Result"]
matches["ROI"] = matches.apply(lambda x: round((x["Odds"] - 1) if x["Hit"] else -1, 2) if x["Result"] else None, axis=1)

# 출력
st.markdown("## ✅ 고적중 전략 (Top 4)")
st.dataframe(top4)
st.markdown(f"**배당 합계:** {top4_odds} / 예상 수익: {top4_return}원")

st.markdown("## ✅ 4폴 전략 조합 (수익 중심)")
st.dataframe(pick4)
st.markdown(f"**배당 합계:** {pick4_odds} / 예상 수익: {pick4_return}원")

st.markdown("## ✅ 10폴 전략 조합 (재미 전략)")
st.dataframe(pick10)
st.markdown(f"**배당 합계:** {pick10_odds} / 예상 수익: {pick10_return}원")

st.markdown("## ✅ 전체 결과 & ROI")
st.dataframe(matches[["Match", "Prediction", "Result", "Hit", "Odds", "ROI"]].dropna())
