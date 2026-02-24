# Financial Risk Radar (투자 포트폴리오 리스크 모니터링 솔루션)

## 1. 프로젝트 개요

Financial Risk Radar는 벤처캐피탈(VC), 사모펀드(PEF), 자산운용사 등 전문 투자 기관을 위한 인공지능 기반 리스크 관리 자동화 솔루션입니다.

투자 대상 기업이나 관심 종목에 대해 웹상의 최신 뉴스와 공시 정보를 실시간으로 수집하고, OpenAI의 **gpt-5-mini** 모델을 활용하여 해당 이슈가 기업 가치에 미칠 펀더멘털 손상 여부를 분석합니다. 단순한 키워드 매칭 방식의 뉴스 스크래핑을 넘어, 문맥(Context)을 이해하는 LLM이 리스크 등급(High/Medium/Low)을 산정하고 투자자가 취해야 할 구체적인 대응 조치(Action Plan)를 제안합니다.

### 주요 기능
* **Automated Risk Scanning:** `ddgs`(DuckDuckGo Search) 패키지를 활용하여 포트폴리오 기업들의 최신 악재(횡령, 배임, 소송, 규제 등) 정보를 자동으로 수집.
* **Contextual Analysis:** 수집된 비정형 텍스트 데이터를 **gpt-5-mini**가 분석하여 단순 노이즈와 실질적 리스크를 구분하고, 리스크 유형(법률, 재무, 평판 등)을 분류.
* **Actionable Insight:** "경영진 면담 필요", "지분 매각 검토", "관망" 등 수석 심사역 페르소나에 기반한 전문가 수준의 대응 가이드 제공.
* **Dashboard Visualization:** 다수의 기업을 일괄 스캔하여 위험도별로 시각화된 대시보드(Streamlit) 제공.

## 2. 시스템 아키텍처

본 시스템은 LangChain 프레임워크를 기반으로 검색 에이전트와 분석 엔진이 결합된 파이프라인으로 구성되어 있습니다.

1.  **Target Injection:** 사용자가 모니터링 대상 기업 리스트 입력.
2.  **Web Search (Agent Action):** 각 기업명과 부정적 키워드(횡령, 적자, 논란 등)를 조합하여 `DuckDuckGoSearchRun`을 통해 정밀 검색 수행.
3.  **Reasoning & Evaluation:** 검색된 뉴스 요약본을 **gpt-5-mini** 모델에 주입하여, 시스템 프롬프트에 정의된 리스크 평가 기준에 따라 분석.
4.  **Structured Output:** 분석 결과를 JSON 포맷으로 파싱하여 리스크 등급, 요약, 대응 방안 데이터 생성.
5.  **Rendering:** Streamlit UI를 통해 분석 결과를 사용자에게 리포트 형태로 출력.

## 3. 기술 스택

* **Language:** Python 3.10 이상
* **LLM:** OpenAI **gpt-5-mini**
* **Orchestration:** LangChain
* **Search Tool:** DuckDuckGo Search (`ddgs`)
* **Web Framework:** Streamlit
* **Environment Management:** python-dotenv

## 4. 프로젝트 구조

확장성을 고려하여 설정(Config), 로직(Logic), 프레젠테이션(UI) 계층을 분리한 구조입니다.

```text
risk-radar/
├── .env                  # 환경 변수 설정 (API Key)
├── requirements.txt      # 의존성 패키지 목록
├── main.py               # 애플리케이션 진입점 및 리스크 모니터링 대시보드
└── app/
    ├── __init__.py
    ├── config.py         # 심사역 페르소나, 리스크 평가 프롬프트 및 JSON 스키마
    └── radar.py          # ddgs 검색 로직 및 LLM 기반 리스크 분석 엔진
```

## 5. 설치 및 실행 가이드
### 5.1. 사전 준비
Python 환경이 구성된 상태에서 저장소를 복제하고 프로젝트 디렉토리로 이동하십시오.

```Bash
git clone [레포지토리 주소]
cd risk-radar
```
### 5.2. 의존성 설치
LangChain, 검색 도구 및 데이터 처리 패키지를 설치합니다.

```Bash
pip install -r requirements.txt
```
### 5.3. 환경 변수 설정
프로젝트 루트 경로에 .env 파일을 생성하고 OpenAI API 키를 입력하십시오.

```Ini, TOML
OPENAI_API_KEY=sk-your-api-key-here
```
### 5.4. 실행
Streamlit 애플리케이션을 실행합니다.

```Bash
streamlit run main.py
```
## 6. 출력 데이터 사양 (JSON Schema)
AI 모델의 분석 결과는 다음의 JSON 구조로 반환되어 시스템의 안정적인 UI 렌더링을 지원합니다.

```JSON
{
  "risk_level": "High",
  "risk_type": "법률/Compliance",
  "summary": "대표이사의 자본시장법 위반 혐의로 인한 검찰 소환 조사 진행 중이며, 주가 조작 의혹 확산으로 브랜드 평판 심각한 훼손.",
  "action": "컴플라이언스 위원회 소집 요구 및 투자금 조기 회수(Put Option) 가능성 법률 검토 필요."
}
```
## 7. 면책 조항 (Disclaimer)
본 솔루션이 제공하는 리스크 분석 결과는 웹 검색 데이터와 인공지능의 추론에 기반한 참고 정보입니다. 금융 시장의 모든 변수를 반영하지 못할 수 있으며, 실제 투자 의사결정이나 매수/매도 실행에 대한 법적 책임을 지지 않습니다. 최종적인 투자 판단은 반드시 해당 기업의 공식 공시 자료 확인 및 금융 전문가의 자문을 거쳐 진행하시기 바랍니다.
