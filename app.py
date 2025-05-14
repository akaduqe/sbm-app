
import streamlit as st
import pandas as pd

st.title("축구 베팅 모델 v6.5 - 실전 경기 연동 테스트")

uploaded_file = st.file_uploader("경기 일정 CSV 파일 업로드", type="csv")

if uploaded_file is not None:
    matches = pd.read_csv(uploaded_file)

    # 간이 예측 생성 (없을 경우 대비)
    if 'Prediction' not in matches.columns:
        matches['Prediction'] = ['승'] * len(matches)

    st.markdown("### 예측 및 결과 입력")

    for i, row in matches.iterrows():
        st.write(f"{row['Date']} [{row['League']}] {row['Home']} vs {row['Away']}")
        if 'Prediction' in row:
            st.write(f"예측: {row['Prediction']} | 결과 입력: {row.get('Result', '-')}")
        else:
            st.write("예측 준비 중... | 결과 입력: -")
