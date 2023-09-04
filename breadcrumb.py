import pymysql


conn = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8' ,database='test') 
cursor = conn.cursor() 

#첫실행시 db 생성
# create_database = "CREATE DATABASE test" 
# cursor.execute(create_database)
#테이블 생성 

create_article_table  = "CREATE TABLE Article (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,title VARCHAR(255),content VARCHAR(255),parent_id INT(11) NULL,depth INT(11),bread TEXT NULL);"
create_subpage_table = "CREATE TABLE Sub_page (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, data TEXT,Article_id INT(11),  FOREIGN KEY (Article_id) REFERENCES Article(id));"


#db생성, 테이블 생성

#게시글 생성 - 첫 생성글은 부모_id를 null로 지정 

create_article = "INSERT INTO Article (title, content, parent_id ,depth,bread) VALUES ('부모글', '첫번쨰 생성글, 부모x', NULL,0,NULL),('두번쨰', '부모 1번글', 1,1,1),('세번째', '부모 1번글', 1,1,1),('네번째', '부모 2번', 2,2,1/2),('다섯번째', '부모 1번', 1,1,1),('여섯번째', '부모2', 2,2,1/2),('일곱번째', '부모6번', 6,3,1/2/6);"
# create_subpage = "INSERT INTO Sub_page (data,Article_id) VALUES ('부모글', '첫번쨰 생성글, 부모x')"
first_run = [create_article_table,create_subpage_table,create_article]


for i in first_run:
    cursor.execute(i)


# #최초 글 생성 ORM 으로 작성 #첫글 생성로직 
def create(request): # 생성2 
    # article = Article.object.create(title, content, parent_id, depth, bread)
    article = Article.object.create(제목, 컨텐츠, NULL, 1 , NULL ) (최초생성) 
    'INSERT INTO Article (title, content, parent_id,) VALUES ('제목', '컨텐츠', NULL, 1, NUll);'
    # sub_page = sub_page.object.create(서브페이지,참조키)
    sub_page = sub_page.object.create(NULL,article)
    'INSERT INTO sub_page (data, FOREIGN KEY) VALUES ('NULL', '(현재 생생된 아티클 PK)');'


def lower_crete(request,parents_pk): # 조회 2 생성2 변경1 #하위글 생성 로직 
    parents_article= Article.object.get(pk=pk)
    # 'SELECT * FROM Article WHERE id=parents_pk'
    now_article = Article.object.create(title='제목',content='컨텐츠',parent_id = parents_pk, depth=(parents_article.depth +1)bread =f'{bread}/{str(parents_pk)}')    
    # 'INSERT INTO Article (title, content, parent_id) VALUES ('제목', '컨텐츠', parents_article.PK , parents_article.depth+1, parents_article.bread + parents_pk );'
    sub_page = sub_page.object.create(NULL,article) 
    'INSERT INTO sub_page (data, FOREIGN KEY) VALUES ('NULL', '(LAST INSET ID)');' # LAST INSET ID 
    sub_page = sub_page.object.get(fk= parents_pk )
    # 'UPDATE Sub_page  SET DATA = 기존값+본인PK WHERE fk=parents_pk'
    # 'SELECT * FROM Sub_page WHERE fk=parents_pk'
    sub_page.data = (f'{sub_page.data}/{now_article.pk}')
    sub_page.save()


def get_article(request,article_pk): # 조회 2
    article = Article.object.get(pk=article_pk)
    # 'SELECT * FROM Article WHERE id=article_pk'
    sub_page = sub_page.object.get(fk= article_pk )
    # 'SELECT * FROM Sub_page WHERE fk=article_pk'
    sub_page_list= sub_page.data.split('/')

    context= {
        'page_id' : article.pk,
        'title' : article.title,
        'sub_page' : sub_page_list,
        'breadcrumbs' : article.bread
    }
    return context 




# cursor.execute(create_article) 

conn.commit() 
conn.close() 



# 브레드크럼을 만드는 방법,
# 1. 스택에 넣어서 이동할 때 상위페이지를 넣어준다, -> 뒤로가기랑 뭐가다르지?
# 2. DB에 저장시 상위페이지들을 모두 넣는다, 

# -결정-
# 3. 부모와 자식관계로 연결시킨 뒤  DEPTH를 만들어서 자식이된다면 뎁스 +1 ,  부모PK + 본인 뎁스 확인해서 WHERE + - >   DB에 문자열로 그냥 삽입시키자, 
#    서브페이지는 하위페이지가 만들어질때마다 갱신되어야함 - 테이블을 따로 만들어서 사용하자, -> 부모PK 유일하니까  SUB_PAGE -> 만
# -> 서브페이지를 찾아올떄, 모든 DB를 찾아서 가져온다면 시간이?
# -> 해시테이블로 뎁스 분류 후 , 그 안에서 찾아오기? 
# -> 뎁스보다 부모의 게시글 ID로 해시테이블만들기
# -> 부모의 게시글 ID로 해시테이블을 만든 뒤, 서브페이지 찾아오기,
# -결정-
# ->브레드크럼은 각 게시물의 부모노드를 상속시켜서 계속해서 문자열로 이어붙이기, 
# ->서브페이지는 - > 부모의 아이디 + 뎁스의 위치로 서브페이지 찾아오기 -> 이렇게하면 2번 조회하게되는건데 음,,
# 부모노드에 대한 해시테이블을 만들어서 리스트값으로 서브페이지 보여주기,  mysql에서 해시테이블을 어떻게 만들어줘야하는거지? 
# mysql에서는 해시테이블 대신 인덱스검색 사용, 정확값이 값이 일치한다면 빠르다, 범위검색으로 사용하면 느림, 
# 작성시 인덱스 데이터 추가++ 서브페이지의 경우 where + 조건문으로 탐색하는 속도보다 부모페이지와 인덱스를 매핑해서 사용하면 속도향상이 될 것 예상(부모노드에 매핑되어서 정확한 값으로만 조회하기에 속도향상  but 생성,삭제시 추가연산)
#  반대로 게시글은 빈번하게 수정되고 만들어지는 페이지라 CU에서 더 많은 부하가 생김 
# 조회vs생성 그럼 그냥 해시테이블 말고 sub_page 테이블을 만드는게 더 좋을듯? 어차피  부모의 고유값으로 찾아오는거라 인덱스를 만드나 그냥 테이블을 만드나 동일한 속도를 보장하는데 흠,
# 그냥 테이블을 따로 분리시켜서 만들자,  