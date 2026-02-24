import streamlit as st
import pandas as pd
from app.radar import scan_company_risk

st.set_page_config(page_title="Financial Risk Radar", layout="wide")

st.title("투자 포트폴리오 리스크 모니터링 에이전트")
st.caption("관심 기업 또는 투자 포트폴리오의 치명적 악재(법률, 재무 등)를 실시간으로 탐지하고 리포팅합니다.")
st.divider()

# --- 사이드바: 타겟 설정 ---
with st.sidebar:
    st.header("모니터링 대상 등록")
    target_input = st.text_area(
        "기업명을 쉼표(,)로 구분하여 입력하세요.",
        value="카카오, 삼성전자, 엔씨소프트",
        height=150
    )

    scan_btn = st.button("전체 리스크 스캔 실행", type="primary", width="stretch")

# --- 메인 영역: 리스크 대시보드 ---
if scan_btn:
    if not target_input.strip():
        st.warning("모니터링할 기업을 입력해주세요.")

    else:
        # 입력받은 기업명 리스트 전처리
        companies = [c.strip() for c in target_input.split(",") if c.strip()]

        st.subheader("리스크 분석 종합 리포트")
        progress_bar = st.progress(0)

        results = []

        # 각 기업별로 순차적 스캔 진행
        for i, company in enumerate(companies):
            with st.spinner(f"'{company}' 리스크 분석 중..."):
                res = scan_company_risk(company)
                results.append(res)

            # 프로그레스 바 업데이트
            progress_bar.progress((i + 1) / len(companies))
        
        st.success("스캔이 완료되었습니다.")
        st.divider()

        # 분석 결과 시각적 렌더링
        for res in results:
            company = res.get("company", "Unknown")

            if "error" in res:
                st.error(f"**{company}**: 분석 중 오류 발생")
                continue

            risk_level = res.get("risk_level", "Low")

            # 리스크 레벨에 따른 UI 컨테이너 색상 및 아이콘 변경

            if risk_level == "High":
                with st.container(border=True):
                    st.error(f"🚨 **[HIGH RISK] {company}**")
                    st.write(f"**유형:** {res.get('risk_type')}")
                    st.write(f"**요약:** {res.get('summary')}")
                    st.info(f"**Action:** {res.get('action')}")
            elif risk_level == "Medium":
                with st.container(border=True):
                    st.warning(f"⚠️ **[MEDIUM RISK] {company}**")
                    st.write(f"**유형:** {res.get('risk_type')}")
                    st.write(f"**요약:** {res.get('summary')}")
                    st.info(f"**Action:** {res.get('action')}")
            else:
                with st.container(border=True):
                    st.success(f"✅ **[LOW RISK / SAFE] {company}**")
                    st.write("치명적인 악재나 리스크가 발견되지 않았습니다.")