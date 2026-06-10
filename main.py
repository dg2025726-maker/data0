import streamlit as st
import pandas as pd

st.title("🌸🍂 봄·가을은 점점 짧아지고 있는가?")
st.write("기온 데이터를 기반으로 계절 길이 변화를 통계적으로 분석합니다.")

# ✔ 파일 이름 그대로 사용
file_path = "ta_20260601093156(1).csv"

# 데이터 불러오기
df = pd.read_csv(file_path)

# 데이터 확인
st.subheader("📊 원본 데이터")
st.write(df.head())

# 👉 컬럼 자동 추정 (보통 이런 형태일 가능성 높음)
# 날짜 / 평균기온
date_col = df.columns[0]
temp_col = df.columns[1]

# 날짜 변환
df[date_col] = pd.to_datetime(df[date_col])
df["year"] = df[date_col].dt.year

# ✔ 봄/가을 조건 (10~20도)
season_df = df[(df[temp_col] >= 10) & (df[temp_col] <= 20)]

# 연도별 일수 계산
season_days = season_df.groupby("year").size()

st.subheader("📈 연도별 봄·가을 일수")
st.line_chart(season_days)

# 평균 비교
st.subheader("📉 평균 변화 분석")

first_half = season_days[season_days.index < season_days.index.mean()]
second_half = season_days[season_days.index >= season_days.index.mean()]

st.write("과거 평균:", round(first_half.mean(), 2))
st.write("최근 평균:", round(second_half.mean(), 2))

# 결론 자동 출력
st.subheader("📌 결론")

if second_half.mean() < first_half.mean():
    st.success("👉 최근으로 갈수록 봄·가을 기간이 짧아지는 경향이 확인됩니다.")
else:
    st.warning("👉 뚜렷한 감소 경향이 확인되지 않습니다.")
