import time, datetime, ssl
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import re
from random import uniform
from itertools import count
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm # (필요) pip install tqdm

class AladinCategoryCrawler():
    myencoding = 'utf-8'

    def getSoup(self):
        if self.soup == None:
            return None
        else:
            return BeautifulSoup(self.soup, 'html.parser')

    def get_request_url(self):
        request = urllib.request.Request(self.url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        try:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(request, context=context, timeout=15)
            if response.getcode() == 200:
                return response.read().decode(self.myencoding)
        except Exception as err:
            print(err)
            now = datetime.datetime.now()
            msg = '[%s] error for url %s' % (now, self.url)
            print(msg)
            return None

    def get_category_from_detail(self, detail_url, retry=3):
        for attempt in range(retry):
            try:
                request = urllib.request.Request(detail_url)
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                context = ssl._create_unverified_context()
                response = urllib.request.urlopen(request, context=context, timeout=15)

                if response.getcode() == 200:
                    html = response.read().decode(self.myencoding)
                    soup = BeautifulSoup(html, 'html.parser')
                    category_links = soup.select('ul#ulCategory li a')

                    if len(category_links) >= 2:
                        return category_links[1].get_text(strip=True)
                    return "N/A"
            except Exception as err:
                if attempt < retry - 1:
                    # (중요) 기존 코드에 빠져있던 대기 시간 (예: 2초)
                    wait_time = (attempt + 1) * 2 
                    time.sleep(wait_time)
                else:
                    return "N/A"
        return "N/A"

    def extract_item_id(self, href):
        match = re.search(r'ItemId=(\d+)', href)
        return match.group(1) if match else None

    def save2Csv(self, result):
        data = pd.DataFrame(result, columns=self.mycolumns)
        data.to_csv(self.siteName + '.csv',
                    encoding='utf-8-sig', index=False)

    def __init__(self, siteName, url):
        self.siteName = siteName
        self.url = url
        self.mycolumns = ['item_id', 'real_category']
        if url:
            self.soup = self.get_request_url()
        else:
            self.soup = None

####################################################
siteName = 'category_mapping'
####################################################

def getCategoryData(csv_file='aladin.csv', max_workers=15):
    try:
        df = pd.read_csv(csv_file, index_col=0)
        if 'item_id' not in df.columns:
            print(f"오류: {csv_file}에 'item_id' 컬럼이 없습니다.")
            return
    except FileNotFoundError:
        print(f"오류: {csv_file} 파일을 찾을 수 없습니다.")
        print("먼저 1_crawl_bestsellers.py를 실행하세요.")
        return
    except Exception as e:
        print(f"CSV 파일 로드 중 오류: {e}")
        return

    print(f'원본 데이터: {len(df)}개 행')

    df_valid = df[pd.to_numeric(df['item_id'], errors='coerce').notnull()]
    unique_item_ids = df_valid['item_id'].unique()

    total_count = len(unique_item_ids)
    if total_count == 0:
        print("크롤링할 유효한 item_id가 없습니다.")
        return

    print(f'고유 ItemID 수: {total_count}개')

    crawler = AladinCategoryCrawler(siteName, "")
    savedData = [] 

    def fetch_category(item_id):
        try:
            detail_url = f'https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={item_id}'
            category = crawler.get_category_from_detail(detail_url)
            time.sleep(uniform(0.5, 1.5))
            return (item_id, category, None) # 성공
        except Exception as err:
            return (item_id, 'N/A', str(err)) # 실패

    print(f"병렬 크롤링 시작 (최대 {max_workers}개 동시 작업)...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_category, item_id): item_id for item_id in unique_item_ids}

        for future in tqdm(as_completed(futures), total=total_count, desc="카테고리 크롤링"):
            item_id, category, error = future.result()
            savedData.append([item_id, category])
            if error:
                tqdm.write(f"  [오류] ItemID {item_id}: {error}")

    crawler.save2Csv(savedData)

    print('='*60)
    print(f'총 {len(savedData)}개 ItemID 처리 완료')
    success = len([x for x in savedData if x[1] != 'N/A'])
    print(f'카테고리 추출 성공: {success}개')
    print(f'카테고리 추출 실패: {len(savedData) - success}개')
    print(f"\n'{siteName}.csv' 파일로 저장 완료.")

####################################################
if __name__ == "__main__": # 스크립트로 실행 시에만 작동
    print(siteName + ' 카테고리 크롤링 시작')
    getCategoryData('aladin.csv', max_workers=15)
    print(siteName + ' 카테고리 크롤링 끝')
