#test_chosun.r
print("한겨레 크롤링 연습")

install.packages("xlsx")
install.packages("rJava")
library(rvest)
library(xlsx)
library(rJava)

#target url : "http://www.hani.co.kr/arti/list1.html"

base_url1<- "http://www.hani.co.kr/arti/list"
base_url2<- ".html"

page <- 1
all_han_news <- c()

while(page< 50){
    
    han_url <- paste0(base_url1,page,base_url2)
    
    han_html <- read_html(han_url, encoding="UTF-8")
    
    item <- html_nodes(han_html,'div.article-area')
    
    title_node <- html_nodes(item, 'h4 a')
  
    date_node <- html_nodes(item, 'p span.date')
    
    title <- html_text(title_node)
    date<- html_text(date_node)
   
    all_text <- data.frame(date,title)
    
    all_han_news <- rbind(all_han_news, all_text)
    
    page <- page +1
}

write.xlsx(all_han_news, "testhan0515.xlsx", sheetName = "han0515_", row.names = F, append=T)



