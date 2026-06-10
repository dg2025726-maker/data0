import streamlit as st
import pandas as pd

st.title("🌸🍂 봄·가을은 점점 짧아지고 있는가? (통계 분석)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 데이터 미리보기")
    st.write(df.head())

    # 컬럼 자동 설정
    date_col = df.columns[0]
    temp_col = df.columns[1]

    df[date_col] = pd.to_datetime(df[date_col])
    df["year"] = df[date_col].dt.year

    # 🌸 봄 (10~20도 상승 구간 느낌)
    spring = df[(df[temp_col] >= 10) & (df[temp_col] <= 20) & (df[date_col].dt.month <= 6)]

    # 🍂 가을 (10~20도 하강 구간 느낌)
    autumn = df[(df[temp_col] >= 10) & (df[temp_col] <= 20) & (df[date_col].dt.month >= 7)]

    spring_days = spring.groupby("year").size()
    autumn_days = autumn.groupby("year").size()

    # 그래프
    st.subheader("🌸 봄 기간 변화")
    st.line_chart(spring_days)

    st.subheader("🍂 가을 기간 변화")
    st.line_chart(autumn_days)

    # 📉 회귀분석 (기울기 계산)
    def get_slope(series):
        x = series.index.values
        y = series.values
        if len(x) < 2:
            return 0
        slope = ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean())**2).sum()
        return slope

    spring_slope = get_slope(spring_days)
    autumn_slope = get_slope(autumn_days)

    st.subheader("📉 회귀분석 결과")

    st.write(f"봄 기울기: {round(spring_slope, 3)}")
    st.write(f"가을 기울기: {round(autumn_slope, 3)}")

    # 평균 비교
    mid_year = int(df["year"].mean())

    spring_old = spring_days[spring_days.index < mid_year]
    spring_new = spring_days[spring_days.index >= mid_year]

    autumn_old = autumn_days[autumn_days.index < mid_year]
    autumn_new = autumn_days[autumn_days.index >= mid_year]

    st.subheader("📊 평균 비교")

    st.write("봄 (과거 vs 최근):", round(spring_old.mean(),2), "→", round(spring_new.mean(),2))
    st.write("가을 (과거 vs 최근):", round(autumn_old.mean(),2), "→", round(autumn_new.mean(),2))

    # 결론
    st.subheader("📌 결론")

    if spring_slope < 0 and autumn_slope < 0:
        st.success("👉 봄과 가을 모두 점점 짧아지는 경향이 통계적으로 확인됩니다.")
    elif spring_slope < 0 or autumn_slope < 0:
        st.warning("👉 일부 계절에서 짧아지는 경향이 확인됩니다.")
    else:
        st.error("👉 계절 길이 감소 경향이 명확하지 않습니다.")
