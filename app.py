
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Soccer Betting Model v5.7", layout="wide")
st.title("Soccer Betting Model v5.7")
st.subheader("실전 Sofascore 경기 자동 수집 + 조합 + 결과 학습")

# Mocked real matches from Sofascore (this would be dynamic in production)
matches = pd.DataFrame([
    {"Match": "Real Madrid vs Alaves", "League": "LaLiga", "Prediction": "Home", "Odds": 1.65, "ml_value": 0.21},
    {"Match": "Osasuna vs Mallorca", "League": "LaLiga", "Prediction": "Draw", "Odds": 3.30, "ml_value": 0.18},
    {"Match": "Granada vs Celta Vigo", "League": "LaLiga", "Prediction": "Away", "Odds": 2.10, "ml_value": 0.19},
    {"Match": "Inter vs Lazio", "League": "Serie A", "Prediction": "Home", "Odds": 1.85, "ml_value": 0.23},
    {"Match": "Bayern vs Hoffenheim", "League": "Bundesliga", "Prediction": "Home", "Odds": 1.40, "ml_value": 0.17},
])

st.markdown("### ✅ 경기 결과 입력")
result_options = ["", "Home", "Draw", "Away"]
user_results = []

for i, row in matches.iterrows():
    label = f"{row['Match']} ({row['Prediction']} @ {row['Odds']})"
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(label)
    with col2:
        result = st.selectbox("결과 입력", result_options, key=f"res_{i}")
        user_results.append(result)

matches["Result"] = user_results
matches["Hit"] = matches["Prediction"] == matches["Result"]
matches["ROI"] = matches.apply(
    lambda x: round((x["Odds"] - 1), 2) if x["Hit"] else (-1 if x["Result"] else None),
    axis=1
)

# 고적중 전략 조합
from itertools import combinations
best_combo = None
best_score = -1

for combo in combinations(matches.index, 3):
    selected = matches.loc[list(combo)]
    if all(selected["Result"]):
        score = selected["Hit"].sum()
    else:
        score = selected["ml_value"].sum()
    if score > best_score:
        best_score = score
        best_combo = selected

st.markdown("## ✅ 고적중 전략 조합 (단 하나만 추천)")
st.dataframe(best_combo)
if all(best_combo["Result"]):
    if all(best_combo["Hit"]):
        st.success("적중 성공!")
    else:
        st.error("적중 실패.")
else:
    st.warning("결과 입력 대기 중...")

# 전체 경기 결과
st.markdown("## ✅ 전체 경기 결과 및 ROI")
st.dataframe(matches[["Match", "Prediction", "Result", "Hit", "Odds", "ROI"]])
