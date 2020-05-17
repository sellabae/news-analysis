# library(rvest)
# library(xlsx)
# library(rJava)

# 기본변수와 메세지 출력하기
msg <- "Hello World! Let's test R code!"
message(msg)

# 인코딩을 특정해서 csv 파일쓰기
# con <- file('testfile.csv', encoding="UTF-8")
# write.csv(msg, file=con, row.names=FALSE)

# csv파일 읽기
yna <- read.csv('testdata_yna.csv')
# head(yna)
print(typeof(yna))  #데이터타입 확인하기
print(yna[1,1])     #첫줄에 첫컬럼 선택하기

# csv파일 쓰기 (새로덮어쓰기)
# write.csv(yna, file=con, row.names=FALSE)
write.table(yna, file='testfile.csv',
            sep=",", row.names=FALSE)

# csv파일 추가쓰기 (append)
write.table(yna, file='testfile.csv',
            sep=",", row.names=FALSE,
            append=TRUE, col.names=FALSE)
