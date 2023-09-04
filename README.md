# Breadcrumbs
 - notion의 페이지 기능 (breadcrumb,sub_page)기능을 구현


# 방법
- 게시글이 DB에 저장 될 때 breadcrumb경로를 문자열로 저장
- 게시글이 생성 시 sub_page 테이블 데이터를 생성(데이터는 게시글을 FK로 가진다.)
- 게시글이 수정 시 sub_page 테이블에서 게시글의 부모PK를 FK로 가지는 데이터를 업데이트 (기존에 있던 경로 + 본인)
- 최초 루트 게시글 생성 로직과 하위 게시글 생성 로직 2가지로 나눠서 사용

# DB
1. 게시글
 "CREATE TABLE Article 
    (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content VARCHAR(255)
    ,parent_id INT(11) NULL,
    depth INT(11),
    bread TEXT NULL);"
2. 서브페이지
    "CREATE TABLE Sub_page 
    (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    data TEXT,
    Article_id INT(11),
    FOREIGN KEY (Article_id) REFERENCES Article(id));"


