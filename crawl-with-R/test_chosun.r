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
