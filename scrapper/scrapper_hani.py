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
print()

# 저장될 데이터프레임 준비
cols = ['date','category','title','link','author']
# df = pd.DataFrame(columns=cols)

# 저장될 폴더&파일 준비
dirpath = 'scrapped/hani/'
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
fpath = dirpath + 'hani_scrapped_at_{0}.csv'.format(now.strftime('%Y-%m-%d_%H:%M:%S'))
with open(fpath, 'w') as f:
    f.write(','.join(cols) + '\n')


selector_hani = {'article':'div.article-area',
                 'title':'.article-title a',
                 'category':'.category a',
                 'date':'.date',
                 'author':None}

# 한겨레 현재시간 전체기사 base url
home_url = "http://www.hani.co.kr"
base_url = "http://www.hani.co.kr/arti/"

# 한 페이지 내 기사목록 스크랩
def get_articles_hani(url):
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
        at = article.select('.article-title a')[0]
        link = home_url + at.get('href')
        title = at.text
        category = article.select('.category a')[0].text
        datestr = article.select('.date')[0].text
        date = datetime.strptime(datestr, '%Y-%m-%d %H:%M')
        #add all to dataframe
        df.loc[len(df)] = [date,category,title,link,'']
        
    return df

# 페이지별 반복
for i in range(30):
    end_url = "list{0}.html".format(i+1)
    df = get_articles_hani(base_url + end_url)
    df.to_csv(fpath, mode='a', header=False, index=False)

