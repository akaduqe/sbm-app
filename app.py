
import streamlit as st
import pandas as pd

st.set_page_config(page_title="축구 베팅 모델 v7.1", layout="wide")
st.title("⚽ 실전 예측 모델 v7.1")

uploaded_file = st.file_uploader("📂 경기 일정 파일 업로드 (.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 업로드된 경기")
    st.dataframe(df)

    # 예측 변수: recent_form_diff, elo_diff, player_rating, rotation_risk, motivation_factor, VAR_bias, market_sentiment
    def simulate_probabilities(row):
        base = 0.3
        home_score = base + 0.1 * (row.get("recent_form_diff", 0)) + 0.05 * (row.get("elo_diff", 0)) + 0.02 * (row.get("player_rating", 0))
        draw_score = base + 0.01 * (row.get("VAR_bias", 0)) - 0.01 * abs(row.get("elo_diff", 0))
        away_score = base + 0.1 * (-row.get("recent_form_diff", 0)) + 0.05 * (-row.get("elo_diff", 0)) + 0.02 * (row.get("rotation_risk", 0))
        total = home_score + draw_score + away_score
        return home_score/total, draw_score/total, away_score/total

    # 배당 예시 (임시)
    def simulate_odds(row):
        return 2.1, 3.3, 3.4

    def calculate_value(prob, odd):
        return odd * prob - 1

    predictions = []
    values = []

    for _, row in df.iterrows():
        home_prob, draw_prob, away_prob = simulate_probabilities(row)
        odds_home, odds_draw, odds_away = simulate_odds(row)

        value_home = calculate_value(home_prob, odds_home)
        value_draw = calculate_value(draw_prob, odds_draw)
        value_away = calculate_value(away_prob, odds_away)

        best = max([(value_home, "Home"), (value_draw, "Draw"), (value_away, "Away")], key=lambda x: x[0])
        predictions.append(best[1])
        values.append(round(best[0], 3))

    df["Prediction"] = predictions
    df["Value"] = values

    st.subheader("🔮 예측 결과 (value 기반)")
    st.dataframe(df)

    # 조합 추천
    st.subheader("💡 조합 추천")
    filtered = df[df["Value"] > 0]
    st.markdown("**✅ 4폴 추천:**")
    st.dataframe(filtered.head(4)[["Home", "Away", "Prediction", "Value"]])
    st.markdown("**✅ 10폴 추천:**")
    st.dataframe(filtered.head(10)[["Home", "Away", "Prediction", "Value"]])
    st.markdown("**🔥 고적중 전략 조합:**")
    st.dataframe(filtered.sort_values(by="Value", ascending=False).head(5)[["Home", "Away", "Prediction", "Value"]])

    # 결과 입력
    st.subheader("📝 결과 입력")
    df["Result"] = [st.selectbox(f"{row['Home']} vs {row['Away']}", ["미입력", "Home", "Draw", "Away"], key=i) for i, row in df.iterrows()]
    df["ROI"] = df.apply(lambda x: 1 if x["Prediction"] == x["Result"] else -1 if x["Result"] != "미입력" else 0, axis=1)

    st.subheader("💰 ROI 계산 결과")
    total_roi = df[df["Result"] != "미입력"]["ROI"].sum()
    st.write(f"**총 ROI:** {total_roi}")
    st.dataframe(df[["Home", "Away", "Prediction", "Value", "Result", "ROI"]])
