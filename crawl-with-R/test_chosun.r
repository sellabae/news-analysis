#test_chosun.r
print("조선일보전체기사 가져오기 연습")

library(rvest)



#target url : "http://news.chosun.com/svc/list_in/list_title.html?indate=20200501&pn=1"

base_url<- "http://news.chosun.com/svc/list_in/list_title.html?indate=20200504&pn="
base_url

page <- 1
all_chosun_news <- c()

while(page< 50){
  
  chosun_url <- paste0(base_url, page)
  
  chosun_html <- read_html(chosun_url)
  
  item <- html_nodes(chosun_html,'dl.list_item')
  
  title_node <- html_nodes(item, 'dt a')
  
  chosun_news <- html_text(title_node)
  
  all_chosun_news <- c(all_chosun_news, chosun_news)
  
  write(all_chosun_news, "test_chosun.txt")

  page <- page +1
  
}




for(i in 1:10){
  print(i)
}




왜 반복되지?? ㅠ



##셀라 파이썬 반복문

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




## 네이버 블로그 반복문 사용, 

naver_url_1 <- 'http://news.naver.com/main/list.nhn?sid2=230&sid1=105&mid=shm&mode=LS2D&date='
date <- 20170720:20170721
naver_url_2 <- '&page='
page <- 1:2


news_url <- c()
news_date <-c() 

for (dt in date){
  
  for (page_num in page){
    naver_url <- paste0(naver_url_1,dt,naver_url_2,page_num)
    html <- read_html(naver_url)
    temp <- unique(html_nodes(html,'#main_content')%>%
                     html_nodes(css='.list_body ')%>%
                     html_nodes(css='.type06_headline')%>%
                     html_nodes('a')%>%
                     html_attr('href'))
    news_url <- c(news_url,temp)
    news_date <- c(news_date,rep(dt,length(temp)))
    print(c(dt,page_num))
  }
  
}