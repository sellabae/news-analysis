#test_chosun.r
print("�����Ϻ���ü��� �������� ����")

library(rvest)

#target url : "http://news.chosun.com/svc/list_in/list_title.html?indate=20200504&pn=1"

base_url1<- "http://news.chosun.com/svc/list_in/list_title.html?indate="
base_url2<- "&pn="
base_url1
base_url2

#�����Ⱓ ��  �����Ϻ� ��ü��� �������� (�� �߰��� �ִ� 1000���� ����) 
date<-20200504
page <- 1
all_chosun_news <- c()

#��¥,�ۼ��� node �߰��ϱ� 
#���� ��¥�� ���������� title20��,date20��,writer 20���� ���� ������ ������ �߻�!! ��� �����ٰ��ΰ�??

while(date <= 20200505){
  while(page< 10){
  
  chosun_url <- paste0(base_url1,date,base_url2,page, encoding='UTF-8')
  
  chosun_html <- read_html(chosun_url)
  
  item <- html_nodes(chosun_html,'dl.list_item')
  
  title_node <- html_nodes(item, 'dt a')
  #�ϴ� ���� ��� ����ְ� ���߿� text ��ȯ�ϴ� �� ���ļ� ���� �ִ� �� �˾ƺ���. )
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

