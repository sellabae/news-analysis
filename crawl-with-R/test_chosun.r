#test_chosun.r
print("조선일보전체기사 가져오기 연습")

library(rvest)

#target url : "http://news.chosun.com/svc/list_in/list_title.html?indate=20200504&pn=1"

base_url1<- "http://news.chosun.com/svc/list_in/list_title.html?indate="
base_url2<- "&pn="
base_url1
base_url2

#일정기간 중  조선일보 전체기사 가져오기 (일 발간수 최대 1000개로 가정) 
date<-20200504
page <- 1
all_chosun_news <- c()

#날짜,작성자 node 추가하기 
#같은 날짜에 한페이지씩 title20개,date20개,writer 20개가 따로 나오는 문제가 발생!! 어떻게 합쳐줄것인가??

while(date <= 20200505){
  while(page< 10){
  
  chosun_url <- paste0(base_url1,date,base_url2,page, encoding='UTF-8')
  
  chosun_html <- read_html(chosun_url)
  
  item <- html_nodes(chosun_html,'dl.list_item')
  
  title_node <- html_nodes(item, 'dt a')
  #일단 각각 노드 잡아주고 나중에 text 변환하는 것 합쳐서 쓸수 있는 지 알아보자. )
  date_node <- html_nodes(item, 'dd span.date')
  writer_node <-html_nodes(item, 'dd span.author')
  
  title_text <- html_text(title_node)
  date_text <- html_text(date_node)
  writer_text<- html_text(writer_node)
  
  all_text <- data.frame(title_text,date_text,writer_text)
  
  all_chosun_news <- c(all_chosun_news, all_text)
  
  write.csv(all_chosun_news, "test_chosun.csv", row.names = F, fileEncoding = "cp949")
  
  page <- page +1
  } 
  date <- date +1
  page<- 1
}

