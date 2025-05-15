
import streamlit as st
import pandas as pd

st.set_page_config(page_title="축구 베팅 모델 v1.0", layout="wide")
st.title("⚽ 실전 예측 모델 v1.0")

uploaded_file = st.file_uploader("📂 경기 일정 파일 업로드 (.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 업로드된 경기")
    st.dataframe(df)

    def simulate_probabilities(row):
        base = 0.3
        home_score = base + 0.1 * row.get("elo_diff", 0) + 0.05 * row.get("form_diff", 0)
        draw_score = base + 0.01 * (row.get("motivation_factor", 0))
        away_score = base + 0.1 * (-row.get("elo_diff", 0)) + 0.05 * (-row.get("form_diff", 0))
        total = home_score + draw_score + away_score
        return home_score/total, draw_score/total, away_score/total

    def generate_odds(prob):
        margin = 1.05
        return round(margin / prob, 2)

    def calculate_value(prob, odd):
        return round(odd * prob - 1, 3)

    home_probs, draw_probs, away_probs = [], [], []
    odds_home, odds_draw, odds_away = [], [], []
    values, preds = [], []

    for _, row in df.iterrows():
        hp, dp, ap = simulate_probabilities(row)
        oh, od, oa = generate_odds(hp), generate_odds(dp), generate_odds(ap)
        vh, vd, va = calculate_value(hp, oh), calculate_value(dp, od), calculate_value(ap, oa)

        best = max([(vh, "Home", oh), (vd, "Draw", od), (va, "Away", oa)], key=lambda x: x[0])

        home_probs.append(round(hp, 2))
        draw_probs.append(round(dp, 2))
        away_probs.append(round(ap, 2))
        odds_home.append(oh)
        odds_draw.append(od)
        odds_away.append(oa)
        values.append(best[0])
        preds.append(best[1])

    df["home_prob"] = home_probs
    df["draw_prob"] = draw_probs
    df["away_prob"] = away_probs
    df["odds_home"] = odds_home
    df["odds_draw"] = odds_draw
    df["odds_away"] = odds_away
    df["value"] = values
    df["prediction"] = preds

    st.subheader("🔮 예측 결과")
    st.dataframe(df)

    st.subheader("💡 조합 추천")
    combo_df = df[df["value"] > 0]
    st.markdown("**✅ 4폴 추천:**")
    st.dataframe(combo_df.head(4)[["Home", "Away", "prediction", "value"]])
    st.markdown("**✅ 10폴 추천:**")
    st.dataframe(combo_df.head(10)[["Home", "Away", "prediction", "value"]])
    st.markdown("**🔥 고적중 전략 조합:**")
    st.dataframe(combo_df.sort_values(by="value", ascending=False).head(5)[["Home", "Away", "prediction", "value"]])

    st.subheader("📝 결과 입력")
    df["Result"] = [st.selectbox(f"{row['Home']} vs {row['Away']}", ["미입력", "Home", "Draw", "Away"], key=i) for i, row in df.iterrows()]
    df["ROI"] = df.apply(lambda x: 1 if x["prediction"] == x["Result"] else -1 if x["Result"] != "미입력" else 0, axis=1)

    st.subheader("💰 ROI 요약")
    st.write(f"**총 ROI:** {df[df['Result'] != '미입력']['ROI'].sum()}")
    st.dataframe(df[["Home", "Away", "prediction", "value", "Result", "ROI"]])
