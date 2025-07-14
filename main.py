import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="연도별 나이별 단백질 섭취량 비교", layout="wide")

st.title("🥩 연도별 나이별 단백질 섭취량 비교 웹앱")

# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요.", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    st.subheader("데이터 미리보기")
    st.write(df.head())
    
    # 컬럼명 확인
    st.write("컬럼 리스트:", df.columns.tolist())
    
    # 연도, 나이대 컬럼명을 확인 후 변수 지정
    # 예시로 '구분', '연령(세)', '섭취량(g)' 컬럼명이라고 가정
    year_col = '구분'
    age_col = '연령(세)'
    protein_col = '섭취량(g)'
    
    years = df[year_col].unique()
    ages = df[age_col].unique()
    
    # 사이드바 필터
    st.sidebar.header("🔎 필터")
    selected_years = st.sidebar.multiselect("비교할 연도를 선택하세요", options=years, default=years)
    selected_ages = st.sidebar.multiselect("나이대를 선택하세요", options=ages, default=ages)
    
    # 필터링
    filtered_df = df[(df[year_col].isin(selected_years)) & (df[age_col].isin(selected_ages))]
    
    # 그룹별 평균 계산
    group_df = filtered_df.groupby([year_col, age_col])[protein_col].mean().reset_index()
    
    # Bar Chart
    st.subheader("📊 연도별 나이대별 평균 단백질 섭취량")
    fig = px.bar(group_df, x=year_col, y=protein_col, color=age_col, barmode="group", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Line Chart (전체 평균)
    st.subheader("📈 연도별 전체 평균 단백질 섭취량 추이")
    mean_df = filtered_df.groupby(year_col)[protein_col].mean().reset_index()
    fig2 = px.line(mean_df, x=year_col, y=protein_col, markers=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Boxplot
    st.subheader("🗃️ 연도별 단백질 섭취량 분포")
    fig3 = px.box(filtered_df, x=year_col, y=protein_col, color=age_col)
    st.plotly_chart(fig3, use_container_width=True)
    
    # 증감률 계산
    st.subheader("📈 연도별 평균 단백질 섭취량 증감률")
    mean_df['증감률(%)'] = mean_df[protein_col].pct_change() * 100
    st.write(mean_df)
    
    # 다운로드 버튼
    st.download_button("⬇️ 결과 CSV 다운로드", data=group_df.to_csv(index=False).encode('utf-8-sig'),
                       file_name="단백질섭취량_연도별나이별.csv", mime="text/csv")
else:
    st.info("👆 엑셀 파일을 업로드하면 분석 결과가 표시됩니다.")
