# -*- coding: UTF-8 -*-
#  조선일보 news.chosun.com 전체기사 코너 날짜별 기사제목 크롤러

import requests
from bs4 import BeautifulSoup
import lxml

import os
import sys
import datetime as dt
from datetime import datetime
import pandas as pd
import re

#프로그램 실행부
args = sys.argv
if len(args) < 3:
    print('Use: -.py [yyyy-mm-dd] [days]')
    sys.exit()
arg_startdate = args[1]
arg_days = int(args[2])

# 스크래핑 --------------------------------------------------------
print('조선일보 기사 제목 스크래퍼')

# local time
print('local', datetime.now())
# 현재 한국 시간
KST = dt.timezone(dt.timedelta(hours=9)) #korean timezone utc+9
now = datetime.now(tz=KST)
print('korea', now)

# 저장될 데이터프레임 준비
cols = ['date','category','title','author','link','desc']

# 저장될 폴더 준비
dirpath = 'scrapped/chosun/'
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
    
selector_chos = {'article':'dl.list_item',
                 'title':'dt a',
                 'category':None,
                 'date':'.date',
                 'author':'.author',
                 'desc':'.desc'}


# 한 페이지 스크랩, return dataframe
def get_articles_chos(url, selector, verbose=1):
    # Gets page
    res = requests.get(url)
    res.encoding = 'UTF-8'
    if not res.ok:
        print('Request fails. url:', url)
        return None
    
    if verbose > 0 : print('Getting articles from', url) #show page url
    df = pd.DataFrame(columns=cols)
    soup = BeautifulSoup(res.text, 'lxml')
    
    article_list = soup.select(selector['article'])
    # Extracts article details
    for article in article_list:
        at = article.select(selector['title'])[0]
        link = "https:" + at.get('href')                            #기사링크
        title = at.text                                             #제목
        category = ''                                               #분류
        datestr = article.select(selector['date'])[0].text
        datestr = re.sub("\s\(\w*\)$", "", datestr)
        date = datetime.strptime(datestr, '%Y.%m.%d')               #날짜
        try:
            author = article.select(selector['author'])[0].text     #작성자
            author = author.replace('\n','').strip()
        except:
            author = ''
        desc = article.select(selector['desc'])[0].text             #짧은설명
        #add all to dataframe
        row = [date,category,title,author,link,desc]
        df.loc[len(df)] = row
        if verbose >= 2: print(' ',title) #print this row
        
    return df


# 특정 날짜의 '전체기사' 코너의 기사 모두 가져오기
def chos_get_articles_oneday(date, verbose=1):
    # 유효한 날짜인지 확인
    if date.date() >= now.replace(tzinfo=None).date():
        print("Not valid date {0}".format(date.date()))
        return
    
    print('\nGet all articles on the day', date.date())
    
    # 조선일보 특정일 전체기사 base url
    datestr = date.strftime('%Y%m%d')
    base_url = "https://news.chosun.com/svc/list_in/list.html?indate={0}".format(datestr)
    print('BaseURL:', base_url)
    
    # 파일 생성후 컬럼 이름 출력
    fpath = dirpath + 'chos_{0}.csv'.format(datestr)
    with open(fpath, 'w') as f:
        f.write(','.join(cols) + '\n')

    # 해당일자 전체기사 페이지 전체 반복
    i = 1
    while True:
        page_url = base_url + "&pn={0}".format(i)
        df = get_articles_chos(page_url, selector=selector_chos, verbose=verbose)
        if df.empty:
            break
        df.to_csv(fpath, mode='a', header=False, index=False)
        i += 1
    print("Checked through {0} pages".format(i))
    print("Saved articles in '{0}'".format(fpath))
    

# 일정기간 중 전체기사 가져오기
def chos_get_articles_days(startdate, days=7, verbose=1):
    enddate = startdate+dt.timedelta(days=days-1)
    print('Fetch articles from {0} to {1}. {2} days.'.format(
        startdate.date(), enddate.date(), days))
    
    for i in range(days):
        date = startdate + dt.timedelta(days=i)
        chos_get_articles_oneday(date, verbose=verbose)


# 스크래퍼 실행
chos_get_articles_days(datetime.strptime(arg_startdate,'%Y-%m-%d'), days=arg_days, verbose=0)