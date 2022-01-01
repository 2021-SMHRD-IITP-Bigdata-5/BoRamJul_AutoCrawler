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

#driver = webdriver.Chrome(chrome_options=opt, 
#    executable_path='<your-chromedriver-path>')
chrome_options = wb.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

wb_path = os.path.join('chromedriver')

driver = wb.Chrome(executable_path=wb_path,chrome_options=chrome_options)

## <!-- 스테디셀러 크롤러 start -->
# 스테디셀러 (알라딘)
# driver = wb.Chrome()
# url = 'https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&BestType=SteadySeller'
# driver.get(url)
soup = bs(driver.page_source, 'lxml')

title_steady = soup.select('.bo3')
title_list_steady = []
rank_list_steady = []
for i in range(len(title_steady)):
    title_list_steady.append(title_steady[i].text)
    rank_list_steady.append(i+1)
dic = {'순위':rank_list_steady,'책제목':title_list_steady}
df = pd.DataFrame(dic)
df.set_index('순위', inplace=True)
df.to_csv('./steady.csv', encoding='euc-kr')
df

df['순위'] = df['종합순위'].rank(method='first', ascending=True)
pd.options.display.float_format = '{:.0f}'.format
df.set_index('순위', inplace=True)
del df['종합순위']
## <!-- 스테디셀러 크롤러 end -->

# 데이터베이스 연결
conn = cx_Oracle.connect(oracle_user,oracle_password, '{}:{}/{}'.format(oracle_url ,oracle_port, oracle_dbName))

# 커서생성
cursor = conn.cursor()

## sql문
sql = 'DROP TABLE T_STEADY CASCADE CONSTRAINTS' ## T_STEADY 삭제
sql = 'CREATE TABLE T_STEADY(book_title varchar2(200), book_rank number(15)' ## T_STEADY 테이블 생성
sql = 'insert into T_STEADY values(:1,:2)'

for i in range(1, len(df.loc[:,'책제목'])+1):
    cursor.execute(sql,[df.loc[i]['책제목'],i])
# cursor.execute(sql, news_href_list[0])
    
print('저장된 링크수>>',cursor.rowcount)

# SQL실행 후 반영 및 커서, 데이터베이스객체 연결종료
cursor.close()
conn.commit()
conn.close()
