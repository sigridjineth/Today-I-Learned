# JPA Auditing에 대한 간략한 정리

## Auditing

```
I have seen projects storing these things manually and doing so become very complex because you will need to write it completely by your own which will definitely require lots of code and lots of code means less maintainability and less focus on writing business logic.
```

* Many attempt to reduce the burden of reiterating the codes to support business logic to focus on it. 역시 프로그래머들이란..

* Spring Data JPA provides support for keeping track of who created or changed an entity and the point of the time that this happened.
* Using EntityListeners, JPA automatically audits and logs the change, thanks to Spring Data automates it.

## Basic Annotations

* Spring Data JPA project has the following built-in annotations: @CreateBy, @CreatedDate, @LastModifiedBy, @LastModifiedDate.
* We could create ```Auditable``` abstract class for implementing the annotations, and letting other classes to use the interface by inheriting it.

## JPA Lifecycle Callback methods

* 리스너: 모든 엔티티를 대상으로 언제 어떤 사용자가 수정했고 이를 시간으로 남겨야 하는 요구 사항이 있다고 가정하자. 로직을 하나씩 찾아서 로그를 남기는 것은 비효율적이므로, JPA에 있는 리스너의 기능을 사용한다. 엔티티의 생명주기에 따라 이벤트를 처리할 수 있다고 한다.

* @PrePersist : Entity is going to be notified only when ```persist``` method is called.
* @PostPersist : The status after a entity is pushed or committed to database. It occurs for an entity after the entity has been made persistent.
* @PreUpdate: The status before a entity calls commit or push to update its information to database, but a entity is modified.
* @PostUpdate : The status after a entity calls commit or push to update its information to database.
  * Not clear the difference between @PostPersist

```java
@Entity
public class Employee {
 
	@TableGenerator(name = "employee_gen", pkColumnName = "gen_name", valueColumnName = "gen_val", allocationSize = 1,table="id_gen")
	@Id
	@GeneratedValue(generator = "employee_gen", strategy = GenerationType.TABLE)
	private int idEmployee;
 
	private String firstName;
	private String lastName;
	private int salary;
 
	public int getIdEmployee() {
		return idEmployee;
	}
 
	public void setIdEmployee(int idEmployee) {
		this.idEmployee = idEmployee;
	}
 
	public String getFirstName() {
		return firstName;
	}
 
	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}
 
	public String getLastName() {
		return lastName;
	}
 
	public void setLastName(String lastName) {
		this.lastName = lastName;
	}
 
	public int getSalary() {
		return salary;
	}
 
	public void setSalary(int salary) {
		this.salary = salary;
	}
 
	@PrePersist
	public void methodInvokedBeforePersist() {
		System.out.println("Invoked before persisting employee");
	}
 
	@PostPersist
	public void methodInvokedAfterPersist() {
		System.out.println("Invoked after persisting employee");
	}
 
	@PreUpdate
	public void methodInvokedBeforeUpdate() {
		System.out.println("Invoked before updating employee");
	}
 
	@PostUpdate
	public void methodInvokedAfterUpdate() {
		System.out.println("Invoked after updating employee");
	}
 
	@PreRemove
	public void methodInvokedBeforeRemove() {
		System.out.println("Invoked before removing employee");
	}
 
	@PostRemove
	public void methodInvokedAfterRemove() {
		System.out.println("Invoked after removing employee");
	}
 
}
```

```java
Employee employee = new Employee();
employee.setFirstName("prasad");
employee.setLastName("kharkar");
employee.setSalary(100000);
 
em.persist(employee);
int idEmployee = employee.getIdEmployee();
transaction.commit();
 
transaction.begin();
 
employee = (Employee) em.find(Employee.class, idEmployee);
employee.setSalary(employee.getSalary() + 10000);
transaction.commit();
		
transaction.begin();
em.persist(employee);
em.remove(employee);
transaction.commit();

//Invoked before persisting employee
//Invoked after persisting employee
//Invoked before updating employee
//Invoked after updating employee
//Invoked before removing employee
//Invoked after removing employee
```

* 콜백 메서드로 auditing을 구현할 수 있다.

```java
//AuditorListener.class
//Implement Auditable inferface (or AbstractAuditable) class

@Entity
public class Bar {
    @Column(name = "operation")
    private String operation;
      
    @Column(name = "timestamp")
    private OffsetDateTime timestamp;
    
    @PrePersist
    public void onPrePersist() {
        audit("INSERT");
    }
      
    @PreUpdate
    public void onPreUpdate() {
        audit("UPDATE");
    }
      
    @PreRemove
    public void onPreRemove() {
        audit("DELETE");
    }
      
    private void audit(String operation) {
        setOperation(operation);
        setTimestamp(OffsetDateTime.now());
    }
}

//https://www.baeldung.com/database-auditing-jpa
```

## JPA EntityListeners

* JPA EntityListeners are classes where JPA lifecycle callback methods are implemented using annotations.
* 엔티티 리스너는 특정 칼럼의 변화를 감지해 데이터를 변화시키고 로그 테이블에 저장하는 수고를 덜어준다.
  * 엔티티 리스너를 직접 만들어보는 사람들도 있다. [https://bum752.github.io/posts/JPA-entity-listener-%EB%A7%8C%EB%93%A4%EA%B8%B0/](https://bum752.github.io/posts/JPA-entity-listener-만들기/)
* 원래는 위에서 콜백 메소드로 리스너를 직접 구현하고 ```@EntityListeners (AuditListener.class)``` 로 직접 선언해주어야 한다.
  * JPA는 `@EntityListeners` 어노테이션을 통해 특정 콜백 리스너를 지정할 수 있다.
  * 콜백 리스너를 다음과 같이 이해했다.
    * 콜백(Callback) : 어느 특정 이벤트가 발생하면 특정 메소드를 호출한다.
      * The other code tells the developer: Hey, if this event occurs, I'll call the function in this bucket. You must know where the bucket is to connect your callback.
    * 리스너(Listener): 어느 특정 이벤트가 발생하면 연결된 리스너(핸들러)들에게 이벤트를 전달한다.
      * The other code tells the developer: Hey, if this thing occurs, I'll send this event. You can connect your handler (hopefully) where it makes sense to you.
    * http://shuklaxyz.blogspot.com/2012/07/what-is-difference-between-callbacks.html
    * 즉, 엔티티 리스너는 엔티티에 특정 변화나 변동이 있을 경우 연결된 리스너/핸들러에게 이와 같은 사실을 통지하는 역할을 수행한다.
* 그런데 Spring Data JPA는 ```AuditingEntityListener``` 를 직접 제공한다.
  * Spring Data JPA provides a JPA entity listener class, **AuditingEntityListener**, which contains the callback methods (annotated with the **@PrePersist** and **@PreUpdate** annotations), which will be used to persist and update these properties when we will persist or update our entity.
  * **Spring Data JPA** ships with an **entity listener** that can be used to trigger capturing **auditing** information. https://docs.spring.io/spring-data/jpa/docs/1.7.0.DATAJPA-580-SNAPSHOT/reference/html/auditing.html

* 스프링 Data 3.5 버전부터는 ```@EnableJpaAuditing``` 을 붙여 configuration을 마칠 수 있다.
  * ```@EnableJpaAuditing``` 은 생성일(```@createdAt```), 수정일(```@modifiedAt```), 작성자(```@createdBy```), 수정자 (```@modifiedBy```) 등의 정보를 가져오는 생성자를 자동으로 주입하는 역할을 수행한다. 
* 일단 뭐가 많으니까 여기까지만 정리한다. JPA를 따로 깊이있게 공부하는 이유가 뭔지 좀 알 것 같기도 ^^
  1. 모든 엔티티는 생명주기가 존재한다.
  2. EntityListener 클래스를 통해 콜백 리스너를 지정한다. 생명 주기에 변동과 수정사항이 발생하는 이벤트가 발생할 경우 지정된 리스너에게 이벤트 발생 사실을 고지받는다.
  3. Spring Data JPA는 ```AuditingEntityListener``` 라는 리스너를 미리 만들어두었다. 이를 가져다 사용하면 된다.

## More links...

* 자바에서의 콜백 http://www.dreamy.pe.kr/zbxe/CodeClip/3768942
* ```@EnableJpaAuditing``` https://docs.spring.io/spring-data/commons/docs/current/api/org/springframework/data/annotation/CreatedDate.html
* https://eclipse4j.tistory.com/201
* http://www.thejavageek.com/2014/05/24/jpa-entitylisteners/
* http://wonwoo.ml/index.php/post/995
* https://docs.spring.io/spring-data/data-jpa/docs/current/api/org/springframework/data/jpa/domain/support/AuditingEntityListener.html
* https://blusky10.tistory.com/316
* https://gist.github.com/dlxotn216/94c34a2debf848396cf82a7f21a32abe
* https://attacomsian.com/blog/spring-data-jpa-auditing
* https://dev.to/njnareshjoshi/jpa-auditing-persisting-audit-logs-automatically-using-entitylisteners-238p
* https://docs.spring.io/spring-data/jpa/docs/1.7.0.DATAJPA-580-SNAPSHOT/reference/html/auditing.html