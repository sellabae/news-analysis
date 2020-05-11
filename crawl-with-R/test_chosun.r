

install.packages('utf8')
library(utf8)

print("조선일보전체기사 가져오기 연습")

install.packages('rvest')
library(rvest)


url0 <- ("http://news.chosun.com/svc/list_in/list_title.html?indate=20200504&pn=1")
chosun <- read_html(url0)
item <- html_nodes(chosun, "dl.list_item")
titlenode<-html_nodes(item, "dt a")
title <-html_text(titlenode)

write(title, "chosun200504.txt")

#조선일보 url 특성, indate=날짜 &pn=페이지넘버 



http://news.chosun.com/svc/list_in/list_title.html?indate=20200505&pn=2