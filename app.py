
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("축구 베팅 모델 v6.3 - 예측 + 조합 + 입력 + ROI")

# 경기 예시 데이터
matches = pd.DataFrame([
    {"Date": "2024-05-20", "League": "EPL", "Home": "Man City", "Away": "Arsenal", "Prediction": "승", "Value": 0.81, "O/U": "Over", "Odds": 2.1},
    {"Date": "2024-05-20", "League": "LaLiga", "Home": "Real Madrid", "Away": "Sevilla", "Prediction": "무", "Value": 0.74, "O/U": "Under", "Odds": 3.2},
    {"Date": "2024-05-21", "League": "Serie A", "Home": "Napoli", "Away": "Inter", "Prediction": "패", "Value": 0.65, "O/U": "Under", "Odds": 2.9},
    {"Date": "2024-05-21", "League": "Bundesliga", "Home": "Bayern", "Away": "Dortmund", "Prediction": "승", "Value": 0.87, "O/U": "Over", "Odds": 1.95}
])

st.subheader("경기 예측 결과 및 입력")
results = []
roi = []

for i, row in matches.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"{row['Date']} [{row['League']}] {row['Home']} vs {row['Away']} | 예측: {row['Prediction']} ({row['O/U']}) | 배당: {row['Odds']} | value: {row['Value']}")
    with col2:
        result = st.selectbox(f"결과 입력 - {row['Home']} vs {row['Away']}", ["미입력", "승", "무", "패"], key=f"r_{i}")
        results.append(result)
        roi.append(row['Odds'] - 1 if result == row['Prediction'] else -1)

matches["Result"] = results
matches["ROI"] = roi

st.subheader("입력 결과 및 수익")
st.dataframe(matches)

total_roi = sum([r for r in roi if r != -1])
st.success(f"총 수익률 (입력된 경기 기준): {round(total_roi,2)}")
