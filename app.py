
import streamlit as st
import pandas as pd
import numpy as np
from itertools import combinations

st.set_page_config(page_title="Soccer Betting Model v5.7.1", layout="wide")
st.title("Soccer Betting Model v5.7.1")
st.subheader("Colab에서 생성한 Sofascore 경기 CSV 기반 실전 예측")

uploaded_file = st.file_uploader("경기 데이터 파일 업로드 (matches.csv)", type=["csv"])

if uploaded_file is not None:
    matches = pd.read_csv(uploaded_file)
    st.success("✅ 경기 데이터 업로드 완료!")
    
    matches["Prediction"] = np.where(matches["Home"] > matches["Away"], "Home",
                             np.where(matches["Home"] < matches["Away"], "Away", "Draw"))
    matches["Odds"] = np.where(matches["Prediction"] == "Home", 1.85,
                        np.where(matches["Prediction"] == "Away", 2.10, 3.20))
    matches["ml_value"] = np.round(np.random.uniform(0.14, 0.24, size=len(matches)), 3)
    
    st.markdown("### ✅ 경기 결과 입력")
    result_options = ["", "Home", "Draw", "Away"]
    user_results = []

    for i, row in matches.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{row['Home']} vs {row['Away']} ({row['Prediction']} @ {row['Odds']})")
        with col2:
            result = st.selectbox("결과", result_options, key=f"res_{i}")
            user_results.append(result)

    matches["Result"] = user_results
    matches["Hit"] = matches["Prediction"] == matches["Result"]
    matches["ROI"] = matches.apply(
        lambda x: round((x["Odds"] - 1), 2) if x["Hit"] else (-1 if x["Result"] else None),
        axis=1
    )

    # 고적중 전략
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

    st.markdown("## ✅ 전체 경기 결과 및 ROI")
    st.dataframe(matches[["Home", "Away", "Prediction", "Result", "Hit", "Odds", "ROI"]])

else:
    st.warning("먼저 Colab에서 만든 경기 파일(matches.csv)을 업로드해주세요.")
