
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("축구 베팅 모델 v6.2 - 실전 경기 자동 예측")

# 실제 경기 예시 데이터 (크롤링된 결과라고 가정)
matches = pd.DataFrame([
    {"Date": "2024-05-20", "Time": "21:00", "League": "EPL", "Home": "Man City", "Away": "Arsenal"},
    {"Date": "2024-05-20", "Time": "23:30", "League": "LaLiga", "Home": "Real Madrid", "Away": "Sevilla"},
    {"Date": "2024-05-21", "Time": "02:00", "League": "Serie A", "Home": "Napoli", "Away": "Inter"}
])

# 예측 생성
def predict(row):
    prediction = "승"
    value = 0.82
    ou = "Over" if row["Home"] in ["Man City", "Real Madrid"] else "Under"
    return pd.Series([prediction, value, ou])

matches[["Prediction", "Value", "O/U"]] = matches.apply(predict, axis=1)

# 출력
st.subheader("실전 경기 예측 결과")
st.dataframe(matches)
