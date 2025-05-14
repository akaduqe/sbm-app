
import streamlit as st
import pandas as pd

st.set_page_config(page_title="축구 베팅 모델 v7.0", layout="wide")
st.title("⚽ 실전 예측 모델 v7.0")

uploaded_file = st.file_uploader("📂 경기 일정 파일 업로드 (.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 업로드된 경기")
    st.dataframe(df)

    # 예측 로직: 간단한 value 계산 시뮬레이션
    def calc_value(row):
        home_prob = 0.4
        draw_prob = 0.3
        away_prob = 0.3
        odds_home = 2.2
        odds_draw = 3.1
        odds_away = 3.0

        values = {
            "Home": odds_home * home_prob - 1,
            "Draw": odds_draw * draw_prob - 1,
            "Away": odds_away * away_prob - 1,
        }
        best_pick = max(values, key=values.get)
        return best_pick, values[best_pick]

    df[["Prediction", "Value"]] = df.apply(lambda row: pd.Series(calc_value(row)), axis=1)

    st.subheader("🔮 예측 결과 (value 기반)")
    st.dataframe(df)

    # 조합 추천
    st.subheader("💡 조합 추천 (4폴 / 10폴 / 고적중)")
    value_filtered = df[df["Value"] > 0]
    fourfold = value_filtered.head(4)
    tenfold = value_filtered.head(10)
    best_combo = value_filtered.sort_values(by="Value", ascending=False).head(5)

    st.markdown("**✅ 4폴 추천:**")
    st.dataframe(fourfold[["Home", "Away", "Prediction", "Value"]])

    st.markdown("**✅ 10폴 추천:**")
    st.dataframe(tenfold[["Home", "Away", "Prediction", "Value"]])

    st.markdown("**🔥 고적중 전략 조합:**")
    st.dataframe(best_combo[["Home", "Away", "Prediction", "Value"]])

    # 결과 입력
    st.subheader("📝 결과 입력")
    result_inputs = []
    for i, row in df.iterrows():
        result = st.selectbox(f"{row['Home']} vs {row['Away']}", ["미입력", "Home", "Draw", "Away"], key=f"result_{i}")
        result_inputs.append(result)
    df["Result"] = result_inputs

    # ROI 계산
    def calc_roi(pred, actual):
        return 1 if pred == actual else -1

    df["ROI"] = df.apply(lambda x: calc_roi(x["Prediction"], x["Result"]) if x["Result"] != "미입력" else 0, axis=1)
    total_roi = df[df["Result"] != "미입력"]["ROI"].sum()
    st.markdown(f"**💰 총 ROI: {total_roi}**")

    st.subheader("📈 최종 결과")
    st.dataframe(df[["Home", "Away", "Prediction", "Value", "Result", "ROI"]])
