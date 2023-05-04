import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import *
import time
import re
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ChromeOptions

import chromedriver_autoinstaller
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup as bs
from tqdm import tqdm


import sys


if len(sys.argv) != 3:
    start_num = 0
    finish_num = 10
else:
    start_num = int(sys.argv[1])
    finish_num = int(sys.argv[2])



input_data = pd.read_csv('./cafe_data.csv')
output_data = pd.DataFrame(columns=['si', 'gu', 'dong', 'name', 'review'])


opts = ChromeOptions()
opts.add_argument("--window-size=2560,1440")
chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=opts)

# 주소 입력
driver.get("https://map.naver.com")
time.sleep(30)

# 검색어 입력
for i in range(start_num, finish_num):
    reviews = []

    # 검색어 남아있는 경우에 삭제
    try:
        driver.find_element(By.CLASS_NAME,"button_clear").send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        pass

    # 검색 박스 선택
    search_box = driver.find_element(By.CLASS_NAME,'input_search')
    search_box.click()
    time.sleep(1)
    
    # 검색어 입력 및 검색
    si, gu, dong, cafe_name, _ = input_data.iloc[i] # 서울특별시,강남구,역삼동,정월
    search = f"{si} {gu} {dong} {cafe_name}"
    print(f"#################### {i}th [{search}] ####################")
    search_box.send_keys(search)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    # searchiframe 저장
    searchiframe = driver.find_element(By.ID, "searchIframe")
    driver.switch_to.frame(searchiframe)
    time.sleep(1)

    # 검색했을 때 결과가 안 나올 경우
    try:
        # 검색했을 때 결과가 여러개인 경우 / 안 들어가지는 경우에 대해 처리
        try:
            driver.find_element(By.CLASS_NAME, 'place_bluelink').click()
            time.sleep(2)
        except Exception as e:
            pass

        # iframe 전환
        driver.switch_to.default_content()
        entryiframe = driver.find_element(By.ID, "entryIframe")
        driver.switch_to.frame(entryiframe)
        time.sleep(3)

        # 탭 메뉴 element 얻어오기 및 리뷰탭 찾기
        tabs = driver.find_elements(By.CLASS_NAME, '_tab-menu')
        tab_length = len(tabs)
    except Exception as e: # 카페가 없음 -> 다음 검색어로 이동
        # 리뷰 저장
        output_data.loc[len(output_data)] = [si, gu, dong, cafe_name, reviews]
        driver.switch_to.default_content()
        continue
        
    has_review_tab = False
    for tap in tabs:
        if tap.text == '리뷰':
            tap.click()
            has_review_tab = True
            time.sleep(2)
            break

    if not has_review_tab: # 리뷰가 없음 -> 다음 검색어로 이동
        # 리뷰 저장
        output_data.loc[len(output_data)] = [si, gu, dong, cafe_name, reviews]
        driver.switch_to.default_content()
        continue
    
    # 리뷰 수 카운트 (DEBUG용)
    review_count = driver.find_element(By.CLASS_NAME, 'place_section_count').text
    
    # 아래로 내리기
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

    # 모든 리뷰를 펼칠 때까지 다음을 반복 (리뷰의 질을 고려해 9번만 시행 -> 10*9 + 10 = 최대 100개 리뷰)
    for _ in range(9):
        try:
            # 더보기 버튼이 있다면
            more_btn = driver.find_element(By.CLASS_NAME, 'fvwqf')
            if more_btn.text != '더보기': break

            # 더보기 버튼 클릭
            more_btn.send_keys(Keys.ENTER)
            time.sleep(0.2)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(1)
        except Exception as e: # 더보기 버튼이 없다
            break

    # 리뷰 크롤링
    review_list = driver.find_elements(By.CLASS_NAME, 'zPfVt')
    time.sleep(1)
    
    for review in tqdm(review_list):
        time.sleep(0.1)
        try:
            # 리뷰 펼치기
            driver.execute_script("arguments[0].click();", review.find_element(By.XPATH, '..'))
            # 해당 리뷰 추가
            reviews.append(review.text)
        except Exception as e:
            print(f"리뷰가 존재하지 않음 {e}")

    # 리뷰 저장
    output_data.loc[len(output_data)] = [si, gu, dong, cafe_name, reviews]
    

    driver.switch_to.default_content()
    time.sleep(5)

    
pd.DataFrame(output_data).to_csv(f'./data/review_data-{start_num}+{finish_num}-{datetime.datetime.now().strftime("%d%H%M")}.csv')
    
print(" _____ _   _ ____\n\
| ____| \ | |  _ \\n\
|  _| |  \| | | | |\n\
| |___| |\  | |_| |\n\
|_____|_| \_|____/ ")
 
