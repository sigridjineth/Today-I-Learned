# CS16 Day 5 TDD와 객체지향 프로그래밍

### 학습사항

* Day 5 TDD 기반해서 구현해보기 - 1단계 (다른 사람의 테스트 따라 만들기)
* 객체지향 알아보기 - 생활코딩 Java 강의 기반

### 대체 TDD, 어떻게 하는거지..

* 포비님의 발표자료를 참고하여 학습하자.

  * https://okky.kr/article/476113
  * https://www.slideshare.net/OKJSP/okkycon-tdd
  * https://wikidocs.net/224

* 자바 JUnit에서 assertThat의 쓰임에 대해 알아본다.

  * **assertThat** will tell you what the assertion was and what you got instead. **assertTrue** will only tell you that you got false where you expected true.
  * assertThat은 assertTrue에 비해 확장판(?)인 것 같다. assertTrue는 boolean 값을 반환하지만, assertThat은 두 값을 비교해주는 역할을 한다.
  * assertThat의 일반적인 사용법은 다음과 같다.

  ```java
  assertThat(테스트대상, Matcher구문);
  assertThat("메시지", 테스트대상, Matcher구문);
  ```

* 자바 JUnit에서 예외 테스트를 수행하는 방법에 대해 알아본다.

  * **JUnit의 ExpectedException** Rule을 사용한다.
  * https://blog.outsider.ne.kr/659
  * https://advenoh.tistory.com/32
  * http://wonwoo.ml/index.php/post/1524

* substring

* Matcher.start(), Matcher.end()

