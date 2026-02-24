import os 
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.prompts import ChatPromptTemplate
from app.config import MODEL_NAME, SYSTEM_PROMPT

load_dotenv()

def scan_company_risk(company_name):
    """특정 기업의 최근 악재를 웹에서 검색하고 리스크 수준을 평가"""
    
    # LLM 및 검색 도구 초기화
    llm = ChatOpenAI(model=MODEL_NAME, reasoning_effort="low")
    search_tool = DuckDuckGoSearchRun()

    # 리스크 탐지용 타겟팅 검색 쿼리 구성
    # 단순 기업명뿐 아니라 부정적 키워드를 조합하여 검색 효율 극대화
    search_query = f'"{company_name}" (횡령 OR 배임 OR 소송 OR 상장폐지 OR 적자 OR 압수수색 OR 논란 OR 부도)'

    try:
        search_results = search_tool.invoke(search_query)
    except Exception as e:
        return {"error": f"검색 중 오류 발생: {str(e)}", "raw": ""}

    # 검색 결과가 너무 짧거나 의미 없으면 조기 종료 가능하지만,
    # LLM이 직접 'Low Risk'로 판별하게 넘김.

    # LLM 리스크 분석
    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"""
        [대상 기업]
        {company_name}
        
        [최신 뉴스 및 웹 검색 결과]
        {search_results}
        """)
    ])

    chain = analysis_prompt | llm
    result_text = chain.invoke({}).content

    # JSON 파싱
    try:
        parsed_result = json.loads(result_text)
        parsed_result["company"] = company_name # 결과 객체에 기업명 주입
        return parsed_result
    except:
        return {"error": "리스크 분석 결과 파싱 실패", "raw": result_text, "company": company_name}