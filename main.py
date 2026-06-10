import streamlit as st
import pandas as pd

st.title("🌸🍂 봄·가을 분석 (수정 버전)")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("📊 컬럼 확인:", df.columns)

    # 👉 컬럼 직접 선택하게 (이게 핵심)
    date_col = st.selectbox("날짜 컬럼 선택", df.columns)
    temp_col = st.selectbox("온도 컬럼 선택", df.columns)

    # 날짜 변환
    df[date_col] = pd.to_datetime(df[date_col])

    # 👉 온도 숫자로 변환 (핵심)
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')

    df = df.dropna()

    df["year"] = df[date_col].dt.year

    # 👉 범위 확인용 출력
    st.write("온도 범위:", df[temp_col].min(), "~", df[temp_col].max())

    # 조건
    spring = df[(df[temp_col] >= 10) & (df[temp_col] <= 20) & (df[date_col].dt.month <= 6)]
    autumn = df[(df[temp_col] >= 10) & (df[temp_col] <= 20) & (df[date_col].dt.month >= 7)]

    st.write("봄 데이터 개수:", len(spring))
    st.write("가을 데이터 개수:", len(autumn))

    spring_days = spring.groupby("year").size()
    autumn_days = autumn.groupby("year").size()

    if len(spring_days) > 0:
        st.subheader("🌸 봄 기간 변화")
        st.line_chart(spring_days)
    else:
        st.error("❌ 봄 데이터 없음 → 온도 조건 확인 필요")

    if len(autumn_days) > 0:
        st.subheader("🍂 가을 기간 변화")
        st.line_chart(autumn_days)
    else:
        st.error("❌ 가을 데이터 없음 → 온도 조건 확인 필요")
