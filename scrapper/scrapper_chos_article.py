import requests
from bs4 import BeautifulSoup
import lxml

import os
import datetime as dt
from datetime import datetime
import pandas as pd
import re

# local time
print('local', datetime.now())
# 현재 한국 시간
KST = dt.timezone(dt.timedelta(hours=9)) #korean timezone utc+9
now = datetime.now(tz=KST)
print('korea', now)

# 저장될 데이터프레임 준비
cols = ['date','category','title','link','author']

# 저장될 폴더 준비
dirpath = 'scrapped/chosun/'
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
    
selector_chos = {'article':'dl.list_item',
                 'title':'dt a',
                 'category':None,
                 'date':'.date',
                 'author':'.author'}


# 한 페이지에 있는 기사들 가져오기
def get_articles_chos(url, selector, verbose=1):
    # Gets page
    res = requests.get(url)
    res.encoding = 'UTF-8'
    if not res.ok:
        print('Request fails. url:', url)
        return None
    
    if verbose > 0 : print('Getting articles from', url) #print this page
    df = pd.DataFrame(columns=cols)
    soup = BeautifulSoup(res.text, 'lxml')
    
    article_list = soup.select(selector['article'])
    # Extracts article details
    for article in article_list:
        at = article.select(selector['title'])[0]
        link = "https:" + at.get('href')                            #기사링크
        title = at.text                                             #제목
#         category = article.select(selector['category'])[0].text   #분류
        datestr = article.select(selector['date'])[0].text
        datestr = re.sub("\s\(\w*\)$", "", datestr)
        date = datetime.strptime(datestr, '%Y.%m.%d')               #날짜
        try:
            author = article.select(selector['author'])[0].text         #작성자
            author = author.replace('\n','').strip().replace(' 기자','') #문자열 정리
        except:
            author = ''
        #add all to dataframe
        df.loc[len(df)] = [date,'',title,link,author]
        if verbose > 2: print('','',title,link,author) #print this row
        
    return df


# 해당일 전체기사 가져오기
def chos_get_articles_oneday(date, verbose=1):
    if date.date() >= now.replace(tzinfo=None).date():
        print("Not {0} yet.".format(date.date()))
        return
    
    print('\nGet all articles on the day', date.date())
    
    # 조선일보 특정일 전체기사 base url
    datestr = date.strftime('%Y%m%d')
    base_url = "https://news.chosun.com/svc/list_in/list.html?indate={0}".format(datestr)
    print('BaseURL:', base_url)
    
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
# chos_get_articles_oneday(datetime.strptime('2020-04-27','%Y-%m-%d'), verbose=0)
chos_get_articles_days(datetime.strptime('2020-04-27','%Y-%m-%d'), days=7, verbose=0)
# chos_get_articles_days(datetime.strptime('2020-05-04','%Y-%m-%d'), days=7, verbose=0)