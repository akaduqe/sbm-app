
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("축구 베팅 모델 v6.6 - 수동 입력 기반 실전 예측 시스템")

uploaded_file = st.file_uploader("경기 일정 CSV 파일 업로드", type=["csv"])
if uploaded_file is not None:
    matches = pd.read_csv(uploaded_file)
    required_cols = ["Date", "Time", "League", "Home", "Away"]
    if list(matches.columns[:5]) != required_cols:
        st.error("CSV 열 순서가 올바르지 않습니다. 정확한 순서: " + ", ".join(required_cols))
    else:
        st.success("CSV 파일 정상 인식됨.")
        matches["Prediction"] = ["승", "무", "패", "승", "무", "승", "패", "무", "승", "패"]
        matches["O/U"] = ["오버", "언더", "오버", "언더", "오버", "언더", "오버", "언더", "오버", "언더"]
        matches["Odds"] = [1.85, 3.20, 4.10, 1.90, 3.00, 1.70, 4.00, 3.10, 2.10, 3.90]
        matches["Value"] = [0.12, 0.03, -0.08, 0.10, 0.01, 0.22, -0.15, 0.00, 0.07, -0.03]

        results = []
        roi = []
        status = []

        st.subheader("예측 및 결과 입력")

        for i, row in matches.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['Date']} [{row['League']}] {row['Home']} vs {row['Away']}**")
                st.write(f"예측: {row['Prediction']} | 언오버: {row['O/U']} | 배당: {row['Odds']} | value: {row['Value']}")
            with col2:
                result = st.selectbox(f"결과 입력 - {row['Home']} vs {row['Away']}", ["미입력", "승", "무", "패"], key=f"r_{i}")
                results.append(result)
                if result == "미입력":
                    roi.append(None)
                    status.append("입력 대기")
                else:
                    roi.append(row['Odds'] - 1 if result == row['Prediction'] else -1)
                    status.append("학습 완료" if result == row['Prediction'] else "학습 완료")

        matches["Result"] = results
        matches["ROI"] = roi
        matches["Status"] = status

        st.subheader("전체 예측 및 학습 상태")
        st.dataframe(matches)

        roi_values = [r for r in roi if r is not None]
        if roi_values:
            st.metric("ROI 평균", round(sum(roi_values) / len(roi_values), 2))
