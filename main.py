import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드 (예: 정제된 clean_df.csv 파일이 있다고 가정)
@st.cache_data
def load_data():
    df = pd.read_csv("섭취량_clean_data.csv")  # 실제 파일 경로 또는 업로드된 파일로 대체 가능
    df["연도"] = df["연도"].astype(str)
    return df

df = load_data()

# 앱 제목
st.title("연도별 · 연령대별 섭취량 비교 웹앱")

# 연도 및 연령대 필터
years = sorted(df["연도"].unique())
ages = sorted(df["연령대"].dropna().unique())

selected_year = st.selectbox("연도를 선택하세요", years)
selected_age = st.selectbox("연령대를 선택하세요", ages)

# 1. 연령대 고정 → 연도별 섭취량 변화
st.subheader(f"'{selected_age}' 연령대의 연도별 섭취량 변화")
age_df = df[df["연령대"] == selected_age]
fig1 = px.line(age_df, x="연도", y="섭취량(g)", title="연도별 섭취량 변화", markers=True)
st.plotly_chart(fig1)

# 2. 연도 고정 → 연령대별 섭취량 비교
st.subheader(f"{selected_year}년의 연령대별 섭취량 비교")
year_df = df[df["연도"] == selected_year]
fig2 = px.bar(year_df, x="연령대", y="섭취량(g)", title="연령대별 섭취량", text="섭취량(g)")
st.plotly_chart(fig2)

# 3. 데이터 테이블 보기
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(df)

# 4. CSV 다운로드
st.download_button("📥 데이터 다운로드 (CSV)", data=df.to_csv(index=False), file_name="섭취량_데이터.csv")
