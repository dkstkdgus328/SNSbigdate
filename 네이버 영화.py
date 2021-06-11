from bs4 import BeautifulSoup

from selenium import webdriver

import time

import math

import numpy

import pandas as pd

import random

import os

import re



print("=" *80)

print(" 8. 네이버 영화 리뷰 및 평점 수집하기 ")

print("=" *80)

print("\n")





query_txt = input('영화제목을 입력하세요: ')

cnt = int(input('2.몇건 가져오시겠습니까?: '))

page_cnt = math.ceil(cnt / 20)

f_dir = input("3.파일 저장할 폴더명:")


now = time.localtime()

s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

os.makedirs(f_dir+s+'-'+query_txt)

os.chdir(f_dir+s+'-'+query_txt)


ff_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.txt'

fc_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.csv'

fx_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.xls'


s_time = time.time( )


path = "C:/Temp/chromedriver_win32/chromedriver.exe"

driver = webdriver.Chrome(path)

driver.get('https://movie.naver.com')

time.sleep(5)

driver.find_element_by_id("ipt_tx_srch").click()

element = driver.find_element_by_id("ipt_tx_srch")

element.send_keys(query_txt)

driver.find_element_by_class_name("btn_srch").click()

driver.find_element_by_class_name("result_thumb").click()

time.sleep(2)

driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[5]/a').click()

driver.switch_to.frame("pointAfterListIframe") 


def scroll_down(driver):

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);") 
    time.sleep(2)                                                           

scroll_down(driver)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

result= soup.find('div', class_='score_total').find('em')

result2 = result.get_text()

print("=" *80)

result3 = result2.replace(",","")

result4 = re.search("\d+",result3)

search_cnt = int(result4.group())

if cnt > search_cnt :

    cnt = search_cnt

print("전체 검색 결과 건수 :",search_cnt,"건")

print("실제 최종 출력 건수",cnt)

print("실체 출력될 최종 페이지수" , page_cnt)

review = []

r_nickname = []

r_date = []

r_star = []

r_gong = []

r_bgong = []







content_list = soup.find("div", class_ = "score_result").find_all('li')







up = 0







while True :
    
    f = open(ff_name, 'a',encoding='UTF-8')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    reple_result = soup.find('div', class_='score_result').find('ul')

    for li in content_list :



        up += 1

        f.write("\n")
        f.write("총 %s 건 중 %s 번째 리뷰 데이터를 수집합니다==============" %(cnt,up) + "\n")

        print("댓글 : ")
        
        temp_review = li.find("div", class_ = "score_reple").find("p").get_text()

        print(temp_review, "\n")
        f.write("3.리뷰:" + temp_review + "\n")
        review.append(temp_review)





        print("아이디 : ")
        
        temp_nickname = li.find("div", class_ = "score_reple").find_all("em")[0].get_text()

        temp_nickname = temp_nickname.replace("\n", "")

        print(temp_nickname)
        f.write("ID:"+temp_nickname + "\n")
        print("\n")

        r_nickname.append(temp_nickname)





        print("날짜 : ")
        
        temp_date = li.find("div", class_ = "score_reple").find_all("em")[1].get_text()

        print(temp_date)
        f.write("작성일자:" + temp_date + "\n")
        print("\n")

        r_date.append(temp_date)





        print("별점 : ")
        
        temp_star = li.find("div", class_ = "star_score").find("em").get_text()

        print(temp_star)
        f.write("별점:"+ temp_star +"\n")
        print("\n")

        r_star.append(temp_star)





        print("공감 : ")
        
        temp_gong = li.find("div", class_ = "btn_area").find_all("strong")[0].get_text()

        print(temp_gong)
        f.write("공감:" + temp_gong + "\n")
        print("\n")

        r_gong.append(temp_gong)





        print("비공감 : ")
        
        temp_bgong = li.find("div", class_ = "btn_area").find_all("strong")[1].get_text()

        print(temp_bgong)
        f.write("비공감:" + temp_bgong + "\n")
        print("\n\n")

        r_bgong.append(temp_bgong)

        
        
        
        
        

        if up == cnt :

            break

    f.close()

    if up  == cnt :

        break

        

    else :

        driver.find_element_by_link_text('''다음''').click()

        time.sleep(2)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        content_list = soup.find("div", class_ = "score_result").find_all('li')

        



movie_reple = pd.DataFrame()

movie_reple['댓글내용']=pd.Series(review)

movie_reple['작성자ID']=pd.Series(r_nickname)

movie_reple['작성일자']=pd.Series(r_date)

movie_reple['별점']=pd.Series(r_star)

movie_reple['공감횟수']=pd.Series(r_gong)

movie_reple['비공감횟수']=pd.Series(r_bgong)



movie_reple.to_csv(fc_name,encoding="utf-8-sig",index=True)


movie_reple.to_excel(fx_name ,index=True)




e_time = time.time( )

t_time = e_time - s_time



print("\n")





print("=" *80)

print("1.요청된 총 %s 건의 리뷰 중에서 실제 크롤링 된 리뷰수는 %s 건입니다" %(cnt,up))

print("2.총 소요시간은 %s 초 입니다 " %round(t_time,1))

print("3.파일 저장 완료: txt 파일명 : %s " %ff_name)

print("4.파일 저장 완료: csv 파일명 : %s " %fc_name)

print("5.파일 저장 완료: xls 파일명 : %s " %fx_name)

print("=" *80)







driver.close( )
