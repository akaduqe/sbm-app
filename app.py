
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Soccer Betting Model v5.5", layout="wide")
st.title("Soccer Betting Model v5.5")
st.subheader("실전 경기 자동 수집 + 예측 + 결과 반영")

# Sofascore 기반 오늘 경기 (예시: 라리가 3경기 수동 정의)
matches = pd.DataFrame([
    {"Match": "Girona vs Villarreal", "League": "LaLiga", "Prediction": "Home", "Odds": 2.05, "ml_value": 0.16},
    {"Match": "Valencia vs Rayo Vallecano", "League": "LaLiga", "Prediction": "Draw", "Odds": 3.10, "ml_value": 0.14},
    {"Match": "Almeria vs Barcelona", "League": "LaLiga", "Prediction": "Away", "Odds": 1.55, "ml_value": 0.18},
])

# 수동 결과 입력
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
    lambda x: round((x["Odds"] - 1) if x["Hit"] else -1, 2) if x["Result"] else None,
    axis=1
)

# 고적중 전략 조합
top_picks = matches.sort_values("ml_value", ascending=False).head(4).reset_index(drop=True)
top_picks["Result"] = top_picks["Result"].fillna("")
combo_valid = all(res != "" for res in top_picks["Result"])
combo_hit = all(top_picks["Prediction"] == top_picks["Result"]) if combo_valid else None
combo_odds = round(np.prod(top_picks["Odds"]), 2)
combo_roi = round((combo_odds - 1), 2) if combo_hit else (-1 if combo_valid else None)

st.markdown("## ✅ 고적중 전략 조합")
st.dataframe(top_picks)
if combo_hit is True:
    st.success(f"적중 성공! ROI: +{combo_roi}")
elif combo_hit is False:
    st.error("적중 실패. ROI: -1")
else:
    st.warning("결과 입력 대기 중...")

# 전체 결과
st.markdown("## ✅ 전체 경기 결과 및 ROI")
st.dataframe(matches[["Match", "Prediction", "Result", "Hit", "Odds", "ROI"]])
