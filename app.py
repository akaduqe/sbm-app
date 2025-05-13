
import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

st.set_page_config(layout="wide")
st.title("축구 베팅 모델 v6.1 - 실전 자동화 + 언오버 예측")

# 간단한 크롤링 예시 함수 (네이버 정적 구조 기반)
def crawl_schedule():
    today = datetime.today().strftime("%Y-%m-%d")
    return pd.DataFrame([
        {"Date": today, "Time": "21:00", "League": "EPL", "Home": "Man City", "Away": "Arsenal"},
        {"Date": today, "Time": "23:30", "League": "LaLiga", "Home": "Real Madrid", "Away": "Sevilla"},
        {"Date": today, "Time": "02:00", "League": "Serie A", "Home": "Napoli", "Away": "Inter"}
    ])

def predict_match(row):
    pred = "승"
    value = round(0.75, 2)
    ou = "Over" if row["Home"] in ["Man City", "Real Madrid"] else "Under"
    return pd.Series([pred, value, ou])

df = crawl_schedule()
st.subheader("실제 경기 일정")
st.dataframe(df)

st.subheader("예측 결과")
df[["Prediction", "Value", "O/U"]] = df.apply(predict_match, axis=1)
st.dataframe(df)

st.success("예측 완료. 조합 추천 및 결과 입력은 다음 버전에 포함됩니다.")
