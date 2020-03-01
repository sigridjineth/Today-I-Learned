# JPA에 대한 간략적인 정리

### Meaning of Data Persistence in Java

* Persistence is an adjective describing data that outlives the process that created it.
* Java Persistence could be defined as storing Entity model to any level of persistence using Java.
* 데이터베이스를 하나만 활용하는 애플리케이션은 하나의 **EntityManagerFactory** 를 생성한다. 
  * 여러 쓰레드 간의 공유가 가능하다.
  * EntityManager를 생성한다. 왜 Factory가 따로 존재하는지는 잘 모르겠다.
* **EntityManager**(Session) 는 엔티티를 저장하는 메모리 상의 데이터베이스이다.
  * 여러 쓰레드 간의 공유가 불가능하다.

### Persistence Context 영속성 컨텍스트

* 엔티티 Entity = 하나의 테이블에 대응되는 하나의 클래스
* 엔티티 매니저 = (Entity) 객체를 관리하는 역할.

* 영속성 컨텍스트 = JPA가 엔티티 객체를 모아두는 공간
  * 예를 들어, Users 테이블에 10개의 row(userId라고 해보자)가 저장되어 있다면 영속성 컨텍스트에 10개의 엔티티가 생성되고 또 관리되어야 한다.
  * 영속성 컨텍스트는 내부에 캐시가 있어 영속 상태의 엔티티는 이 곳에 모두 저장이 된다고 한다.

![img](https://t1.daumcdn.net/cfile/tistory/24824933598030F436)

![img](https://t1.daumcdn.net/cfile/tistory/99CA54415AE4627A2C)

* 영속성 컨텍스트에는 내부에 1차 캐시가 존재한다. 1차 캐시는 스레드 하나가 시작할 때 생성되고 끝나면 지워진다.

* New: Java 영역에만 존재하고, 데이터베이스와는 매핑되지 않은 상태이다. new 키워드를 활용한다.

* Managed: 영속된 상태라고도 부르는데, 데이터베이스에 저장되고 메모리 상에도 같은 상태로 존재한다. @Id 등으로 지정한 PK 값을 활용하여 데이터를 꺼낼 수 있다. 

  * Persist 메소드를 호출하거나 find 메소드를 호출하면 이루어질 수 있다.
    * 단, persist() 로 데이터베이스에 저장하는 것이 아니라 영속성 컨텍스트에 저장하고 추후에 DB로 commit하는 것이다.
    * 1차 캐시 덕분에 하나의 엔티티를 두 번 조회해도 같은 참조값을 갖는다. 따라서 영속 엔티티의 동일성이 보장된다.
  * "Commit" 이라는 표현을 활용하는 것이 인상적이다. 마치 local repo와 origin repo 사이의 관계를 보는 듯 하다.
  * 다음과 같이 조회를 시도할 경우 Persistent Context를 참조할 뿐, 데이터베이스를 참조하지 않는다.

  ```java
  public static void find(EntityManager em) {
  	Member member = new Member();
  	member.setId("member2");
  	member.setName("회원2");
  	// 1. 1차 캐시에 저장
  	em.persist(member);
  	
  	// 2. 1차 캐시에서 조회
  	Member findMember = em.find(Member.class, "member2");
  	System.out.println(findMember.getName());
  }
  ```

  

  ![img](https://t1.daumcdn.net/cfile/tistory/99CA7D475AE4690217)

  * 영속성 컨텍스트에는 없지만 DB에는 존재할 경우 쿼리 명령을 실행하여 가져온다.

  ```
  public static void find(EntityManager em) {
  	// DB에서 조회
  	Member findMember = em.find(Member.class, "member3");
  	System.out.println(findMember.getName());
  }
  ```

  

  ![img](https://t1.daumcdn.net/cfile/tistory/995DBE475AE46A6A28)

* 왜 이렇게 처리할까? 아마 캐시를 사용하여 DB 접속 필요를 줄임으로써 성능 이슈를 해결하려는 것으로 보인다.

* 쓰기 지연(Lazy writing): 특정 비즈니스에서 update, insert, delete를 여러 번 구현했을 경우, 특정 영역에 캐시로 저장해둔 다음 flush가 되는 순간 한꺼번에 DB로 쿼리를 날릴 수 있다는 장점이 있다고 한다. 이를 **트랜잭션을 지원하는 쓰기 지연** 이라고 부른다.

  * 트랜잭션 내부에서 persist 명령이 발생하면, 엔티티들을 1차 캐시에 넣어두고 INSERT 쿼리를 생성해서 보관한다.
  * commit() 하는 시점에 동시에 DB로 쿼리를 커밋한다(이를 보통 **flush()** 라고 부른다).
    * **flush();** Flushing is the process of synchronizing the underlying persistent store with persistable state held in memory. It will update or insert into your tables in the running transaction, but it may not commit those changes.
    * **Commit();** Commit will make the database commit. When you have a persisted object and you change a value on it, it becomes dirty and hibernate needs to flush these changes to your persistence layer. So, you should commit but it also ends the unit of work (`transaction.commit()`).
      * https://stackoverflow.com/questions/14581865/hibernate-flush-and-commit
    * 여전히 flush와 commit의 차이를 잘 모르겠다. ```git stage``` 와 ```git push``` 의 차이인가?
    * 굳이 이야기하자면 local repo와 origin repo를 일치시키는 sync라고 생각해볼 수 있겠다.

  ```java
  EntityManager em = emf.createEntityManager();
  EntityTransaction transaction = em.getTransaction();
  // 엔티티 매니저는 데이터 변경시 트랜잭션을 시작해야 한다.
  transaction.begin(); // 트랜잭션 시작
  em.persist(memberA);
  em.persist(memberB);
  // 이때까지 INSERT SQL을 데이터베이스에 보내지 않는다.
  // 커밋하는 순간 데이터베이스에 INSERT SQL을 보낸다.
  transaction.commit(); // 트랜잭션 커밋
  
  출처: https://ict-nroo.tistory.com/130 [개발자의 기록습관]
  ```

  

![img](https://github.com/namjunemy/TIL/blob/master/Jpa/inflearn/img/04_transactional_write_behind.PNG?raw=true)

* Removed: DB 상태에서 삭제되었으며, 더 이상 영속 컨텍스트에서도 존재하지 않는다.

* 트랜잭션은 여러 과정을 **하나로 묶을 때** 사용된다고 한다. 따라서 모든 과정은 성공하거나 실패하거나 둘 중 하나만 존재한다.
* 아마 이런 쓰기 지연을 만들어내는 이유는 다음을 꼽을 수 있을 것이다.
  * 쿼리를 모아두었다가 한 번에 DB로 보내면 성능을 높일 수 있다.
  * 모든 사항이 변경되지 않으면 작업을 롤백되어야 할 때 (예를 들어 쇼핑몰에서 결제가 이루어지지 않았는데 앞단에서 구매는 이루어졌다면?) 데이터 결과를 원상태로 복구시키는 데 유용할 것이다.
* 더티 체킹, merge와 detach과 같은 개념은 나중에 학습한다.
  * 더티 체킹: ```git pull``` 처럼 데이터 변화를 감지한다. 1차 캐시를 저장할 때 스냅샷도 저장한다. commit() 또는 flush()가 일어날 때 **엔티티와 스냅샷을 비교**해서, 변경사항이 있으면 UPDATE SQL를 만들어낸다고 한다.
  * detach & merge (준영속 상태와 병합)

### Hibernate Query Language

- 관계형 언어인 SQL과 달리 HQL(Java Persistence Query Language의 Hibernate 구현체)은 객체-관계 매핑(ORM)이 되어있는 친구를 직접 건드리는 역할을 수행한다.

### 연관관계 매핑 ORM

* 엔티티끼리는 서로 관계를 맺고 있다.
  * 예를 들어 Category 엔티티와 Book 엔티티가 있을 때 Category에는 수 많은 Book이 관계를 맺고 있을 것이다.
* 연관관계 매핑은 객체의 참조와 테이블의 외래키를 서로 매핑하는 것을 뜻한다.
  * JPA는 서로 관계에 있는 엔티티 객체를 참조한다.
* 방향과 다중성이라는 개념을 살펴보자.
  * 단방향 관계: 두 엔티티의 관계에서 한 쪽의 엔티티만 참조하고 있는 것을 의미한다. (예: Category-Book)
  * 양방향 관계: 두 엔티티의 관계에서 양 쪽이 서로 참조하고 있는 것을 의미한다. (단방향 2개라고 이해하면 된다.)
  * Many to One : 다대일(N:1)
  * One to Many : 일대다(1:N)
  * One to One: 일대일(1:1)
  * Many to Many: 다대다(N:N)
    * 어떤 엔티티를 중심으로 보느냐에 따라 다중성이 상이하다.
  * 외래키를 갖고 있는 테이블이 연관 관계의 주인이 된다. 연관관계의 주인만이 외래 키를 관리할 수 있다. 주인이 아닌 엔티티는 읽기 권한만 가질 수 있다.
* 예를 들어 One to Many에 대해 살펴보자.

```
@Entity
@Table(name="category")
public class Category {
	@Id
	@Column(name="no")
	@GeneratedValue(strategy=GenerationType.IDENTITY)
	private Integer no;
	
	@Column( name="name", nullable=false, length=100 )
	private String name;

	@OneToMany(mappedBy="category")
	private List<Book> books = new ArrayList<Book>();
	
	// getter , setter 생략
	
}
```

* 카테고리는 책을 리스트로 가지며, @OnetoMany에 mappedBy라는 속성을 추가했다.

* 주인은 mappedBy 속성을 사용할 수 없으므로 주인이 아닌 Category 엔티티의 books 필드에 mappedBy 속성을 사용하여 주인이 아님을 JPA에게 알려준다.

* 카테고리 입장에서는 많은 책을 가진다. 그러므로 @OnetoMany 어노테이션을 달고 books 필드를 category에 매핑한다.

  ```
  @OneToMany( mappedBy = "category“ )
  private List<Book> books = new ArrayList<Book>();
  ```

### 더티 체킹에 대한 간단한 정리

* 일단 엔티티 매니저가 엔티티를 저장하고 조회하고 수정하고 삭제한다.
* 그런데 엔티티 매니저의 메소드에는 persist, find, delete 따위의 쿼리를 날리지 않아도 된다.
* 예를 들어 지난 java-qna step2의 경우에는 PostsService의 update 메소드에서 쿼리를 날리는 부분이 없다.
* 영속성 컨텍스트에 엔티티가 담겨있는 상태에서는 @Transactional 어노테이션이 붙은 경우 트랜잭션이 모두 끝난 경우 데이터베이스에 수정분을 반영한다고 한다.
  * 데이터베이스에 변경 데이터를 저장하는 시점은 1) Transaction commit 시점 2) EntityManager flush 시점 3) JPQL 사용 시점이라고 한다.
* 즉, Entity 객체에 수정만 가하면 DB에 알아서 추가가 된다는 아주 신기한 마법.
  * Dirt - 즉, 더러운 부분 - 이 바로 엔티티 데이터의 변경된 부분이다.
* 더티 체킹이 이루어지기 위해서는 다음 두 가지 조건이 필요하다.
  * Managed 상태에 있는 엔티티여야 하고
  * (서비스 레이어에서) @Transactional 어노테이션을 활용하여 트랜잭션 안에서 엔티티를 변경하는 경우여야 한다.
* @Transactional이 어떻게 작동하는가?
  * Table: Posts에서 PK id 값이 (예를 들어) 1인 Posts 엔티티 객체를 조회한다.
  * Posts의 내용을 변경한다.
  * JPA는 엔티티 조회 시점의 스냅샷을 보유하고 있다고 한다. 이것과 변경내용을 비교해서 변경이 있을 경우 DB에 commit을 한다. 이 때 @Transactional 에서 이루어진 쿼리를 동시에 커밋한다.
    * 질문: JPA는 언제 엔티티를 조회하는가?

```java
@Transactional
  public Long update(Long id, PostsUpdateRequestDto requestDto) {
    Posts posts = postsRepository.findById(id).orElseThrow(
        () -> new IllegalArgumentException("no such post." + " id = " + id));
    posts.update(requestDto.getTitle(), requestDto.getContent());
    return id;
  }
```

* 트랜잭션 커밋 이후, 트랜잭션이 끝나는 시점에 모든 엔티티에 대한 정보를 DB에 반영한다.
  * 트랜잭션이 아닌 상태에서 엔티티 내용이 변경되는 경우

## Reference

* https://en.m.wikibooks.org/wiki/Java_Persistence/What_is_Java_persistence%3F
* https://dzone.com/articles/how-does-spring-transactional
* https://attacomsian.com/blog/spring-data-jpa-query-annotation
* [https://velog.io/@conatuseus/%EC%97%94%ED%8B%B0%ED%8B%B0-%EB%A7%A4%ED%95%91-2-msk0kq84v5](https://velog.io/@conatuseus/엔티티-매핑-2-msk0kq84v5)
* https://gmlwjd9405.github.io/2019/08/03/reason-why-use-jpa.html

- https://tinkerbellbass.tistory.com/24

- https://goddaehee.tistory.com/167
- https://lng1982.tistory.com/273
- https://ict-nroo.tistory.com/130
- https://victorydntmd.tistory.com/208?category=795879
- https://tinkerbellbass.tistory.com/24
- https://hyeooona825.tistory.com/87
- [https://velog.io/@jayjay28/%EC%97%94%ED%8B%B0%ED%8B%B0Entity](https://velog.io/@jayjay28/엔티티Entity)
- [https://velog.io/@conatuseus/%EC%97%B0%EA%B4%80%EA%B4%80%EA%B3%84-%EB%A7%A4%ED%95%91-%EA%B8%B0%EC%B4%88-1-i3k0xuve9i](https://velog.io/@conatuseus/연관관계-매핑-기초-1-i3k0xuve9i)

