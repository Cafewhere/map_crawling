from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
import pandas as pd
import os 


driver = webdriver.Chrome()
driver.get("https://map.kakao.com/")

time.sleep(3) #기다림

# my_location = driver.find_element(By.XPATH, '//*[@id="search.keyword.bounds"]') #현 지도 내 장소 검색


time.sleep(3)


# searchbox = driver.find_element_by_xpath("//input[@id='search.keyword.query']") # 검색창에 입력하기
searchbox = driver.find_element(By.XPATH, " //input[@id='search.keyword.query']") 
searchbox.send_keys("스타벅스")
time.sleep(3)
# searchbutton = driver.find_element_by_xpath("//button[@id='search.keyword.submit']") # 검색버튼 누르기
searchbutton = driver.find_element(By.XPATH, " //button[@id='search.keyword.submit']") 

driver.execute_script("arguments[0].click();", searchbutton) 

time.sleep(2)



cafe_list = []
oper_list = []
star_list = []

# cafe_menu_price = [] 

for j in range(1,5):
    cafe_name_xpath=  '//*[@id="info.search.place.list"]/li['+str(j)+']/div[3]/strong/a[2]'
    b = driver.find_element(By.XPATH, cafe_name_xpath)
    cafe_list.append(b.text)
print("---------------------------------카페리스트------------------------------")
print(cafe_list)

i=1
while(i<=4):
    print(cafe_list[i-1]+"의 정보입니다.")

    ###################카페 더보기###########################
    # place_more = driver.find_element(By.XPATH, "//*[@id='info.search.place.more']")
    # driver.execute_script("arguments[0].click();", place_more) 

    # for j in range(6,10):
    #     cafe_name_xpath=  '//*[@id="info.search.place.list"]/li['+str(j)+']/div[3]/strong/a[2]'
    #     b = driver.find_element(By.XPATH, cafe_name_xpath)
    #     cafe_list.append(b.text)
    # print(cafe_list)
        # for j in range(1,5):


    cafe_info = driver.find_element(By.XPATH, '//*[@id="info.search.place.list"]/li['+str(i)+']/div[5]/div[4]/a[1]')
    i+=1 
    driver.execute_script("arguments[0].click();", cafe_info) 
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환 . 

    time.sleep(2)
    print("------------------------------------------------------------------------")
    try: ######영업시간 더보기 버튼 있을때 

        time_info = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[1]/ul/li/a/span')
        driver.execute_script("arguments[0].click();", time_info) 
        time.sleep(2)

        time_xpath = driver.find_element(By.XPATH,'//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[2]/div')
        tx = time_xpath.text
        print(tx)
      

    except: ###영업시간 더보기 버튼 없을때 
        try:
            time_xpath = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div/ul/li/span')
            tx = time_xpath.text
            print(tx) 
           
        except:
            None
            


    print("----------------------------------메뉴/가격------------------------------")



    try:
        more_menu = driver.find_element(By.CSS_SELECTOR, '#mArticle > div.cont_menu > a > span.ico_comm.ico_more') #메뉴 더보기 있는 경우 
        driver.execute_script("arguments[0].click();", more_menu)  #메뉴 더보기 클릭 
        menu_list = [] 
        price_list = [] 
        j = 1
        while(j<30):
            try:
                menu_info_xpath = '#mArticle > div.cont_menu > ul > li:nth-child('+str(j)+') > div > span'
                price_info_xpath =  '#mArticle > div.cont_menu > ul > li:nth-child('+str(j)+') > div > em.price_menu'
                a = driver.find_element(By.CSS_SELECTOR, menu_info_xpath )
                b = driver.find_element(By.CSS_SELECTOR, price_info_xpath)
                j+=1 
            except:
                break #예외나면 빈칸으로 출력 

        
            menu_list.append(a.text)
            price_list.append(b.text)
        print(menu_list) #메뉴
        print(price_list)

    except: #메뉴 더보기 없음 
        k = 1
        while (k<10):
            try:
                menu_info_xpath = '#mArticle > div.cont_menu > ul > li:nth-child('+str(k)+') > div > span'
                a = driver.find_element(By.CSS_SELECTOR, menu_info_xpath )
            except:
                break





    # menu_and_price = [] 
    # try:
    #     

    #     for j in range(5,10):
        
    #             menu_info_xpath = '#mArticle > div.cont_menu > ul > li:nth-child('+str(j)+') > div > span'
    #             a = driver.find_element(By.CSS_SELECTOR, menu_info_xpath )

    #             menu_list.append(a.text)
            


    #     for j in range(5,10):
            
    #             price_info_xpath =  '#mArticle > div.cont_menu > ul > li:nth-child('+str(j)+'+) > div > em.price_menu'
    #             a= driver.find_element(By.CSS_SELECTOR, price_info_xpath)
        
    #             price_list.append(a.text)
    #             #mArticle > div.cont_menu > ul > li:nth-child(9) > div > em.screen_out
        


    # except:
    #         print("더보기 오류")


    # try:
    #     for k in range(1,20):
    #         menu_and_price.append(menu_list[k-1] +":" +price_list[k-1] +"원")
    #     print(menu_and_price) 

    # except:
    #     print("")


    ##################별점 #################


    try:
        star = driver.find_element(By.XPATH, '//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div/a[1]/span[1]')
        st =  star.text
        print("★ : "+  st +"점")
        
        star_list.append(st)


    except:
        print("별점 없음")
    print(star_list)
    ##################리뷰 ##################

    review_list = []

    j=1
    while(j<5):
        try: 

            
            #review_xpath = '//*[@id="mArticle"]/div[7]/div[2]/ul/li['+str(j)+']/div[3]/p/span' #리뷰 xpath 경로가 다른 경우 
            review_css = '#mArticle > div.cont_evaluation > div.evaluation_review > ul > li:nth-child('+str(j)+') > div.comment_info > p > span'
            

            #review = driver.find_element(By.XPATH, review_xpath)
            review = driver.find_element(By.CSS_SELECTOR, review_css)
            review_list.append(review.text)
            j+=1

        except: break
        #     review_xpath = '//*[@id="mArticle"]/div[7]/div[2]/ul/li['+str(j)+']/div[4]/p/span'
        #     review = driver.find_element(By.XPATH, review_xpath)
        #     review_list.append(review.text)
            # try:
            #     review_xpath = '//*[@id="mArticle"]/div[7]/div[3]/ul/li['+str(j)+']/div[3]/p/span'
            #     review = driver.find_element(By.XPATH, review_xpath)
        
            #     review_list.append(review.text)
            # except:
            #     review_xpath = '//*[@id="mArticle"]/div[7]/div[3]/ul/li['+str(j)+']/div[4]/p/span'
            #     review = driver.find_element(By.XPATH, review_xpath)
        
            #     review_list.append(review.text)

    print("-------------------------------리뷰--------------------------------------") 
    print(review_list)

    ################카페 사진 url###################
    print("--------------------------------카페 사진 주소----------------------------")
    frame_list = [] 
    for j in range(1,4):
        try: 
            frame_xpath= '//*[@id="mArticle"]/div[5]/div[2]/ul/li['+str(j)+']/a'
            frame = driver.find_element(By.XPATH, frame_xpath).get_attribute('style')
        except:
            break
        image = frame[23:-2]
        frame_list.append(image)
    print(frame_list)


    # 현재 사용중인 탭 종료
    driver.close()

    # 메인 탭으로 이동
    driver.switch_to.window(driver.window_handles[0])

    
df1 = pd.DataFrame({"카페":cafe_list, "별점":star_list})
df1.to_csv("cafe_list.csv", index = False, encoding='utf-8-sig')
    
    
df2 = pd.DataFrame({"메뉴": menu_list, "가격": price_list})
df2.to_csv("menu_and_price.csv", index = False, encoding='utf-8-sig')



df3 = pd.DataFrame({"리뷰": review_list})

    
df3.to_csv("review.csv", index = False, encoding='utf-8-sig')
