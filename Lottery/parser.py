from Lottery.config.settings import KAKAO_API_KEY
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()
from crawler.models import LotteryList

KAKAO_API_KEY = os.environ.get("KAKAO_API_KEY", None)

def getLotteryList():
    driver = webdriver.Chrome('/Users/suyeon/Downloads/chromedriver')
    driver.implicitly_wait(3)
    driver.get('https://dhlottery.co.kr/store.do?method=topStoreRank&rank=1&pageGubun=L645')
    Lottery = []
    for largePage in range(1, 22):
        if largePage == 1:
            first, last = 1, 11
        elif largePage == 21:
            first, last = 3, 4
        else:
            first, last = 3, 13
        print("first, last", first, last)
        for page in range(first, last):

            driver.find_element_by_xpath('//*[@id="page_box"]/a[{}]'.format(page)).send_keys(Keys.ENTER)
            driver.implicitly_wait(3)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            store_names = soup.select(
                '#article > div:nth-child(2) > div > div.group_content.group_data_search > table > tbody > tr > td:nth-child(2)'
            )

            locations = soup.select(
                '#article > div:nth-child(2) > div > div.group_content.group_data_search > table > tbody > tr > td:nth-child(4)'
            )

            counts = soup.select(
                '#article > div:nth-child(2) > div > div.group_content.group_data_search > table > tbody > tr > td:nth-child(3)'
            )

            for item in zip(store_names, locations, counts):
                lottery = {
                    'store_name': item[0].get_text().strip(),
                    'location': item[1].get_text().strip(),
                    'lottery_count': item[2].get_text().strip(),
                    'latitude': 0,
                    'longitude': 0
                }
                Lottery.append(lottery)
        if largePage == 21:
            break
        driver.find_element_by_css_selector('#page_box > a.go.next').send_keys(Keys.ENTER)
        driver.implicitly_wait(3)

    return Lottery

def getLatLng(input_list):
    for item in input_list:
        searchAddr = item['location']
        # location 으로 검색
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query={}'.format(searchAddr)
        headers = {
            "Authorization": "KakaoAK {}".format(KAKAO_API_KEY)
        }
        # places : 검색결과
        places = requests.get(url, headers=headers).json()['documents']
        for place in places:
            item['latitude'] = place['x']
            item['longitude'] = place['y']
    return input_list


if __name__ == '__main__':
    lotteryList = getLotteryList()
    result = getLatLng(lotteryList)
    for item in lotteryList:
        LotteryList(store_name=item['store_name'], location=item['location'], lottery_count=item['lottery_count'],
                    latitude=item['latitude'], longitude=item['longitude']).save()
