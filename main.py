import streamlit as st
import pandas as pd

st.title("🌸🍂 봄·가을은 점점 짧아지고 있는가? (완성본)")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 데이터 확인")
    st.write(df.head())

    # ✅ 컬럼 지정 (네 파일 기준)
    date_col = "날짜"
    temp_col = "평균기온(℃)"

    # ✅ 날짜 정리 (핵심!!!)
    df[date_col] = df[date_col].astype(str).str.strip()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # ✅ 온도 숫자 변환
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')

    # 결측 제거
    df = df.dropna()

    # 연도 추출
    df["year"] = df[date_col].dt.year

    # 🌸 봄 (1~6월, 10~20도)
    spring = df[
        (df[temp_col] >= 10) &
        (df[temp_col] <= 20) &
        (df[date_col].dt.month <= 6)
    ]

    # 🍂 가을 (7~12월, 10~20도)
    autumn = df[
        (df[temp_col] >= 10) &
        (df[temp_col] <= 20) &
        (df[date_col].dt.month >= 7)
    ]

    # 연도별 일수
    spring_days = spring.groupby("year").size()
    autumn_days = autumn.groupby("year").size()

    # 그래프
    st.subheader("🌸 봄 기간 변화")
    st.line_chart(spring_days)

    st.subheader("🍂 가을 기간 변화")
    st.line_chart(autumn_days)

    # 📉 회귀분석
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
    st.write(f"봄 기울기: {round(spring_slope, 4)}")
    st.write(f"가을 기울기: {round(autumn_slope, 4)}")

    # 평균 비교
    mid_year = int(df["year"].mean())

    spring_old = spring_days[spring_days.index < mid_year]
    spring_new = spring_days[spring_days.index >= mid_year]

    autumn_old = autumn_days[autumn_days.index < mid_year]
    autumn_new = autumn_days[autumn_days.index >= mid_year]

    st.subheader("📊 평균 비교")
    st.write("봄:", round(spring_old.mean(),2), "→", round(spring_new.mean(),2))
    st.write("가을:", round(autumn_old.mean(),2), "→", round(autumn_new.mean(),2))

    # 결론
    st.subheader("📌 결론")

    if spring_slope < 0 and autumn_slope < 0:
        st.success("👉 봄과 가을이 점점 짧아지고 있음 (통계적으로 확인)")
    elif spring_slope < 0 or autumn_slope < 0:
        st.warning("👉 일부 계절에서 짧아지는 경향 있음")
    else:
        st.error("👉 뚜렷한 감소 경향 없음")
