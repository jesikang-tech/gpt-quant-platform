# GPT Quant Platform

한국 ETF를 대상으로 가격 데이터 수집, 다중 팩터 분석, 랭킹, 시장 국면 판단, AI 의사결정, 포트폴리오 분석 및 Historical Replay를 제공하는 Flask 기반 퀀트 분석 플랫폼입니다.

## 주요 기능

- 한국 ETF 가격 데이터 수집 및 증분 업데이트
- 수익률, 추세, 기울기 기반 ETF 다중 팩터 분석 및 랭킹
- 20 / 40 / 60 거래일 분석 구간 지원
- Historical Replay를 통한 과거 시점 기준 분석
- Market Regime 및 Market Strategy 분석
- AI Decision 및 설명 가능성 분석
- Portfolio 구성, 설명, Rebalance, Optimization 및 Analytics
- Decision Outcome, Learning Summary 및 Audit Lifecycle 추적
- Adaptive Strategy, Performance, Reliability 및 Statistics 분석
- 한국어 / 영어 대시보드

## 데이터 수집

기본 가격 수집 경로: IncrementalPriceUpdater -> PriceCollector -> FDRProvider -> FinanceDataReader

프로젝트에는 pykrx 기반 수집 모듈도 포함되어 있습니다.

## 실행 환경

현재 검증 환경:

- Windows
- Python 3.13.14
- Flask 3.1.3
- pandas 2.3.3
- scikit-learn 1.7.2
- FinanceDataReader 0.9.202
- pykrx 1.2.8

전체 Python 의존성은 requirements.txt에서 관리합니다.

## 기본 실행

데이터베이스 초기화:

    .\.venv\Scripts\python.exe .\init_db.py

ETF 정보 갱신, 가격 데이터 증분 수집, 배치 분석 및 랭킹 리포트 실행:

    .\.venv\Scripts\python.exe .\main.py

Flask 대시보드/API 서버 실행:

    .\.venv\Scripts\python.exe .\api_server.py

기본 개발 서버는 포트 5000을 사용합니다.

## Historical Replay

Historical Replay는 분석일 당시 이용 가능한 가격 데이터만으로 과거 시점의 랭킹을 계산합니다.

- 1m: 20 거래일
- 2m: 40 거래일
- 3m: 60 거래일

미래 성과 데이터는 과거 랭킹 산출 이후 별도의 검증 정보로 처리하며, 과거 시점의 선정 및 랭킹 결과에는 반영하지 않습니다.

## 테스트 및 검증

전체 회귀 테스트:

    .\.venv\Scripts\python.exe -m pytest -q

텍스트 인코딩 검사:

    .\.venv\Scripts\python.exe .\tools\check_text_encoding.py

현재 기준 전체 회귀 테스트는 188 passed입니다.

프로젝트 텍스트는 UTF-8 / LF를 기준으로 관리하며, 신규 텍스트 파일에는 BOM을 추가하지 않습니다.
