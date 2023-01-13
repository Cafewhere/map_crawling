from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
import pandas as pd
import os 


driver = webdriver.Chrome()
driver.get("https://map.naver.com/v5/")



# # 팝업 창 제거
# driver.find_element(By.CSS_SELECTOR,"button#intro_popup_close").click()
#검색창에 검색어 입력하기
time.sleep(3)

search_box = driver.find_element(By.XPATH,'/html/body/app/layout/div[3]/div[2]/shrinkable-layout/div/app-base/search-input-box/div/div[1]/div/input')

search_box.send_keys('카페')  #커피베이,빽다방


time.sleep(3)
# 검색버튼 누르기

search_box.send_keys(Keys.RETURN)

time.sleep(3)
#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > ul > li.SF_Mq.Sg7qM > div > a > div > div > span
#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > ul > li.SF_Mq.Sg7qM > div > a > div > div > span

# //*[@id="_pcmap_list_scroll_container"]/ul/li[2]/div[1]/a/div/div/span[1]
# //*[@id="_pcmap_list_scroll_container"]/ul/li[3]/div[1]/a/div/div/span[1]

searchiframe = driver.find_element(By.ID, "searchIframe")
driver.switch_to.frame(searchiframe)

# time.sleep(3)
cafe_name = []


for i in range(1,5): # 검색 결과중 상위 4개의 카페만 크롤링 합니다. 
           
        xpath = '//*[@id="_pcmap_list_scroll_container"]/ul/li['+str(i)+']/div[1]/a/div/div/span[1]'

        a = driver.find_element(By.XPATH, xpath)
        cafe_name.append(a.text) # 배열에 추가합니다.

print("-----------------------------------------------근처에 검색된 카페 목록 입니다---------------------------------------------")
print(cafe_name)

time.sleep(3)


# for i in range(1,5): # 1번째 부터 4번째까지
           
#     xpath = '//*[@id="_pcmap_list_scroll_container"]/ul/li['+str(i)+']/div[1]/a/div/div/span[1]'
cafe_menu = [] 
cafe_menu_price = []
cafe_review = []

cafe_num = 1


while(cafe_num<=4):
    
    cafe_xpath = '//*[@id="_pcmap_list_scroll_container"]/ul/li['+str(cafe_num)+']/div[1]/a/div/div/span[1]'
   
    driver.find_element(By.XPATH, cafe_xpath).click() # 검색해서 나온 카페중에 임의로 가장 첫번째 위치한 카페를 클릭합니다. 

    print("카페 명 : "+ driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li['+str(cafe_num)+']/div[1]/a/div/div/span[1]').text) # 카페 이름 
    print("-------------------------------------------------------------------------------------------------------------------------")
    driver.switch_to.default_content()
    driver.switch_to.frame(searchiframe)
    time.sleep(3)
    cafe_num+=1
    ####밑의 세줄을 써야지 상세 페이지의 정보를 크롤링 할 수 있습니다.
    driver.switch_to.default_content() 
    entryiframe = driver.find_element(By.ID, "entryIframe")

    driver.switch_to.frame(entryiframe)
    ###
    time.sleep(3) #3초 기다립니다.

    #카페의 사진을 출력합니다. 이미지는 xpath가 간단하여 굳이 for문을 쓰지 않았습니다.
    #image1 
    try:
        image1 = driver.find_element(By.XPATH, '//*[@id="ibu_1"]').get_attribute('style')
        image1 = image1[49:-32] # text중에서 이미지 주소에 해당되는 부분만 뽑아옵니다. 
        print("---------------------------------------------------카페 사진 입니다---------------------------------------------------")
        print(image1)
    except:
        print("사진이 존재하지 않습니다")
    #image2부터는 내부사진이 존재하는 경우가 많습니다.

    # image2 = image2[49:-32]# text중에서 이미지 주소에 해당되는 부분만 뽑아옵니다. 

    # image3 = driver.find_element(By.XPATH, '//*[@id="ibu_3"]').get_attribute('style')
    # image3 = image3[49:-32]

    # image4 = driver.find_element(By.XPATH, '//*[@id="ibu_4"]').get_attribute('style')
    # image4 = image4[49:-32]



    # print(image3)
    # print(image4)

    driver.switch_to.default_content() 
    driver.switch_to.frame(entryiframe)

    time.sleep(3)
    #운영시간은 버튼을 클릭해야 상세정보가 뜹니다. 
    #운영시간의 xpath -> 지점마다 다른 경우가 있어 css_selector를 사용하였습니다. 



    #app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.pSavy

    driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.pSavy > div > a > div > div > span').click() 

    time.sleep(3)
    oper_css= '#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.pSavy'

    o = driver.find_element(By.CSS_SELECTOR, oper_css)
    print("-------------------------------------------------------운영시간--------------------------------------------------------")
    print(o.text)
    print("-----------------------------------------------------------------------------------------------------------------------")
    time.sleep(3)

    driver.switch_to.default_content()
    driver.switch_to.frame(entryiframe)
    # driver. execute_script("window.scrollTo(0,900)") #스크롤 내리기 . <홈>에서 리뷰는 아래 부분에 위치합니다. 
    # time.sleep(3)
    # for n in range(1,4): # 3개의 리뷰를 가져옵니다. 리뷰는 click 버튼을 눌러야 전체를 볼 수 있지만, 보통 리뷰를 길게 쓰지 않고 , 1~2줄 정도는 전체로 보여지기 때문에 굳이 버튼을 추가하지 않았습니다. <홈>의 리뷰에서 가져온거라 최대 3개까지 볼수 있고 더 많은 리뷰는 <리뷰>창으로 이동해야합니다.  
    #     reivew_xpath = '//*[@id="app-root"]/div/div/div/div[7]/div/div[4]/div[2]/div/div[2]/ul/li['+str(n)+']/div/div/div[1]/a'
    #     r = driver.find_element(By.XPATH, reivew_xpath)
    #     cafe_review.append(r.text)
    # print("--------------------------------------------------------카페 리뷰입니다------------------------------------------------------")
    # print(cafe_review)



    # 상세정보 4개 홈-메뉴-리뷰-사진 순
    # 상세정보 5개 홈.소식.메뉴.리뷰.사진 or 홈.메뉴.선물하기.리뷰.사진
    # 상세정보 6개 홈.소식.메뉴.선물하기.리뷰.사진

    ####카카오맵과 다르게 어느 위치에있는지에 따라 경로가 바뀌어서 아예 텍스트로 검색하는게 낫다고 판단했습니다.


    menu_page = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[5]/div/div/div/div/a[2]/span')
    # print(menu_page.text)
    if (menu_page.text !='메뉴'):
            menu_page = driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div/div/div[5]/div/div/div/div/a[3]/span') #세번째 상세 정보 
            # print(menu_page.text)
    menu_page.click()


    time.sleep(3)

    j = 1

    while (j<30): # 대부분의 카페 메뉴는 많아봤자 20개 정도 이므로 충분한 크기의 30을 최대 메뉴 갯수로 설정 합니다. 

    # for j in range(1,5):
        try:
            
            menu_css = ' #app-root > div > div > div > div:nth-child(7) > div > div.place_section.no_margin > div > ul > li:nth-child('+str(j)+') > a > div > div.pr1Qk > div > span'
        #app-root > div > div > div > div:nth-child(7) > div > div.place_section.no_margin > div > ul > li:nth-child(1) > a > div.LZ3Zm > div.pr1Qk > div > span.Sqg65
        #app-root > div > div > div > div:nth-child(7) > div > div.place_section.no_margin > div > ul > li:nth-child(1) > a > div.LZ3Zm > div.pr1Qk > div > span
            price_css= '#app-root > div > div > div > div:nth-child(7) > div > div.place_section.no_margin > div > ul > li:nth-child('+str(j)+') > a > div.LZ3Zm > div.SSaNE'
        
            j+=1 
            b = driver.find_element(By.CSS_SELECTOR, menu_css)
            cafe_menu.append(b.text)
        
            
            c = driver.find_element(By.CSS_SELECTOR, price_css)
            cafe_menu_price.append(c.text)
        
        except:
                None
    print("--------------------------------------------------------카페 메뉴와 가격 입니다-----------------------------------------------")
    print(cafe_menu)
    print(cafe_menu_price)

    # menu_and_price = [] 
    # while (k<30):
    #     try:
    #         k=1
    #         menu_and_price.append(cafe_menu[k-1] +":" +cafe_menu_price[k-1])
    #         k+=1
    #     except:
    #         break
    # print(menu_and_price)

    print("------------------------------------------------------------------------------------------------------------------------------")

    driver.switch_to.default_content()
    driver.switch_to.frame(entryiframe)
    
    try:
        review_page = driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div/div/div[5]/div/div/div/div/a[3]/span')

        if (review_page.text !='리뷰'):
                review_page = driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div/div/div[5]/div/div/div/div/a[4]/span') 
                if (review_page.text !='리뷰'):
                    review_page = driver.find_element(By.XPATH,'//*[@id="app-root"]/div/div/div/div[5]/div/div/div/div/a[5]/span') 

        review_page.click()
    except:
        None

    time.sleep(3)


    cafe_review = [] 

    time.sleep(3)
    try:
        for j in range(1,5): #4개의 리뷰를 가져옵니다.

            review_css = '#app-root > div > div > div > div:nth-child(7) > div:nth-child(3) > div.place_section.lcndr > div.place_section_content > ul > li:nth-child('+str(j)+') > div.ZZ4OK.IwhtZ > a ' #임시로 상위 리뷰들이 더보기가 생길 경우 j크기를 조절해서 짧은리뷰들만 가져올수 있습니다.


        #app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section.lcndr > div.place_section_content > ul > li:nth-child(1) > div.ZZ4OK.IwhtZ > a
        #app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section.lcndr > div.place_section_content > ul > li:nth-child(1) > div.ZZ4OK.IwhtZ > a
            r = driver.find_element(By.CSS_SELECTOR, review_css )
            cafe_review.append(r.text)
            driver.execute_script("window.scrollTo(0, window.scrollY + 500);") #스크롤을 내려서 리뷰들을 봅니다. 
            time.sleep(3)
        print("--------------------------------------------------------카페 리뷰입니다------------------------------------------------------")
        print(cafe_review)
    except:
        print("리뷰가 제공되지 않습니다.") # None
 
    
    time.sleep(3)

    df1 = pd.DataFrame({"카페":cafe_name}) #네이버 지도는 별점 존재x
    df1.to_csv("cafe_name.csv", index = False, encoding='utf-8-sig')
        
        
    df2 = pd.DataFrame({"메뉴": cafe_menu, "가격": cafe_menu_price})
    df2.to_csv("cafe_menu_price.csv", index = False, encoding='utf-8-sig')



    df3 = pd.DataFrame({"리뷰": cafe_review})

        
    df3.to_csv("cafe_review.csv", index = False, encoding='utf-8-sig')

    driver.switch_to.default_content()
    driver.switch_to.frame(searchiframe)

driver.close()