#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import requests as req
import json
import os
import sys
import cx_Oracle
import time
import pandas as pd

from bs4 import BeautifulSoup as bs
from inspect import getsourcefile
from os.path import abspath
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

oracle_url = 'project-db-stu.ddns.net'
oracle_user = 'cgi_7_2_1216'
oracle_password = 'smhrd2'
oracle_port = '1524'
oracle_dbName = 'xe'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

## <!-- 베스트셀러 크롤러 start -->
## 베스트셀러 모두 종합
# 베스트셀러(YES24)
#driver = wb.Chrome()
#opt = Options()
#opt.add_argument("--no-sandbox")
#opt.add_argument("--disable-dev-shm-usage")

#driver = webdriver.Chrome(chrome_options=opt, 
#    executable_path='<your-chromedriver-path>')
chrome_options = wb.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

# a = os.path.join("path/of/driver","chromedriver")

# BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
# print(BASE_DIR)
# print(os.path.join(BASE_DIR, '.github/workflows/repo/chromedriver'))

wb_path = os.path.join('chromedriver')

driver = wb.Chrome(executable_path=wb_path,chrome_options=chrome_options)

url = 'https://book.naver.com/bestsell/bestseller_list.naver?cp=yes24'
driver.get(url)
soup = bs(driver.page_source, 'lxml')

title_yes = soup.select('ol.basic>li>dl>dt>a')
title_list_yes = []
rank_list_yes = []
for i in range(len(title_yes)):
    rank_list_yes.append(i+1)
    title_list_yes.append(title_yes[i].text)
dic = {'순위':rank_list_yes,'책제목':title_list_yes}
df_yes = pd.DataFrame(dic)

# 베스트셀러(교보문고)
url = 'https://book.naver.com/bestsell/bestseller_list.naver?cp=kyobo'
driver.get(url)
soup = bs(driver.page_source, 'lxml')

title_kyobo = soup.select('ol.basic>li>dl>dt>a')
title_list_kyobo = []
rank_list_kyobo = []
for i in range(len(title_kyobo)):
    rank_list_kyobo.append(i+1)
    title_list_kyobo.append(title_kyobo[i].text)
dic = {'순위':rank_list_kyobo,'책제목':title_list_kyobo}
df_kyobo = pd.DataFrame(dic)

# 베스트셀러(알라딘)
url = 'https://book.naver.com/bestsell/bestseller_list.naver?cp=aladdin'
driver.get(url)
soup = bs(driver.page_source, 'lxml')

title_din = soup.select('ol.basic>li>dl>dt>a')
title_list_din = []
rank_list_din = []
for i in range(len(title_din)):
    rank_list_din.append(i+1)
    title_list_din.append(title_din[i].text)
dic = {'순위':rank_list_din,'책제목':title_list_din}
df_din = pd.DataFrame(dic)

# 베스트셀러(인터파크도서)
url = 'https://book.naver.com/bestsell/bestseller_list.naver?cp=bookpark'
driver.get(url)
soup = bs(driver.page_source, 'lxml')

title_park = soup.select('ol.basic>li>dl>dt>a')
title_list_park = []
rank_list_park = []
for i in range(len(title_park)):
    rank_list_park.append(i+1)
    title_list_park.append(title_park[i].text)
dic = {'순위':rank_list_park,'책제목':title_list_park}
df_park = pd.DataFrame(dic)

# 베스트셀러(영풍문고)
url = 'https://book.naver.com/bestsell/bestseller_list.naver?cp=ypbooks'
driver.get(url)
soup = bs(driver.page_source, 'lxml')

title_yp = soup.select('ol.basic>li>dl>dt>a')
title_list_yp = []
rank_list_yp = []
for i in range(len(title_yp)):
    rank_list_yp.append(i+1)
    title_list_yp.append(title_yp[i].text)
dic = {'순위':rank_list_yp,'책제목':title_list_yp}
df_yp = pd.DataFrame(dic)

df_all=pd.concat([df_yes,df_kyobo,df_din,df_park,df_yp])

# 베스트셀러 종합순위
df_all_title = []
df_all_rank = []

for i in df_all['책제목'].unique():
    if len(df_all['순위'][df_all['책제목'] == i]) == 1:
        mean = df_all['순위'][df_all['책제목'] == i].mean()+20
    elif len(df_all['순위'][df_all['책제목'] == i]) == 2:
        mean = df_all['순위'][df_all['책제목'] == i].mean()+15
    elif len(df_all['순위'][df_all['책제목'] == i]) == 3:
        mean = df_all['순위'][df_all['책제목'] == i].mean()+10
    elif len(df_all['순위'][df_all['책제목'] == i]) == 4:
        mean = df_all['순위'][df_all['책제목'] == i].mean()+5
    else : mean = df_all['순위'][df_all['책제목'] == i].mean()
    df_all_title.append(i)
    df_all_rank.append(mean)
    
dic = {'종합순위':df_all_rank, '책제목':df_all_title}
df = pd.DataFrame(dic)
df.set_index('종합순위')
pd.options.display.float_format = '{:.2f}'.format # 종합순위 반올림
df = df.sort_values('종합순위') # 오름차순 정렬

df['순위'] = df['종합순위'].rank(method='first', ascending=True)
pd.options.display.float_format = '{:.0f}'.format
df.set_index('순위', inplace=True)
del df['종합순위']
## <!-- 베스트셀러 크롤러 end -->

# 데이터베이스 연결
conn = cx_Oracle.connect(oracle_user,oracle_password, '{}:{}/{}'.format(oracle_url ,oracle_port, oracle_dbName))

# 커서생성
cursor = conn.cursor()

## sql문
sql = 'DROP TABLE T_BEST' ## T_BEST 삭제
sql = 'CREATE TABLE T_BEST(book_title varchar2(200), book_rank number(15)' ## T_BEST 생성
sql = 'insert into t_best values(:1,:2)'

for i in range(1, len(df.loc[:,'책제목'])+1):
    cursor.execute(sql,[df.loc[i]['책제목'],i])
# cursor.execute(sql, news_href_list[0])
    
print('저장된 링크수>>',cursor.rowcount)

# SQL실행 후 반영 및 커서, 데이터베이스객체 연결종료
cursor.close()
conn.commit()
conn.close()

