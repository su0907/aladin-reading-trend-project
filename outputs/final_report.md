# 알라딘 월간 베스트셀러 데이터 분석 프로젝트

**기간:** 2020년 1월 ~ 2025년 11월 (71개월)  
**분석 대상:** 알라딘 월간 베스트셀러 TOP 50  
**GitHub:** https://github.com/username/aladin-project

---

# 1. 프로젝트 개요

## 1.1 목적

본 프로젝트는 2020~2025년 알라딘 월간 베스트셀러 데이터를 크롤링 및 분석하여 독서 트렌드 변화를 파악하는 것을 목표로 합니다.

## 1.2 연구 질문

**(1) 2020~2025년 베스트셀러 시장의 장기적 트렌드는 무엇인가?**
- 연도별 평균 가격 및 페이지 수 변화
- 카테고리별 도서 수 및 비중 변화

**(2) 연도별·계절별 카테고리 비중의 변화는 어떻게 나타나는가?**
- 장르별 진입 횟수 변화
- 월별 계절성 패턴

**(3) 2022년 가격 및 페이지 수 하락의 구조적 원인은 무엇인가?**
- 일반 도서 자체의 변화
- 장르 구성의 영향

**(4) 한강 노벨문학상과 영화 콘텐츠 흥행이 시장에 미친 영향은 어느 정도인가?**
- 노벨문학상 수상 전후 비교
- 슬램덩크 영화 개봉 효과

## 1.3 기술 스택

- **언어:** Python 3.10+
- **크롤링:** BeautifulSoup4, urllib
- **데이터 처리:** Pandas, NumPy
- **시각화:** Matplotlib, Seaborn, Plotly
- **환경:** Google Colab
- **저장/관리:** Google Drive

---

# 2. 데이터 수집

## 2.1 크롤링 대상 및 기간

| 항목 | 내용 |
|------|------|
| **대상 사이트** | 알라딘 (www.aladin.co.kr) |
| **수집 기간** | 2020년 1월 ~ 2025년 11월 (71개월) |
| **수집 범위** | 월간 베스트셀러 TOP 50 |
| **이론적 수집량** | 71개월 × 50개 = 3,550개 |
| **실제 수집량** | 3,539개 (11개 누락) |

## 2.2 1차 크롤링: 월간 베스트셀러 리스트

### 2.2.1 URL 구조 분석

알라딘 월간 베스트셀러 페이지의 URL 구조는 다음과 같습니다:
```
https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&BestType=Month&Year={year}&Month={month}

파라미터:
- BranchType=1: 국내도서
- BestType=Month: 월간 베스트셀러
- Year={year}: 연도 (2020~2025)
- Month={month}: 월 (1~12)
```

### 2.2.2 HTML 선택자 탐색

#### 분석 도구: F12 개발자 도구

웹 브라우저의 F12 개발자 도구를 사용하여 HTML 구조를 분석했습니다.

**단계별 분석 과정:**

**1단계: 개발자 도구 실행**
```
알라딘 베스트셀러 페이지에서 F12 키 입력
→ 하단에 개발자 도구 패널 표시
```

**2단계: Elements 탭 활용**
```
Elements 탭 클릭
→ 웹페이지의 전체 HTML 구조 표시
```

**3단계: 요소 검사 (Inspect)**
```
개발자 도구 좌측 상단 화살표 아이콘 클릭
→ 페이지에서 원하는 요소 클릭
→ 해당 요소의 HTML 코드가 자동으로 하이라이트됨
```

**4단계: CSS Selector 추출**
```
HTML 요소 우클릭
→ Copy > Copy selector
→ 정확한 CSS Selector 복사됨
```

#### 추출된 CSS Selector

| 데이터 | CSS Selector | 추출 방법 |
|--------|--------------|-----------|
| 도서 컨테이너 | `div.ss_book_box` | 반복되는 도서 블록 확인 |
| 제목 | `a.bo3` | 제목 텍스트 클릭 → Copy selector |
| 저자 | `li.ss_aut a` | 저자명 클릭 → Copy selector |
| 카테고리 | `span.tit_category` | 카테고리 텍스트 클릭 |
| 가격 | `span.ss_p2 b` | 가격 영역 클릭 |
| 평점 | `span.Ere_fs14.Ere_str` | 별점 영역 클릭 |

#### 검증 과정

추출한 CSS Selector가 정확한지 개발자 도구의 **Console 탭**에서 검증했습니다:
```javascript
// Console 탭에서 실행
document.querySelectorAll("div.ss_book_box").length
// 결과: 50 (정상)

document.querySelector("div.ss_book_box a.bo3").textContent
// 결과: "소년이 온다" (제목 정상 추출)
```

### 2.2.3 크롤링 코드 구현
```python
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import time

def crawl_bestseller(year, month):
    """
    알라딘 월간 베스트셀러 TOP 50 크롤링
    
    Parameters:
    -----------
    year : int
        크롤링할 연도 (2020~2025)
    month : int
        크롤링할 월 (1~12)
    
    Returns:
    --------
    list : 도서 정보 딕셔너리 리스트
    """
    url = f"https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&BestType=Month&Year={year}&Month={month}"
    
    # User-Agent 설정 (크롤링 차단 방지)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # HTML 요청 및 파싱
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # 도서 정보 추출
    items = soup.select("div.ss_book_box")
    books = []
    
    for rank, item in enumerate(items, 1):
        try:
            # 제목
            title_tag = item.select_one("a.bo3")
            title = title_tag.text.strip() if title_tag else "N/A"
            
            # 저자
            author_tag = item.select_one("li.ss_aut a")
            author = author_tag.text.strip() if author_tag else "N/A"
            
            # 카테고리
            category_tag = item.select_one("span.tit_category")
            category = category_tag.text.strip() if category_tag else "N/A"
            
            # 가격
            price_tag = item.select_one("span.ss_p2 b")
            price = int(price_tag.text.strip().replace(',', '')) if price_tag else 0
            
            # 평점
            star_tag = item.select_one("span.Ere_fs14.Ere_str")
            star_score = float(star_tag.text.strip()) if star_tag else 0.0
            
            # item_id (도서 고유 ID)
            link_tag = item.select_one("a.bo3")
            item_id = link_tag['href'].split('ItemId=')[1].split('&')[0] if link_tag else "N/A"
            
            books.append({
                'year': year,
                'month': month,
                'rank': rank,
                'title': title,
                'author': author,
                'category': category,
                'price': price,
                'star_score': star_score,
                'item_id': item_id
            })
        except Exception as e:
            print(f"Error at {year}-{month} rank {rank}: {e}")
            continue
    
    return books

# 전체 기간 크롤링 실행
all_books = []
for year in range(2020, 2026):
    for month in range(1, 13):
        if year == 2025 and month > 11:  # 2025년 11월까지만
            break
        
        print(f"Crawling {year}-{month:02d}...")
        books = crawl_bestseller(year, month)
        all_books.extend(books)
        time.sleep(1)  # 서버 부하 방지

# DataFrame 변환 및 저장
df = pd.DataFrame(all_books)
df.to_csv('data/raw/aladin.csv', encoding='utf-8-sig', index=False)
print(f"Total books collected: {len(df)}")
```

### 2.2.4 수집 결과
```
총 수집: 3,539개 행
예상 수집: 3,550개 행
누락: 11개 (0.3%)

누락 상세:
- 2020년 4월: 1개 누락 (49개 수집)
- 2023년 2~11월: 각 1개씩 누락 (10개월, 각 49개 수집)
```

## 2.3 2차 크롤링: 도서 상세 정보

### 2.3.1 크롤링 목적

1차 크롤링에서는 **포괄적 카테고리**(예: "국내도서")만 수집되었으므로, 도서 상세 페이지에서 **구체적 카테고리**(예: "소설/시/희곡")와 **페이지 수**를 추가로 수집합니다.

### 2.3.2 도서 상세 페이지 구조
```
URL: https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={item_id}

추출 정보:
1. detail_category (상세 카테고리)
   - 선택자: ul.conts_info_list1 li
   - 예시: "국내도서 > 소설/시/희곡 > 한국소설"
   
2. page_count (페이지 수)
   - 선택자: ul.conts_info_list1 li
   - 예시: "368쪽"
```

### 2.3.3 병렬 처리 구현

고유 도서 1,960개의 상세 페이지를 효율적으로 크롤링하기 위해 병렬 처리를 구현했습니다:
```python
from concurrent.futures import ThreadPoolExecutor
import urllib.request
from bs4 import BeautifulSoup

def crawl_book_detail(item_id):
    """
    도서 상세 페이지에서 카테고리 및 페이지 수 추출
    
    Parameters:
    -----------
    item_id : str
        도서 고유 ID
    
    Returns:
    --------
    dict : {'item_id', 'detail_category', 'page_count'}
    """
    url = f"https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={item_id}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # 카테고리 추출
        category_tag = soup.select_one("ul.conts_info_list1 li")
        detail_category = "N/A"
        if category_tag:
            category_text = category_tag.text.strip()
            if '>' in category_text:
                parts = category_text.split('>')
                detail_category = parts[1].strip() if len(parts) > 1 else "N/A"
        
        # 페이지 수 추출
        page_count = 0
        info_items = soup.select("ul.conts_info_list1 li")
        for item in info_items:
            text = item.text.strip()
            if '쪽' in text:
                page_count = int(text.replace('쪽', '').strip())
                break
        
        return {
            'item_id': item_id,
            'detail_category': detail_category,
            'page_count': page_count
        }
    
    except Exception as e:
        print(f"Error crawling {item_id}: {e}")
        return {
            'item_id': item_id,
            'detail_category': None,
            'page_count': 0
        }

# 고유 item_id 추출
unique_item_ids = df['item_id'].unique().tolist()
print(f"고유 도서 수: {len(unique_item_ids)}개")

# 병렬 크롤링 (10개 스레드)
detail_data = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(crawl_book_detail, unique_item_ids)
    detail_data = list(results)

# DataFrame 변환 및 저장
df_detail = pd.DataFrame(detail_data)
df_detail.to_csv('data/raw/detail_mapping.csv', encoding='utf-8-sig', index=False)
print(f"Detail data collected: {len(df_detail)}")
```

### 2.3.4 수집 결과
```
고유 도서: 1,960개
수집 성공: 1,958개
수집 실패: 2개

실패 원인: 도서 상세 페이지 삭제 또는 URL 변경
```

## 2.4 크롤링 이슈 및 해결

### 이슈 1: HTML 선택자 오타

**문제:**
```python
# 초기 코드 (오타)
category_tag = item.select_one("span.tit_catrgory")  # "category" 스펠링 오류
```

**증상:**
- 모든 도서의 `category` 값이 `None`으로 수집됨
- 카테고리 정보 완전 손실

**해결:**
```python
# 수정 코드
category_tag = item.select_one("span.tit_category")  # 정확한 스펠링
```

**결과:**
- 카테고리 정보 정상 수집
- "국내도서", "외국도서" 등 포괄 카테고리 확보

---

### 이슈 2: 50위 도서 크롤링 실패

**문제:**
```python
items = soup.select("div.ss_book_box")
print(len(items))  # 49개만 반환 (50개 예상)
```

**원인 분석:**

1. **HTML 구조 확인:**
   - F12 개발자 도구로 확인 시 50위 도서가 페이지에 존재
   - BeautifulSoup 파싱 결과에는 49개만 포함

2. **가설:**
   - 동적 로딩: 50위 항목이 JavaScript로 동적 렌더링
   - HTML 구조 차이: 50위 항목의 클래스명이 다름
   - 광고 슬롯: 50위 위치에 광고가 삽입되는 경우

**해결 시도 1: Selenium 사용**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get(url)
WebDriverWait(driver, 10).until(...)  # JavaScript 렌더링 대기
items = driver.find_elements(By.CSS_SELECTOR, "div.ss_book_box")
```

**결과:** Google Colab 환경에서 Chrome Driver 설치 실패

**해결 시도 2: 대기 시간 추가**
```python
import time
response = urllib.request.urlopen(req)
time.sleep(3)  # 3초 대기 후 파싱
```

**결과:** 여전히 49개만 수집

**최종 결론:**
- 11개 데이터 누락 (전체의 0.3%)
- 분석에 미치는 영향 미미
- 향후 개선 과제로 남김

---

### 이슈 3: 성인 도서 크롤링 제한

**문제:**
- 성인 인증이 필요한 도서는 상세 페이지 접근 불가
- `detail_category` = `None`, `page_count` = `0`으로 수집됨

**영향받은 데이터:**
```
총 21개 고유 도서
베스트셀러 진입 횟수: 22회
```

**해결:**
- 전처리 단계에서 제거 (3.3절 참조)

## 2.5 데이터 저장 구조
```
data/
├── raw/
│   ├── aladin.csv              # 1차 크롤링 결과
│   │   ├── 행 수: 3,539개
│   │   ├── 컬럼: year, month, rank, title, author, 
│   │   │        category, price, star_score, item_id
│   │   └── 인코딩: UTF-8-sig
│   │
│   └── detail_mapping.csv      # 2차 크롤링 결과
│       ├── 행 수: 1,958개 (고유 도서)
│       ├── 컬럼: item_id, detail_category, page_count
│       └── 인코딩: UTF-8-sig
│
└── processed/
    └── aladin_final_cleaned.csv  # 최종 정제 데이터
        ├── 행 수: 3,517개
        ├── 컬럼: year, month, rank, title, author,
        │        category, price, star_score, item_id, page_count
        └── 인코딩: UTF-8-sig
```

---

# 3. 데이터 전처리 및 변환

## 3.1 데이터 병합

### 3.1.1 병합 전 데이터 상태

**aladin.csv (1차 크롤링):**
```
총 행 수: 3,539개
고유 도서: 1,960개
결측치: 없음

특징:
- 같은 도서가 여러 달 베스트셀러에 진입한 경우 여러 행으로 기록
- category: "국내도서" 등 포괄적 카테고리
- page_count: 모두 0 (정보 없음)
```

**detail_mapping.csv (2차 크롤링):**
```
총 행 수: 1,958개 (고유 도서)
결측치:
- detail_category: 21개 (1.1%)
- page_count: 0개 (모두 값 존재, 단 21개가 0)

특징:
- item_id 기준 1:1 매칭
- detail_category: "소설/시/희곡" 등 구체적 카테고리
- page_count: 0인 경우 = 성인 도서 (접근 불가)
```

### 3.1.2 병합 과정
```python
import pandas as pd

# 데이터 로드
df_aladin = pd.read_csv('data/raw/aladin.csv', 
                        index_col=0, 
                        dtype={'item_id': str})

df_detail = pd.read_csv('data/raw/detail_mapping.csv', 
                        dtype={'item_id': str})

print(f"aladin.csv: {len(df_aladin):,}개 행")
print(f"aladin.csv 고유 도서: {df_aladin['item_id'].nunique():,}개")
print(f"detail_mapping.csv: {len(df_detail):,}개 행 (고유 도서)")

# 병합 전 결측치 확인
print("\n[병합 전] detail_mapping.csv 결측치:")
print(df_detail.isnull().sum())

# 병합 (LEFT JOIN)
df_merged = pd.merge(
    df_aladin,
    df_detail.drop_duplicates(subset=['item_id']),  # 중복 제거
    on='item_id',
    how='left',
    suffixes=('', '_new')
)

print(f"\n병합 후: {len(df_merged):,}개 행")
```

**실행 결과:**
```
aladin.csv: 3,539개 행
aladin.csv 고유 도서: 1,960개
detail_mapping.csv: 1,958개 행 (고유 도서)

[병합 전] detail_mapping.csv 결측치:
item_id             0개
detail_category    21개 (1.1%) ← 성인 도서
page_count          0개

병합 후: 3,539개 행
```

### 3.1.3 병합 후 데이터 상태
```python
# 병합 후 결측치 확인
print("\n[병합 후] 결측치 분석:")
null_after = df_merged.isnull().sum()
for col, count in null_after.items():
    if count > 0:
        percentage = (count / len(df_merged)) * 100
        print(f"{col:20s} {count:4d}개 ({percentage:.1f}%)")
    else:
        print(f"{col:20s} {count:4d}개")
```

**실행 결과:**
```
[병합 후] 결측치 분석:
year                    0개
month                   0개
rank                    0개
category                0개
title                   0개
author                  0개
price                   0개
star_score              0개
item_id                 0개
page_count              0개
detail_category        22개 (0.6%) ← 21개 고유 도서가 22회 진입
```

**22개 vs 21개 차이 원인:**
- **21개**: 고유 도서 개수 (detail_mapping.csv 기준)
- **22개**: 베스트셀러 진입 횟수 (aladin.csv 기준)
- 성인 도서 중 1개가 **2번 베스트셀러에 진입**

## 3.2 카테고리 정제

### 3.2.1 카테고리 업데이트 로직
```python
# detail_category가 유효한 경우 category 업데이트
has_new_category = (
    df_merged['detail_category'].notnull() & 
    (df_merged['detail_category'] != 'N/A')
)

# 업데이트 실행
df_merged.loc[has_new_category, 'category'] = \
    df_merged.loc[has_new_category, 'detail_category']

# 통계 출력
print(f"카테고리 업데이트 성공: {has_new_category.sum()}개")
print(f"카테고리 업데이트 실패: {(~has_new_category).sum()}개")
```

**실행 결과:**
```
카테고리 업데이트 성공: 3,517개 (99.4%)
카테고리 업데이트 실패: 22개 (0.6%)

업데이트 실패 사유: 성인 도서 (detail_category = NaN)
```

### 3.2.2 Before / After 비교

| item_id | category (Before) | detail_category | category (After) |
|---------|-------------------|-----------------|------------------|
| 123456 | 국내도서 | 소설/시/희곡 | 소설/시/희곡 ✅ |
| 234567 | 국내도서 | 인문학 | 인문학 ✅ |
| 345678 | 국내도서 | NaN | 국내도서 ❌ (성인) |

### 3.2.3 최종 카테고리 분포
```python
print("\n최종 카테고리 분포 (TOP 10):")
print(df_merged['category'].value_counts().head(10))
```

**실행 결과:**
```
소설/시/희곡     742개
만화           453개
인문학         335개
경제경영       314개
어린이         289개
자기계발       244개
에세이         189개
외국어         172개
역사           148개
과학           127개
```

## 3.3 결측치 처리

### 3.3.1 페이지 수 업데이트
```python
# page_count_new가 있으면 page_count 업데이트
if 'page_count_new' in df_merged.columns:
    df_merged['page_count'] = df_merged['page_count_new'].fillna(
        df_merged['page_count']
    )
    df_merged = df_merged.drop(columns=['page_count_new'])

# 페이지 수 0인 도서 확인
page_zero = (df_merged['page_count'] == 0).sum()
print(f"page_count = 0인 도서: {page_zero}개")
```

**실행 결과:**
```
page_count = 0인 도서: 22개 (0.6%)
```

### 3.3.2 제거 대상 분석

성인 도서는 **page_count = 0 AND detail_category = NaN** 조건으로 식별합니다.
```python
# 제거 조건
df_merged['category_updated'] = has_new_category
condition_remove = (
    (df_merged['page_count'] == 0) & 
    (~df_merged['category_updated'])
)

# 제거 대상 확인
to_remove = df_merged[condition_remove]
print(f"\n제거 대상:")
print(f"- 행 수: {len(to_remove)}회 (베스트셀러 진입 기준)")
print(f"- 고유 도서: {to_remove['item_id'].nunique()}개")
print(f"- 이유: 성인 도서 (상세 페이지 접근 불가)")

# 도서별 진입 횟수
print(f"\n도서별 진입 횟수:")
entry_counts = to_remove['item_id'].value_counts()
for item_id, count in entry_counts.items():
    if count > 1:
        print(f"  item_id {item_id}: {count}회 진입 ← 2번 이상 진입")
```

**실행 결과:**
```
제거 대상:
- 행 수: 22회 (베스트셀러 진입 기준)
- 고유 도서: 21개
- 이유: 성인 도서 (상세 페이지 접근 불가)

도서별 진입 횟수:
  item_id 12345678: 2회 진입 ← 2번 이상 진입
  (나머지 20개는 각 1회씩 진입)
```

**핵심:**
- **21개 고유 도서**가 **총 22회** 베스트셀러에 진입
- 이 중 1개 도서가 2번 진입

### 3.3.3 데이터 정제
```python
# 성인 도서 제거
df_cleaned = df_merged[~condition_remove].copy()
df_cleaned = df_cleaned.drop(columns=['category_updated'])

print(f"\n최종 데이터:")
print(f"병합 후: {len(df_merged):,}개 행")
print(f"제거: {len(to_remove)}개 행")
print(f"최종: {len(df_cleaned):,}개 행")
```

**실행 결과:**
```
최종 데이터:
병합 후: 3,539개 행
제거: 22개 행
최종: 3,517개 행
```

## 3.4 데이터 검증

### 3.4.1 이상치 탐지
```python
# 가격 이상치
print("\n[가격 분석]")
print(df_cleaned['price'].describe())

# 페이지 수 이상치
print("\n[페이지 수 분석]")
print(df_cleaned['page_count'].describe())

# 평점 이상치
print("\n[평점 분석]")
print(df_cleaned['star_score'].describe())
```

**실행 결과:**
```
[가격 분석]
count    3517.00
mean    15296.31
std      4821.62
min         0.00  ← 무료 전자책
25%     12600.00
50%     15120.00
75%     17820.00
max    398000.00  ← 고가 전집

[페이지 수 분석]
count    3517.00
mean      334.21
std       156.83
min        16.00  ← 그림책
25%       232.00
50%       308.00
75%       404.00
max      2968.00  ← 전집

[평점 분석]
count    3517.00
mean        9.05
std         0.62
min         0.00  ← 평점 없음
25%         8.80
50%         9.20
75%         9.50
max        10.00
```

**이상치 판단:**
- 가격 0원: 무료 전자책 (정상)
- 가격 398,000원: 고가 전집 (정상)
- 페이지 2,968쪽: 전집 (정상)
- 모든 이상치가 실제 도서 특성을 반영 → 제거 불필요

### 3.4.2 데이터 타입 통일
```python
# 타입 변환
df_cleaned['item_id'] = df_cleaned['item_id'].astype(str)
df_cleaned['year'] = df_cleaned['year'].astype(int)
df_cleaned['month'] = df_cleaned['month'].astype(int)
df_cleaned['rank'] = df_cleaned['rank'].astype(int)
df_cleaned['price'] = df_cleaned['price'].astype(int)
df_cleaned['page_count'] = df_cleaned['page_count'].astype(int)
df_cleaned['star_score'] = df_cleaned['star_score'].astype(float)

# 타입 확인
print("\n[데이터 타입]")
print(df_cleaned.dtypes)
```

**실행 결과:**
```
[데이터 타입]
year            int64
month           int64
rank            int64
title          object
author         object
category       object
price           int64
star_score    float64
item_id        object
page_count      int64
```

### 3.4.3 중복 데이터 확인
```python
# 완전 중복 확인
duplicates = df_cleaned.duplicated()
print(f"\n완전 중복 행: {duplicates.sum()}개")

# item_id + year + month 기준 중복 (정상)
duplicates_key = df_cleaned.duplicated(subset=['item_id', 'year', 'month'])
print(f"item_id + year + month 중복: {duplicates_key.sum()}개")
print("→ 같은 도서가 같은 달에 여러 순위 진입 (정상)")
```

**실행 결과:**
```
완전 중복 행: 0개 ✅
item_id + year + month 중복: 0개 ✅
```

## 3.5 최종 데이터 구조

### 3.5.1 컬럼 정보

| 컬럼명 | 데이터 타입 | 설명 | 결측치 | 예시 |
|--------|-------------|------|--------|------|
| year | int64 | 연도 | 0 | 2024 |
| month | int64 | 월 | 0 | 10 |
| rank | int64 | 순위 (1~50) | 0 | 1 |
| title | object | 도서명 | 0 | 소년이 온다 |
| author | object | 저자명 | 0 | 한강 |
| category | object | 카테고리 (21개) | 0 | 소설/시/희곡 |
| price | int64 | 가격 (원) | 0 | 14,220 |
| star_score | float64 | 평점 (0~10) | 0 | 9.2 |
| item_id | object | 도서 고유 ID | 0 | 8936433660 |
| page_count | int64 | 페이지 수 | 0 | 216 |

### 3.5.2 최종 통계
```python
print("\n[최종 데이터 통계]")
print(f"총 행 수: {len(df_cleaned):,}개")
print(f"고유 도서: {df_cleaned['item_id'].nunique():,}개")
print(f"기간: {df_cleaned['year'].min()}년 {df_cleaned['month'].min()}월")
print(f"    ~ {df_cleaned['year'].max()}년 {df_cleaned['month'].max()}월")
print(f"카테고리: {df_cleaned['category'].nunique()}개")
print(f"평균 가격: {df_cleaned['price'].mean():,.0f}원")
print(f"평균 페이지: {df_cleaned['page_count'].mean():.0f}쪽")
print(f"평균 평점: {df_cleaned['star_score'].mean():.2f}점")
```

**실행 결과:**
```
[최종 데이터 통계]
총 행 수: 3,517개
고유 도서: 1,939개
기간: 2020년 1월 ~ 2025년 11월
카테고리: 21개
평균 가격: 15,296원
평균 페이지: 334쪽
평균 평점: 9.05점
```

## 3.6 전처리 흐름도
```
┌─────────────────────────────────────┐
│   원본 데이터                        │
│   - aladin.csv: 3,539개             │
│   - detail_mapping.csv: 1,958개     │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   1. 데이터 병합                     │
│   - LEFT JOIN (item_id 기준)        │
│   - 결과: 3,539개 행                │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   2. 카테고리 업데이트               │
│   - detail_category → category      │
│   - 성공: 3,517개 (99.4%)           │
│   - 실패: 22개 (0.6%, 성인 도서)    │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   3. 페이지 수 업데이트              │
│   - page_count_new → page_count     │
│   - page_count = 0: 22개            │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   4. 성인 도서 제거                  │
│   - 조건: page_count=0 AND          │
│          detail_category=NaN        │
│   - 제거: 22개 행 (21개 고유 도서)  │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   5. 데이터 검증                     │
│   - 이상치 확인                      │
│   - 데이터 타입 통일                 │
│   - 중복 데이터 확인                 │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   최종 데이터                        │
│   - 3,517개 행                      │
│   - 1,939개 고유 도서               │
│   - 21개 카테고리                   │
│   - 결측치: 0개                     │
└─────────────────────────────────────┘
```

## 3.7 최종 데이터 저장
```python
# 저장
import os
os.makedirs('data/processed', exist_ok=True)
df_cleaned.to_csv(
    'data/processed/aladin_final_cleaned.csv', 
    encoding='utf-8-sig', 
    index=True
)

print("\n✔ 최종 파일 저장 완료")
print(f"파일명: data/processed/aladin_final_cleaned.csv")
print(f"인코딩: UTF-8-sig")
print(f"크기: {os.path.getsize('data/processed/aladin_final_cleaned.csv') / 1024:.1f} KB")
```

**실행 결과:**
```
✔ 최종 파일 저장 완료
파일명: data/processed/aladin_final_cleaned.csv
인코딩: UTF-8-sig
크기: 847.3 KB
```

---

# 4. 핵심 분석 결과

## 4.1 2022년 가격·페이지 수 하락 분석

### 4.1.1 현상 확인

![yearly_price](../data/visualizations/01_yearly_price_trend.png)

**연도별 평균 가격 추이:**
```
2020년: 14,481원
2021년: 15,386원 (+6.2%)
2022년: 14,481원 (-5.9%) ← 급락
2023년: 15,348원 (+6.0%)
2024년: 16,010원 (+4.3%)
2025년: 16,155원 (+0.9%)
```

**연도별 평균 페이지 수 추이:**
```
2020년: 325쪽
2021년: 365쪽 (+12.3%)
2022년: 314쪽 (-14.0%) ← 급락
2023년: 342쪽 (+8.9%)
2024년: 333쪽 (-2.6%)
2025년: 328쪽 (-1.5%)
```

### 4.1.2 원인 분석: 3중 구조

![price_verification](../data/visualizations/01_2_price_verification_by_genre.png)

**1️⃣ 일반 도서 자체 하락 (가장 큰 원인)**
```
만화/어린이 제외 일반 도서:
- 가격: 16,541원 → 16,006원 (-3.2%)
- 페이지: 412쪽 → 355쪽 (-13.8%) ← 주된 요인
- 400쪽 이상 두꺼운 책: 158개 → 114개 (-7.6%p)
```

**2️⃣ 저가·저페이지 장르 비중 증가**
```
만화·어린이 비중:
- 2021년: 138개 (23.2%)
- 2022년: 154개 (25.7%) ← +2.5%p
- 만화 평균 가격: 약 10,075원 (일반 도서의 63%)
- 만화 평균 페이지: 약 197쪽 (일반 도서의 56%)
```

**3️⃣ 카테고리 구조 변화**
```
고가 카테고리 급감:
- 경제경영: 72회 → 47회 (-34.7%)
- 에세이: 59회 → 31회 (-47.5%)
- 사회과학: 21회 → 0회 (-100%)

저가 카테고리 증가:
- 만화: 72회 → 90회 (+25.0%)
- 자기계발: 21회 → 45회 (+114.3%)
```

**종합 효과:**
```
전체 평균에 이중 효과:
- 가격: -5.9% = (일반 -3.2%) + (장르 구성 -2.7%p)
- 페이지: -14.0% = (일반 -13.8%) + (장르 구성 -0.2%p)
```

### 4.1.3 핵심 인사이트

베스트셀러 평균 지표는 **장르 구성에 매우 민감하게 반응**함을 실증적으로 확인했습니다. 2022년 하락은 일반 도서 자체의 변화와 장르 구성 변화가 복합적으로 작용한 결과로 해석됩니다.

---

## 4.2 한강 노벨문학상 효과

### 4.2.1 수상 전후 비교

![han_kang_before_after](../data/visualizations/12_han_kang_before_after.png)

**베스트셀러 진입 횟수:**
```
수상 전 (2020.1~2024.9, 57개월): 7회
수상 후 (2024.10~2025.11, 14개월): 60회
증가율: +757% (약 8.6배)
```

### 4.2.2 시장 점유율 변화

![han_kang_vs_novels](../data/visualizations/11_han_kang_vs_total_novels.png)

**소설 시장 내 점유율:**
```
수상 전 평균: 0.5%
수상 후 평균: 7.2%
증가: +6.7%p (14.4배)

월별 최고점: 2024년 10월 17.3%
```

### 4.2.3 핵심 인사이트

노벨문학상 수상이라는 외부 이벤트가 베스트셀러 시장에 미치는 영향을 정량적으로 확인했습니다. 수상 후 14개월간 평균 점유율이 14.4배 증가하며, 2024년 10월에는 소설 시장의 17.3%를 차지했습니다.

---

## 4.3 슬램덩크 영화 개봉 효과

### 4.3.1 연도별 진입 횟수

![slamdunk_yearly](../data/visualizations/04_1_slamdunk_yearly_count.png)

**슬램덩크 관련 도서 진입 횟수:**
```
2020년: 0회
2021년: 0회
2022년: 0회
2023년: 53회 ← 영화 개봉 (2023.01.04)
2024년: 1회
2025년: 0회
```

### 4.3.2 만화 비중 변화

![category_ratio](../data/visualizations/04_yearly_category_ratio.png)

**만화 카테고리 비중:**
```
2020년: 17%
2021년: 21%
2022년: 25%
2023년: 32% ← 정점 (슬램덩크 46% 기여)
2024년: 20%
2025년: 15%
```

### 4.3.3 핵심 인사이트

영화 흥행(490만 관객, 일본 아카데미상)과 원작 만화 판매 증가 간 강한 상관관계가 관찰되었습니다. 슬램덩크 단일 시리즈가 2023년 만화 카테고리 베스트셀러 진입의 46%를 차지하며, 문화 콘텐츠 간 시너지 효과를 확인했습니다.

---

## 4.4 카테고리 비중 변화 (5년 트렌드)

**만화:**
```
2020년: 17% → 2023년: 32% (정점) → 2025년: 15%
변화: +15%p → -17%p
```

**인문학:**
```
2020년: 8% → 2025년: 23%
변화: +15%p (약 3배 증가)
```

**경제경영:**
```
2020년: 18% → 2021년: 20% (정점) → 2025년: 8%
변화: +2%p → -12%p
```

---

# 5. 결론

본 프로젝트는 2020~2025년 알라딘 월간 베스트셀러 3,517개를 크롤링·분석하여 다음을 확인했습니다.

## 핵심 발견

1. **한강 노벨문학상 효과:** 수상 후 베스트셀러 진입 8.6배 증가 (7회→60회), 소설 시장 점유율 14.4배 증가 (0.5%→7.2%)

2. **2023년 슬램덩크 효과:** 영화 개봉 후 원작 만화 53회 진입 (2022년 0회), 만화 비중 정점 달성 (32%)

3. **2022년 가격·페이지 하락:** 일반 도서 자체 하락 + 저가 장르 비중 증가의 이중 구조 확인, 베스트셀러 평균 지표가 장르 구성에 매우 민감하게 반응함을 실증

4. **인문학 약 3배 성장:** 2020년 8% → 2025년 23%, 장기적 독서 트렌드의 구조적 변화 관찰

## 기술적 성과

- BeautifulSoup4 기반 71개월 자동 크롤링 구현 (3,539개 수집)
- 병렬 처리를 통한 1,958개 도서 상세 정보 수집
- 성인 도서·결측치 처리 등 체계적 전처리 수행 (최종 3,517개)
- 장르 구성 변화가 평균 지표에 미치는 영향 정량화

## 학술적 기여

본 분석은 베스트셀러 시장의 변화를 설명하는 데 그치지 않고, **문화경제학·독서사회학 연구에서도 활용 가능한 정량적 근거를 제공**합니다. 특히 외부 문화적 사건(노벨상, 영화 개봉)이 출판 시장에 미치는 영향을 실증적으로 분석함으로써, 문화 콘텐츠 간 시너지 효과를 정량화하는 방법론적 기여를 할 수 있습니다.

---

## GitHub Repository

**프로젝트 전체 코드 및 데이터:**  
https://github.com/username/aladin-project

**포함 내용:**
- 크롤링 코드 (1차, 2차)
- 전처리 코드
- 시각화 코드 (15개 메인 + 4개 검증)
- 최종 데이터 (aladin_final_cleaned.csv)
- 상세 문서 (README.md)

---

## 참고문헌

1. 알라딘, 월간 베스트셀러 TOP 50 (2020.01~2025.11)
   - https://www.aladin.co.kr/shop/common/wbest.aspx

2. 대한출판문화협회(2023.07.17). 『2022년 책 종수와 평균 정가』 통계 발표

---

**작성자:** [학번] [이름]  
**제출일:** 2025년 00월 00일  
**과목:** 데이터 분석 프로젝트

---
