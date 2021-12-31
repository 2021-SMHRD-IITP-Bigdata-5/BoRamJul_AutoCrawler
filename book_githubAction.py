#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests as req
from bs4 import BeautifulSoup as bs
import json
import os
import sys
from inspect import getsourcefile
from os.path import abspath
import cx_Oracle
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

oracle_url = 'project-db-stu.ddns.net'
oracle_user = 'cgi_7_2_1216'
oracle_password = 'smhrd2'
oracle_port = '1524'
oracle_dbName = 'xe'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

category = ['0401','0402','0403','0404','0405','0408','0409']
news_href_list = []

## <!-- 베스트셀러 크롤러 start -->
## 베스트셀러 모두 종합
# 베스트셀러(YES24)
#driver = wb.Chrome()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ChromeOptions options = new ChromeOptions();
options.addArguments("--headless");
driver = new ChromeDriver(options);

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
driver = wb.Chrome()
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
driver = wb.Chrome()
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
driver = wb.Chrome()
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
driver = wb.Chrome()
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
conn = cx_Oracle.connect(oracle_user,oracle_password, '{}:{}/{}'.format(project-db-stu.ddns.net,1524, xe))

# 커서생성
cursor = conn.cursor()

sql = 'insert into t_best values(:1,:2, )'

for href in df:
    cursor.execute(sql,href)
# cursor.execute(sql, news_href_list[0])
    
print('저장된 링크수>>',cursor.rowcount)

# SQL실행 후 반영 및 커서, 데이터베이스객체 연결종료
cursor.close()
conn.commit()
conn.close()

