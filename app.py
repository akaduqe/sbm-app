
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Soccer Betting AI v5.4", layout="wide")
st.title("Soccer Betting Model v5.4")
st.subheader("실전 전환 준비: 경기 구분, 적중 판정, ROI 계산 강화")

# 예시/실제 경기 구분
matches = pd.DataFrame([
    {"Match": "Man City vs Arsenal", "League": "EPL", "Prediction": "Home", "Odds": 1.95, "ml_value": 0.16, "is_example": False},
    {"Match": "Barcelona vs Sevilla", "League": "LaLiga", "Prediction": "Home", "Odds": 1.80, "ml_value": 0.14, "is_example": False},
    {"Match": "Juventus vs Napoli", "League": "SerieA", "Prediction": "Draw", "Odds": 3.2, "ml_value": 0.15, "is_example": False},
    {"Match": "Dortmund vs Bayern", "League": "Bundesliga", "Prediction": "Away", "Odds": 2.05, "ml_value": 0.13, "is_example": False},
    {"Match": "PSG vs Lyon", "League": "Ligue1", "Prediction": "Home", "Odds": 1.70, "ml_value": 0.18, "is_example": True},
    {"Match": "Atletico vs Betis", "League": "LaLiga", "Prediction": "Home", "Odds": 1.90, "ml_value": 0.12, "is_example": True},
    {"Match": "AC Milan vs Roma", "League": "SerieA", "Prediction": "Home", "Odds": 2.0, "ml_value": 0.14, "is_example": True},
    {"Match": "Leverkusen vs Frankfurt", "League": "Bundesliga", "Prediction": "Home", "Odds": 1.85, "ml_value": 0.15, "is_example": True},
])

# 수동 결과 입력 UI (실제 경기만)
st.markdown("### ✅ 결과 입력 (실제 경기만 가능)")
result_options = ["", "Home", "Draw", "Away"]
user_results = []

for i, row in matches.iterrows():
    label = f"{row['Match']} ({'예시' if row['is_example'] else '실제'}) - {row['Prediction']} @ {row['Odds']}"
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(label)
    with col2:
        if row["is_example"]:
            st.markdown("*입력 불가 (예시 경기)*")
            user_results.append("")
        else:
            result = st.selectbox("결과", result_options, key=f"res_{i}")
            user_results.append(result)

matches["Result"] = user_results
matches["Hit"] = matches["Prediction"] == matches["Result"]
matches["ROI"] = matches.apply(
    lambda x: round((x["Odds"] - 1) if x["Hit"] else -1, 2) if x["Result"] else None,
    axis=1
)

# 고적중 전략 (Top 4 ml_value)
top4 = matches.sort_values("ml_value", ascending=False).head(4).reset_index(drop=True)
top4_hit_status = top4["Hit"].tolist()
top4_result_status = top4["Result"].tolist()
top4_valid = all(res != "" for res in top4_result_status)
top4_success = all(top4_hit_status) if top4_valid else None
top4_odds = round(np.prod(top4["Odds"]), 2)
top4_roi = round((top4_odds - 1), 2) if top4_success else (-1 if top4_valid else None)

st.markdown("## ✅ 고적중 전략")
st.dataframe(top4)
if top4_success is True:
    st.success(f"적중 성공! ROI: +{top4_roi}")
elif top4_success is False:
    st.error("적중 실패. ROI: -1")
else:
    st.warning("결과 입력 대기 중...")

# 전체 결과 요약
st.markdown("## ✅ 전체 경기 결과 및 ROI")
st.dataframe(matches[["Match", "Prediction", "Result", "Hit", "Odds", "ROI", "is_example"]])
