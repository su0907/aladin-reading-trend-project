# 선언부 - 크롤링 클래스
import time, datetime, ssl
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

class AladinBestSeller():
    myencoding = 'utf-8'

    def getSoup(self):
        if self.soup == None:
            return None
        else:
            return BeautifulSoup(self.soup, 'html.parser')

    def get_request_url(self):
        request = urllib.request.Request(self.url)
        try:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(request, context=context)
            if response.getcode() == 200:
                    return response.read().decode(self.myencoding)
        except Exception as err:
            print(err)
            now = datetime.datetime.now()
            msg = '[%s] error for url %s' % (now, self.url)
            print(msg)
            return None

    def save2Csv(self, result):
        data = pd.DataFrame(result, columns=self.mycolumns)
        data.to_csv(self.siteName + '.csv', 
                    encoding='utf-8-sig', index=True)

    def __init__(self, siteName, url):
        self.siteName = siteName
        self.url = url
        self.mycolumns = ['year', 'month', 'rank', 'category', 'title', 'price', 'star_score']
        self.soup = self.get_request_url()


# 실행부 - 크롤링 실행 함수
from itertools import count
import time

siteName = 'aladin'
base_url = 'https://www.aladin.co.kr/shop/common/wbest.aspx'

def getData():
    savedData = []

    for year in range(2020, 2026):
        last_month = 9 if year == 2025 else 12
        for month in range(1, last_month + 1):
            url = base_url
            url += '?BranchType=1&CID=0&Year=' + str(year)
            url += '&Month=' + str(month)
            url += '&Week=1&BestType=MonthlyBest&SearchSubBarcode='
            print(url)

            aladin = AladinBestSeller(siteName, url)
            soup = aladin.getSoup()

            if soup is None:
                break

            for rank, item in enumerate(soup.select("div.ss_book_box"), start=1):
                try:
                    catrgory_tag = item.select_one("span.tit_catrgory")
                    catrgory = catrgory_tag.get_text(strip=True).strip('[]') if catrgory_tag else "N/A"
                    title_tag = item.select_one("a.bo3")
                    title = title_tag.get_text(strip=True) if title_tag else "N/A"
                    price_tag = item.select_one("span.ss_p2")
                    price_text = price_tag.get_text(strip=True).split('원')[0] if price_tag else "0"
                    price = int(price_text.replace(",", ""))
                    star_score_tag = item.select_one("span.star_score")
                    star_score = float(star_score_tag.get_text(strip=True)) if star_score_tag else 0.0

                    savedData.append([year, month, rank, catrgory, title, price, star_score])
                except Exception as err:
                    print(err)
                    continue

    aladin.save2Csv(savedData)
    print('a' * 30)


# 실행 코드
if __name__ == "__main__":
    print(siteName + ' 베스트셀러 크롤링 시작')
    getData()
    print(siteName + ' 베스트셀러 크롤링 끝')