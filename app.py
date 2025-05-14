
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("축구 베팅 모델 v6.5 - 실전 경기 연동 테스트")

# CSV 파일 업로드
uploaded_file = st.file_uploader("경기 일정 CSV 파일 업로드", type=["csv"])
if uploaded_file is not None:
    matches = pd.read_csv(uploaded_file)
    matches["is_real_match"] = True

    st.subheader("예측 및 결과 입력")
    results = []
    roi = []

    for i, row in matches.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{row['Date']} [{row['League']}] {row['Home']} vs {row['Away']}**")
            st.write(f"예측: {row['Prediction']} | 언오버: {row['O/U']} | 배당: {row['Odds']} | value: {row['Value']}")
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
else:
    st.warning("CSV 파일을 업로드하면 실전 경기 예측이 표시됩니다.")
