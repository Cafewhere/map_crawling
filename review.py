import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import *
import time
import re

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


start_num = 160
finish_num = 200

input_data = pd.read_csv('./data.csv', header=None)



opts = ChromeOptions()
opts.add_argument("--window-size=2560,1440")
chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=opts)

# 주소 입력
driver.get("https://map.naver.com")
time.sleep(30)

# 검색어 입력
for i in range(start_num-1, finish_num, 10):
    
    reviews = [] 
    # 검색 박스
    search_box = driver.find_element(By.CLASS_NAME,'input_search')
    search_box.click()
    time.sleep(1)
    #search_box.send_keys('123.00')
    ActionChains(driver).double_click(search_box).perform()
    time.sleep(1)
    search_box.send_keys(Keys.DELETE)
    time.sleep(1)
    
         
   
    # 주소 검색
    address1, address2, address3 = input_data.iloc[i]
    print(f"[!{i}번째 검색어!] {address1} {address2} {address3}")
    #print(f'\n-----------------{address1}+{address2}+{address3}-------------------')
    search_box.send_keys(address1, address2, address3, '카페')
    search_box.send_keys(Keys.RETURN)
    time.sleep(10)
    


  
    # iframe 변경
    searchiframe = driver.find_element(By.ID, "searchIframe")
    driver.switch_to.frame(searchiframe)
    time.sleep(1)

    # scroll_div = driver.find_element(By.CLASS_NAME, "Ryr1F") 
    # # //*[@id="_pcmap_list_scroll_container"]
    # #검색 결과로 나타나는 scroll-bar 포함한 div 잡고
    # driver.execute_script("arguments[0].scrollBy(0,2000)", scroll_div)
    # time.sleep(1)
    # driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
    # time.sleep(1)
    # driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
    # time.sleep(1)
    # driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
    # time.sleep(1)
    # driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
    # time.sleep(1)
    # #여기까지 scroll
    # #맨 아래까지 내려서 해당 페이지의 내용이 다 표시되게 함


    try:
        driver.find_element(By.CSS_SELECTOR, '#app-root > div > div:nth-child(1) > div > div > div > div > div > span:nth-child(2) > a').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#app-root > div > div:nth-child(1) > div > div.sgugZ.R9QDR > div > ul > li:nth-child(2) > a').click()
        time.sleep(1)
    except:
        driver.switch_to.default_content()
        continue



    # 카페 리스트 선택
    for j in range(1, 11):
        print(f"{j}번째 카페")
        #print("[[1]] 카페 선택")
        driver.find_element(By.XPATH, f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{j}]/div[1]/a/div/div/span[1]').click()
        time.sleep(2)

        
        # 카페 세부 정보 크롤링
        #print("[[2]] iframe 전환")
        driver.switch_to.default_content()
        entryiframe = driver.find_element(By.ID, "entryIframe")
        driver.switch_to.frame(entryiframe)
        time.sleep(3)

        tabs = driver.find_elements(By.CLASS_NAME, '_tab-menu')
        tab_length = len(tabs)
       
        #print("[[3]] 리뷰탭 클릭")
        
        has_review_tab = False
        for tap in tabs:
            if tap.text == '리뷰':
                tap.click()
                has_review_tab = True
                continue
            
            
        if not has_review_tab:
            continue
        

        
        time.sleep(2)
        review_count = driver.find_element(By.CLASS_NAME, 'place_section_count').text
        #print(f"[[4]] 스크롤")
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        while True:
            try:
                
                more_btn = driver.find_element(By.CLASS_NAME, 'fvwqf')
                if more_btn.text == '더보기':
                    more_btn.send_keys(Keys.ENTER)
                else:
                    break
                #ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME, 'fvwqf')).click().perform()
                #print(f'\t더보기 클릭')
                time.sleep(0.2)
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(1)
            except Exception as e:
                #print(f'더보기 없음 {e}')
                break

        # 리뷰 크롤링
        # zPfVt
        #review_list = bs(driver.page_source, 'html.parser').find_all('span', {"class":'zPfVt'})
        review_list = driver.find_elements(By.CLASS_NAME, 'zPfVt')
        time.sleep(1)
        #print(f'\t {len(review_list)} / {review_count}')
        for review in tqdm(review_list):
            time.sleep(0.1)
            try:
                
                driver.execute_script("arguments[0].click();", review.find_element(By.XPATH, '..'))
                
                reviews.append(review.text)
                #print(review.text)
            except Exception as e:
                print(f"리뷰가 존재하지 않음 {e}")

        driver.switch_to.default_content()
        driver.switch_to.frame(searchiframe)

    driver.switch_to.default_content()
    time.sleep(5)

    pd.DataFrame(reviews).to_csv(f'./data/{address1}+{address2}+{address3}+review_data.csv')
    


