

install.packages('utf8')
library(utf8)

print("�����Ϻ���ü��� �������� ����")

install.packages('rvest')
library(rvest)


url0 <- ("http://news.chosun.com/svc/list_in/list_title.html?indate=20200504&pn=1")
chosun <- read_html(url0)
item <- html_nodes(chosun, "dl.list_item")
titlenode<-html_nodes(item, "dt a")
title <-html_text(titlenode)

write(title, "chosun200504.txt")

#�����Ϻ� url Ư��, indate=��¥ &pn=�������ѹ� 



http://news.chosun.com/svc/list_in/list_title.html?indate=20200505&pn=2