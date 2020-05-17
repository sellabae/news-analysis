#setwd("C:/Users/Star of zion/Desktop/news-analysis/crawl-with-R")
base_url1 <- "http://news.chosun.com/svc/list_in/list_title.html?indate="
base_url2 <- "&pn="

startdate <- 20200504
page <- 1
filename <- "chosun.csv"
write("date, title, writer", filename)


while(startdate <= 20200505){
  print(startdate)
  while(page < 3){
    page_url <- paste0(base_url1, startdate, base_url2, page)
    print(page_url)
    
    chosun_html <- read_html(page_url)
    
    article_nodes <- html_nodes(chosun_html,'dl.list_item')
    
    title_node <- html_nodes(article_nodes, 'dt a')
    date_node <- html_nodes(article_nodes, 'dd span.date')
    writer_node <- html_nodes(article_nodes, 'dd span.author')
    
    title <- html_text(title_node)
    date <- html_text(date_node)
    writer <- html_text(writer_node)
    writer <- gsub("^\n\\s+|\\s+$", "", writer)
    
    df_this_page <- data.frame(date, title, writer)
    print(nrow(df_this_page))
    
    write.table(df_this_page, filename, fileEncoding="UTF-8",
                sep=",", row.names=F, col.names=F, append=T, qmethod="double")

    page <- page + 1
  } 
  
  startdate <- startdate + 1
  page <- 1
}


