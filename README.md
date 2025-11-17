# 알라딘 월간 베스트셀러 독서 트렌드 분석 프로젝트

## 프로젝트 개요
2020년 1월부터 2025년 9월까지 알라딘 월간베스트셀러 데이터를 크롤링하여 독서 트렌드 변화를 분석하고, GPT의 예측 결과와 실제 데이터를 비교하는 프로젝트입니다.

---

## 1. 분석할 내용
- 연도별 독서 트렌드 변화: 2020년부터 2025년 베스트셀러 비교 분석
- 카테고리별 인기도 변화: 시기별 인기 장르 변화 확인
- GPT 예측 vs 실제 결과 비교: AI의 예측 정확성 검증

## 2. 사용할 데이터
- 출처: 알라딘 월간 베스트셀러 TOP 50 (2020년 1월 ~ 2025년 11월)
- https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&CID=0&Year=2025&Month=9&Week=1&BestType=MonthlyBest&SearchSubBarcode=
- 수집 방식: BeautifulSoup를 활용한 웹 크롤링
- 데이터 항목: 
  - `year`: 연도
  - `month`: 월
  - `rank`: 순위
  - `category`: 도서 카테고리
  - `title`: 도서명
  - `author`: 작가명
  - `price`: 가격
  - `star_score`: 별점
  - `page_count`: 페이지 수
  - `item_id`: 도서 고유 ID

## 3. 프로젝트 범위
### 데이터 수집·크롤링
- 알라딘 월간 베스트셀러 웹페이지 크롤링 (2020.01 ~ 2025.11)
- BeautifulSoup를 활용한 HTML 파싱
- 도서 정보 추출: 연도, 월, 순위, 도서명, 도서 상위 카테고리, 작가명, 가격, 별점, 페이지 수, 도서 고유 ID
- 도서 정보 추출: 도서 상세 카테고리, 페이지 수, 도서 고유 ID

### 데이터 저장/추출
- 크롤링한 데이터를 CSV 형태로 저장
- 연도별, 월별 데이터 구조화
- 총 71개월간의 알라딘 월간 베스트셀러 데이터 축적

### 데이터 가공/정제
- 2단계 크롤링을 통한 상세 카테고리, 페이지 수 정보 수집
- item_id 기준 데이터 병합
- 상세 카테고리로 교체되지 못한 도서는 상위 카테고리(국내도서) 유지 (교체되지 않음은 크롤링 실패임을 의미)
- 페이지 수 0 제거 (성인 도서·크롤링 실패)
- 최종 데이터: 3,517개 행

### 데이터 분석
- 연도별 베스트셀러 트렌드 변화 분석
- 카테고리별 인기도 변화 추이 분석
- GPT 예측과 실제 데이터 비교 분석

### 데이터 시각화
- 연도별 카테고리 비중 변화 차트
- 주요 카테고리별 점유율 변화 시각화
- GPT 예측 vs 실제 결과 비교 차트

### 분석 결과
- 독서 트렌드 변화의 주요 패턴 도출
- 사회적 요인과 독서 트렌드 연관성 해석
- AI 예측의 정확성과 한계점 평가
- 향후 독서 트렌드 전망 및 시사점

## 4. 생성형 AI 결과 (GPT 예측)

### GPT에게 질문한 내용:
"2020년 1월부터 2025년 11월까지의 알라딘 베스트셀러를 비교하면, 어떤 독서 트렌드 변화가 예상될까?"

### 연속적 트렌드 변화

#### 2020년 ~ 2021년 (코로나 초기·팬데믹 시기)
- 아동도서, 웹툰, 그림책, 라이트노벨 강세
- 위로·힐링형 에세이 수요 증가
- 집콕 문화 확산으로 취미·실용서(요리, 건강 등)도 인기

#### 2022년 ~ 2023년 (포스트 코로나·사회 회복기)
- 에세이·힐링 서적은 감소세, 대신 경제/경영/자기계발 서적 수요 증가
- 불확실한 경제 상황 → 재테크, 자기계발서 강세
- 여전히 웹툰·아동도서는 꾸준히 상위권 유지

#### 2024년 ~ 2025년 (AI 붐·기술 확산 시기)
- AI, 데이터, IT 관련 서적이 새롭게 베스트셀러에 진입
- 자기계발·실무 중심 실용서 판매 확대
- 사회·기술적 이슈(챗GPT, 인공지능 활용)가 독서 주제에 반영

### 종합적인 변화 흐름
- 2020~21: 아동·웹툰·에세이 중심 (코로나 영향)
- 2022~23: 경제·자기계발 비중 확대 (사회 회복 + 경기불안)
- 2024~25: AI·기술 서적 부상, 실용성 강화

---

## 기술 스택
- 언어: Python
- 데이터 수집: BeautifulSoup4, requests
- 데이터 처리: Pandas, NumPy
- 시각화: Matplotlib, Seaborn
- 분석:
- 개발 환경: Google Colab, Google Drive

# 📁 프로젝트 구조
```
📂 aladin-bestseller-analysis/
 ┣ 📂 data/                           # 데이터 파일들
 ┃  ┣ 📂 raw/                         # 원본 크롤링 데이터
 ┃  ┃  ┣ aladin.csv                  # 1차 크롤링 데이터 (3,540개)
 ┃  ┃  ┣ detail_mapping.csv          # 2차 크롤링 데이터 (1,960개)
 ┃  ┃  └ .gitkeep
 ┃  ┣ 📂 processed/                   # 전처리된 데이터
 ┃  ┃  ┣ aladin_final_cleaned.csv    # 최종 정제 데이터 (3,517개)
 ┃  ┃  └ .gitkeep
 ┃  └ 📂 visualizations/              # 시각화 이미지
 ┃     ┣ 00_yearly_comics_children_check.png
 ┃     ┣ 01_yearly_price_trend.png
 ┃     ┣ 02_yearly_page_count.png
 ┃     ┣ 03_category_book_count.png
 ┃     ┣ 04_yearly_category_ratio.png
 ┃     ┣ 05_monthly_category_pattern.png
 ┃     ┣ 06_category_avg_price_top15.png
 ┃     ┣ 07_price_distribution.png
 ┃     ┣ 08_author_bestseller_count.png
 ┃     ┣ 09_category_avg_rank.png
 ┃     ┣ 10_monthly_rank1_books.png
 ┃     ┣ 11_han_kang_vs_total_novels.png
 ┃     ┣ 12_han_kang_before_after.png
 ┃     ┣ 13_han_kang_books_count.png
 ┃     ┣ 14_han_kang_price_comparison.png
 ┃     ┣ 15_han_kang_rating_comparison.png
 ┃     ┣ 📂 references/              # 외부 참고 자료
 ┃     ┃  ┣ 2022_book_price.jpeg # 대한출판문화협회
 ┃     ┃  └ .gitkeep
 ┃     └ .gitkeep
 ┃
 ┣ 📂 notebooks/                      # Colab 노트북 파일들
 ┃  ┣ 01_crawling.ipynb               # 1차 크롤링 (베스트셀러 리스트)
 ┃  ┣ 02_data_preprocessing.ipynb     # 데이터 병합 및 전처리
 ┃  ┣ 03_visualization.ipynb          # 데이터 시각화 (16개)
 ┃  └ .gitkeep
 ┃
 ┣ 📂 outputs/                        # 최종 결과물
 ┃  ┣ final_report.md                 # 최종 보고서
 ┃  └ .gitkeep
 ┃
 ┣ 📜 .gitignore                      # Git 제외 파일 설정
 ┣ 📜 README.md                       # 프로젝트 개요 및 설명
 └ 📜 requirements.txt                # 필요 라이브러리 목록
```

## 분석 결과 활용 가능 분야

### 1. 출판·도서 기획
- 출판사: 향후 유망 장르 및 주제 예측 → 신간 기획 방향 설정
- 작가/에이전트: 독자 선호 장르 분석 → 창작 전략 수립
- 마케팅팀: 시즌별 카테고리별 마케팅 전략 수립

### 2. 서점·온라인 플랫폼
- 추천 시스템 개선: 최근 트렌드 반영
- 프로모션 전략: 시즌별 맞춤 기획전 진행

### 3. 교육·연구
- 사회문화 연구: 독서 트렌드와 사회적 사건의 상관성 분석
- 독서 교육 자료: 시대별 독서 흐름 교육에 활용

### 4. 콘텐츠·미디어
- 블로그/유튜브/리포트: 대중적 관심을 끌 수 있는 콘텐츠 제작
- 언론 기사: "코로나 이후 독서 트렌드 변화" 등 사회적 이슈와 연결
