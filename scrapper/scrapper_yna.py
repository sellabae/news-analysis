# -*- coding: UTF-8 -*-
#  연합뉴스 yna.co.kr 기사제목 크롤러
#  카테고리별 '전체기사' 코너가 날짜구분없이 최신뉴스 순서대로 있음

import requests
from bs4 import BeautifulSoup
import lxml

import os
import datetime as dt
from datetime import datetime
import pandas as pd
import re

# 스크래핑 --------------------------------------------------------
print('연합뉴스 기사 제목 스크래퍼')

# 연합뉴스 기사 URL
home_url = "https://www.yna.co.kr/"
print('HOME URL:', home_url)

# local time
print('local now', datetime.now())
# 현재 한국 시간
KST = dt.timezone(dt.timedelta(hours=9)) #korean timezone utc+9
now = datetime.now(tz=KST)
print('korea now', now)

# 기사 목록 선택자
selector_yna = {'article':'.section01 .list div.item-box01',
                 'title':'.tit-news',
                 'link': 'a.tit-wrap',
                 'category': None,
                 'date':'.txt-time',
                 'author': None,
                 'desc':'p.lead'}

categories = {'politics':   '정치',
              'economy':    '경제',
              'industry':   '산업',
              'society':    '사회',
              'local':      '전국',
              'international':'세계',
              'culture':    '문화',
              'lifestyle':  '라이프',
              'entertainment':'연예',
              'sports':     '스포츠'}
def get_url(cat):
    return home_url + cat + "/all"

# 저장될 데이터프레임 준비
cols = ['date','category','title','author','link','desc']

# 저장될 폴더 준비
dirpath = 'scrapped/yna/'
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
# 저장할 파일 준비
fpath = dirpath + 'yna_{0}.csv'.format(now.strftime('%Y%m%d_%H%M%S'))
with open(fpath, 'w') as f:
    f.write(','.join(cols) + '\n')


# 한 페이지 스크랩, return dataframe
def scrap_one_page(url, selector, verbose=1):
    # Gets page
    res = requests.get(url)
    if not res.ok:
        print('Request fails. url:', url)
        return
    if verbose >= 1: print('Getting articles from', url) #show page url
    df = pd.DataFrame(columns=cols)
    soup = BeautifulSoup(res.text, 'lxml')

    article_list = soup.select(selector['article'])
    # Extracts article details
    for article in article_list:
        #get each part
        link = 'https:' + article.select(selector['link'])[0].get('href')   #기사링크
        title = article.select(selector['title'])[0].text                   #제목
        category = ''                                                       #분류
        datestr = article.select(selector['date'])[0].text
        date = datetime.strptime(datestr, '%m-%d %H:%M').replace(year=2020) #날짜
        desc = article.select(selector['desc'])[0].text   #짤은요약글
        desc = desc.replace('\n',' ')
        author_match = re.findall("\(.{1,4}=.{1,4}\)\s.{1,15}\s=\s", desc) #'(..=..).. = ' 패턴 찾기
        author = re.sub(" = ", "", author_match[0]) if len(author_match) else ''    #작성자
        #add all to dataframe
        row = [date,category,title,author,link,desc]
        df.loc[len(df)] = row
        if verbose == 3: print(' ',title) #print title
        if verbose >= 4: print(' ',row) #print this row
        
    if verbose >= 2: print(len(df), 'articles added')
    return df


# 특정 카테고리의 '전체기사'코너에서 페이지 넘기며 모든 기사 스크랩
def scrap_articles_by_cat(category, verbose=1, page_limit=10):
    cat_ko = categories[category]
    print("\nGet all articles in '{0}' section".format(cat_ko))
    
    i = 0
    while True:
        if page_limit and i >= page_limit: break
        page_url = get_url(category) + '/' + str(i+1)    # https://www.yna.co.kr/카테고리/all/페이지번호
        df = scrap_one_page(page_url,
                            selector=selector_yna,
                            verbose=verbose)
        if df.empty: break
        df['category'] = cat_ko
        df.to_csv(fpath, mode='a', header=False, index=False)
        i += 1
    print("Chekced "+i+" pages")


# 모든 카테고리에서 '전체기사'코너의 모든 기사 스크랩
def scrap_articles_all_cat(verbose=1, page_limit=10):
    print("\nGet all articles in all categories!", ','.join(categories.values()))
    for cat in categories.keys():
        scrap_articles_by_cat(cat, verbose=verbose, page_limit=page_limit)
    print("\nSaved at", fpath)


# Run the program
scrap_articles_all_cat(page_limit=3)
