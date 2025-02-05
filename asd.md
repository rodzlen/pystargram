# Django-orm
## ORM이란 
객체 관계 매핑으로 OOP에서 사용하는 SQL문 대신 ORM을 사용해 객체간의 매핑을 지원
하나의 모델은 하나의 데이터베이스와 연결되며 모델에서 정의되는 하나의 속성은 하나의 테이블 레코드와 매핑

- 기본적으로 models.Model 클래스를 상속받는다
- 해당 클래스를 인스턴스화 하여 CRUD를 정의한다

### objects 메서드
장고의 모든 모델은 기본적으로 objects라는 Manager를 갖고있음
모델과 데이터베이스 사이의 인터페이스

### query methods(create)
create() -  create는 즉시 db에 반영됨
```django
from myapp.models import Post, User

user = User.objects.get(id=1)  # 기존 유저 가져오기
post = Post.objects.create(content="Hello ORM!", user=user)  # 새 게시글 생성

```

### query methods(Read)
all() -  모든 데이터를 조회 
filter() - where 
get() - 단일 객체 조회로 결과가 2개 이상이면 오류반환

#### 특정 필드값만 반환
values() - 여러개 조회 가능 
```django
post = Post.objects.values('content','user__nickname)

>>> SELECT content,user.nickname FROM post
```

###	집계 함수 
aggregate() - 집합에 대한 연산함수 SUM, AVG, COUNT, MIN/MAX 지원
```django
from django.db.models import Count
queryset = User.objects.aggergate(Count('id'))
>>> {'id__count' : 3} # 이런식으로 표시됨 
```
 결과의 이름을 바꾸고 싶으면 `alias`를 추가할 수 있다.
```django
queryset = User.objects.aggregate(count=Count('id))

>>> {"count": 3}
```

count() - 집계 결과를 세는 함수로 기본적으로 지원  모든 레코드를 집계
aggregate(Count())와의 차이점
- aggregate는 null을 포함하지 않는다. 
- count()는 널값도 포함




join은 기본적으로 foreign으로 연결된 모든 데이터가 조회됨 
이 떄 n+1의 문제가 생긴다

## N+1 문제
n+1이란 추가적인 n개의 쿼리가 발생하는 문제로 
예를들어 연결된 테이블에서 id값만 불러오려고 할 떄 나머지 레코드도 함께 조회된다.
```django
posts = Post.objects.all()  # 1개의 쿼리 실행

for post in posts:
    print(post.user.nickname)  # 각 post마다 user를 조회 → 추가적인 n개의 쿼리 발생

```

select_related() - join 기능
prefetch_related() - 역참조 foreign으로 연관된 정보들 불러옴 sql 요청을 한번 더함 
안하고 가져오게 되면 post를 돌면서 이미지를 가져올 때마다 포스트도 같이 불러오게되는데 위의 두개 메소드 사용하면 n+1문제 해결 