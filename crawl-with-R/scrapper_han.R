#setwd("C:/Users/Writer/Desktop/news-analysis/crawl-with-R")

library(rvest)

#target url : "http://www.hani.co.kr/arti/list1.html"
base_url1 <- "http://www.hani.co.kr/arti/list"
base_url2 <- ".html"

page <- 1
filename <- "han.csv"
write("date, category, title", filename)

while(page < 3){
    print(page)
    
    page_url <- paste0(base_url1,page,base_url2)
    han_html <- read_html(page_url)
    
    article_nodes <- html_nodes(han_html,'div.article-area')
    title_node <- html_nodes(article_nodes, 'h4 a')
    date_node <- html_nodes(article_nodes, 'p span.date')
    category_node <- html_nodes(article_nodes, 'strong a')
    
    date <- html_text(date_node)
    category <- html_text(category_node)
    title <- html_text(title_node)
    title <- gsub("^\n\\s+|\\s+$", "", title)
   
    df_this_page <- data.frame(date, category, title)
    print(nrow(df_this_page))
    
    write.table(df_this_page, filename, row.names = F, col.names =  F, sep = ",",
                append=T, qmethod = "escape", fileEncoding = "UTF-8")
    
    page <- page +1
}



