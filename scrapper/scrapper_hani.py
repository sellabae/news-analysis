# -*- coding: UTF-8 -*-
#  한겨레 hani.co.kr 전체기사 코너(날짜구분없이 최신뉴스 순서대로) 기사제목 크롤러

import requests
from bs4 import BeautifulSoup
import lxml

import os
import datetime as dt
from datetime import datetime
import pandas as pd
import re

# 스크래핑 --------------------------------------------------------
print('한겨레 기사 제목 스크래퍼')

# local time
print('local', datetime.now())
# 현재 한국 시간
KST = dt.timezone(dt.timedelta(hours=9)) #korean timezone utc+9
now = datetime.now(tz=KST)
print('korea', now)

# 저장될 데이터프레임 준비
cols = ['date','category','title','author','link','desc']
# df = pd.DataFrame(columns=cols)

# 저장될 폴더&파일 준비
dirpath = 'scrapped/hani/'
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
fpath = dirpath + 'hani_{0}.csv'.format(now.strftime('%Y-%m-%d_%H:%M:%S'))
with open(fpath, 'w') as f:
    f.write(','.join(cols) + '\n')


selector = {'article':'div.article-area',
            'title':'.article-title a',
            'link':'.article-title a',
            'category':'.category a',
            'date':'.date',
            'author':None,
            'desc':'.article-prologue a'}

# 한겨레 현재시간 전체기사 base url
home_url = "http://www.hani.co.kr"
base_url = "http://www.hani.co.kr/arti/"

# 한 페이지 내 기사목록 스크랩
def scrap_one_page(url, verbose=1):
    # Gets page
    res = requests.get(url)
    if not res.ok:
        print('Request fails. url:', url)
        return
    
    print('Getting articles from', url)
    df = pd.DataFrame(columns=cols)
    
    soup = BeautifulSoup(res.text, 'lxml')
    
    article_list = soup.select('div.article-area')
    # Extracts article details
    for article in article_list:
        title = article.select(selector['title'])[0].text                   #제목
        link = home_url + article.select(selector['link'])[0].get('href')   #링크
        category = article.select(selector['category'])[0].text             #분야
        datestr = article.select(selector['date'])[0].text                  #날짜
        date = datetime.strptime(datestr, '%Y-%m-%d %H:%M')
        author = ''                                                         #작성자
        try:
            desc = article.select(selector['desc'])[0].text                 #짤은요약글
        except:
            desc = ''
        #add all to dataframe
        row = [date,category,title,author,link, desc]
        df.loc[len(df)] = row
        if verbose == 3: print(' ',title) #print title
        
    if verbose >= 2: print(len(df), 'articles added')
    return df

# 페이지별 반복
def scrap_all(pagecount, verbose=1):
    print('\nGetting articles in {0} pages'.format(pagecount))
    for i in range(pagecount):
        page_url = base_url + "list{0}.html".format(i+1)
        df = scrap_one_page(page_url, verbose=verbose)
        df.to_csv(fpath, mode='a', header=False, index=False)
    print("\nSaved at", fpath)
    
scrap_all(3, verbose=3)