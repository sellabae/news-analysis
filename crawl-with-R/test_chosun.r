#test_chosun.r
print("조선일보전체기사 가져오기 연습")

library(rvest)



#target url : "http://news.chosun.com/svc/list_in/list_title.html?indate=20200501&pn=1"

base_url1<- "http://news.chosun.com/svc/list_in/list_title.html?indate="
base_url2<- "&pn="
base_url1
base_url2

#일정기간 중  조선일보 전체기사 가져오기 (일 발간수 최대 1000개로 가정) 
date<-20200504
page <- 1
all_chosun_news <- c()

while(date <= 20200505){
  while(page< 50){
  
  chosun_url <- paste0(base_url1,date,base_url2,page)
  
  chosun_html <- read_html(chosun_url)
  
  item <- html_nodes(chosun_html,'dl.list_item')
  
  title_node <- html_nodes(item, 'dt a')
  
  chosun_news <- html_text(title_node)
  
  all_chosun_news <- c(all_chosun_news, chosun_news)
  
  write(all_chosun_news, "test_chosun.txt")

  page <- page +1
  } 
  date <- date +1
  page<- 1
}
