
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="축구 베팅 모델 v6.6", layout="wide")

st.title("⚽ 실전용 축구 베팅 모델 v6.6")
uploaded_file = st.file_uploader("📂 경기 일정 파일 업로드 (.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 업로드된 경기")
    st.dataframe(df)

    # 예측 생성 (더미 로직)
    def make_prediction(row):
        return random.choice(["Home", "Draw", "Away"])

    df["Prediction"] = df.apply(make_prediction, axis=1)

    st.subheader("🔮 예측 결과")
    st.dataframe(df)

    # 조합 추천 (4폴 / 10폴)
    st.subheader("💡 조합 추천")
    fourfold = df.sample(min(4, len(df)))
    tenfold = df.sample(min(10, len(df)))

    st.markdown("**[4폴 추천]**")
    st.dataframe(fourfold[["Home", "Away", "Prediction"]])

    st.markdown("**[10폴 추천]**")
    st.dataframe(tenfold[["Home", "Away", "Prediction"]])

    # 결과 입력
    st.subheader("📝 결과 입력")
    result_inputs = []
    for i, row in df.iterrows():
        result = st.selectbox(f"{row['Home']} vs {row['Away']}", ["미입력", "Home", "Draw", "Away"], key=f"result_{i}")
        result_inputs.append(result)

    df["Result"] = result_inputs

    # ROI 계산
    st.subheader("💰 ROI 계산 (간이)")
    def roi_calc(pred, actual):
        return 1 if pred == actual else -1

    if "Result" in df.columns:
        df["ROI"] = df.apply(lambda x: roi_calc(x["Prediction"], x["Result"]) if x["Result"] != "미입력" else 0, axis=1)
        total = df[df["Result"] != "미입력"]["ROI"].sum()
        st.markdown(f"**총 ROI:** {total}")

        st.dataframe(df[["Home", "Away", "Prediction", "Result", "ROI"]])
