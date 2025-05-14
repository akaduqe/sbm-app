
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("축구 베팅 모델 v6.4 - 실전 경기 자동 연동")

# 실전 경기 예시 데이터 (CSV에서 불러왔다고 가정)
matches = pd.DataFrame([
    {"Date": "2024-05-25", "League": "EPL", "Home": "Man City", "Away": "Chelsea", "Prediction": "승", "Value": 0.78, "O/U": "Over", "Odds": 1.95, "is_real_match": True},
    {"Date": "2024-05-25", "League": "LaLiga", "Home": "Barcelona", "Away": "Betis", "Prediction": "무", "Value": 0.69, "O/U": "Under", "Odds": 3.1, "is_real_match": True},
    {"Date": "2024-05-26", "League": "Serie A", "Home": "Juventus", "Away": "AC Milan", "Prediction": "패", "Value": 0.74, "O/U": "Over", "Odds": 2.8, "is_real_match": True},
    {"Date": "2024-05-26", "League": "Bundesliga", "Home": "Leverkusen", "Away": "Bayern", "Prediction": "승", "Value": 0.82, "O/U": "Over", "Odds": 2.2, "is_real_match": True}
])

st.subheader("실전 경기 예측 결과 및 입력")
results = []
roi = []

for i, row in matches.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{row['Date']} [{row['League']}] {row['Home']} vs {row['Away']}**")
        st.write(f"예측: {row['Prediction']} | 언오버: {row['O/U']} | 배당: {row['Odds']} | value: {row['Value']} | 실전경기: {row['is_real_match']}")
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
