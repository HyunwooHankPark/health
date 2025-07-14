import streamlit as st
import pandas as pd
import plotly.express as px

# 앱 제목
st.set_page_config(page_title="단백질 섭취량 분석", layout="wide")
st.title("🥩 연도별・나이대별 단백질 섭취량 비교")

# CSV 또는 Excel 업로드
uploaded_file = st.file_uploader("단백질 섭취량 데이터 파일 업로드 (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    # 엑셀 또는 CSV 처리
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    
    st.success("✅ 데이터 불러오기 완료!")
    
    # 컬럼명 확인
    st.write("컬럼명:", df.columns.tolist())
    
    # 필터용 변수
    years = sorted(df["연도"].unique())
    age_groups = df["나이대"].unique().tolist()
    
    # 필터 설정
    st.sidebar.header("📊 필터 선택")
    selected_years = st.sidebar.multiselect("연도 선택", years, default=years)
    selected_ages = st.sidebar.multiselect("나이대 선택", age_groups, default=age_groups)
    
    # 필터링
    filtered_df = df[(df["연도"].isin(selected_years)) & (df["나이대"].isin(selected_ages))]
    
    # 데이터 미리보기
    with st.expander("🔍 필터링된 데이터 보기"):
        st.dataframe(filtered_df)
    
    # 그래프: 연도별 평균 단백질 섭취량 추이 (선형 그래프)
    st.subheader("📈 연도별 평균 단백질 섭취량 추이")
    line_df = filtered_df.groupby("연도")["단백질섭취량(g)"].mean().reset_index()
    fig1 = px.line(line_df, x="연도", y="단백질섭취량(g)", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # 그래프: 나이대별 막대 그래프
    st.subheader("📊 나이대별 단백질 섭취량 (연도별 비교)")
    fig2 = px.bar(filtered_df, x="연도", y="단백질섭취량(g)", color="나이대", barmode="group", text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

    # 박스플롯: 분포 확인
    st.subheader("📦 연도별 섭취량 분포 (Boxplot)")
    fig3 = px.box(filtered_df, x="연도", y="단백질섭취량(g)", color="나이대")
    st.plotly_chart(fig3, use_container_width=True)

    # CSV 다운로드
    csv = filtered_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ 이 결과 다운로드 (CSV)", data=csv, file_name="단백질섭취량_분석결과.csv", mime="text/csv")
    
else:
    st.info("👆 위에 데이터를 업로드하면 분석 결과가 여기에 표시됩니다.")
