# 자바스크립트 배열에서 forEach, filter, map, reduce 활용법

출처: https://blog.ggaman.com/1012

## 배열을 loop 돌면서 무언가를 하고 싶다면 아래 함수들을 활용하자.

- forEach : 한개씩 돌면서 무언가 하기, return value는 없음.
- filter : 조건에 맞는것만 새로운 배열로. return value는 새 배열.
- map : 한개씩 돌면서 연산한 결과를 새로운 배열로. return value는 새 배열
- reduce : 한개씩 돌면서 이전 연산한 결과를 조합하여 사용하기. return value는 reuce 함수안에서 설정한 대로.
  - 무슨 말인지 이해가 어려울 수도 있는데... 알면 쉬움... ;;

# 간단한, forEach, filter, map 부터

- 이해하기 쉽도록 되도록이면 쉬운 예제를 만들어 보았다.

## forEach - 한개씩 돌면서 무언가 하기

```javascript
["a", "b", "c"].forEach ( 
    function(x) {
        console.log(x);
    }
)
```

- 결과 : 화면에 a, b, c 가 출력 된다.

## filter - 배열에서 조건에 맞는것만 새로운 배열만들어 반환하기.

```javascript
[ 1, 2, 3, 4, 5].filter(
    function(x) {
        return x % 2 == 0;
    }
)
```

- 결과 : [ 2, 4 ] 배열이 반환된다.

## filter + forEach - 조건에 맞는것만 배열로 만들어, 한개씩 돌면서 무언가 처리 하기

```javascript
[ 1, 2, 3, 4, 5].filter(
    function(x) {
        return x % 2 == 0;
    }
).forEach ( 
    function(x) {
        console.log(x);
    }
)
```

- 결과 : 화면에 2, 4 가 출력 된다.

## map - 배열의 각 요소에 무슨짓한 결과를 새 배열로 반환

```javascript
[ 1, 2, 3, 4, 5].map(
    function(x) {
        return x * 2;
    }
)
```

- 결과 : [2, 4, 6, 8, 10] 배열이 반환된다.

## map + forEach - 배열의 각 요소에 어떠한 연산을 하고, 그 결과를 하나씩 돌면서 무슨 짓을 하기

```javascript
[ 1, 2, 3, 4, 5].map(
    function(x) {
        return x * 2;
    }
).forEach ( 
    function(x) {
        console.log(x);
    }
)
```

- 결과 : 화면에 2, 4, 6, 8, 10 이 출력 된다.

## filter + map + forEach - 배열에서 원하는 요소만 뽑아내고, 그 결과 배열에 어떠한 연산을 하고, 그 결과를 하나씩 돌면서 무슨짓을 하기

```javascript
[ 1, 2, 3, 4, 5].filter(
    function(x) {
        return x % 2 == 0;
    }
).map(
    function(x) {
        return x * 2;
    }
).forEach ( 
    function(x) {
        console.log(x);
    }
)
```

- 결과 : 화면에 4, 8 이 출력 된다.

# 조금 까다롭지만 활용성이 매우 좋은 reduce

- reduce는 배열의 순환을 돌면서, 이전 결과를 활용하는 방식이다.
- forEach, filter, map 과 같이 reduce도 내부에서 함수를 1개 받는데, 파라미터에 여러가지 정보가 들어온다.
- 함수는 function ( ac, current, index, array ) 4개의 파라미터를 받는다.
  - ac : reduce 호출할때 넘긴 함수의 결과를 보관. 최초 호출될때는 reduce를 호출할때 두번째 넘김 파라미터의 값.
  - current : 배열의 0 번 부터 배열의 마지막까지 순차적으로 전달 됨
  - index : 현재 배열의 몇번째를 loop 돌고 있는지 알려 주는 값
  - array : reduce 함수를 호출한 배열.
- 긴 설명은 설명이 잘 되어 있는 다른 사이트에서 찾도록 하자.
- reduce 함수에서 위 4가지 파라미터를 활용하면, filter, map, forEach 를 모두 구현할 수 있다.
- 즉, reduce 짱짱임.

## reduce - 숫자가 들어 있는 배열의 합 구하기

```javascript
[1, 2].reduce (
    function ( ac, current, index, array ) {
          // 최초 호출될때, ac는 reduce의 두번째 파라미터인 아래에서 넘긴 0 이고,, current는 배열의 0 번째인 1이 들어 있을 것이다.
          // 그러므로 최초 호출 될 때는 return 값이 0 + 1 이므로, 1이 return 될 것이다.
          // 두번째 호출 될 때는 ac는, 첫번째 호출 되었을때, return한 값인 1 값을 가지고, current는 배열의 1번째 2가 들어 있을 것이다.
          // 그리고 두번째 호출 될 때는 return 값이 1 + 2 인 3 이 될 것이다.
          // 더 이상 loop를 돌 아이템이 없으므로, 해당 함수의 리턴값의 3 이 될 것이다.
        ac = ac + current;
        return ac;
    }
,0); // reduce 함수의 두번째 파라미터인 0 은, 위 익명 함수의 ac에 최초 할당 된다.
```

- 결과 : 3이 반환 될 것이다.

## reduce - string 배열을 순환하면서 모든 배열 item을 1개의 string으로 합치기

```javascript
[ "안녕", "하세요" ].reduce(
    function ( ac, current, index, array ) {
          // 최초 호출될때, ac는 reduce의 두번째 파라미터인 아래에서 넘긴 "" 값을 가지고, current는 배열의 0 번째 "안녕"의 값이 들어 있을 것이다.
          // 그러므로 최초 호출 될 때는 return 값이 "" + "안녕" 이므로, "안녕"이 return 될 것이다.
          // 두번째 호출 될 때는 ac는 첫번째 호출 되었을때, return한 값인 "안녕" 값을 가지고, current는 배열의 1번째 "하세요"가 들어 있을 것이다.
          // 그리고 두번째 호출 될 때는 return 값이 "안녕"+"하세요"가 될 것이다.
          // 더 이상 돌 item이 없으므로, 결과적으로 해당 함수의 return 값은 "안녕하세요"가 될 것이다.
        return ac + current; 
    }
, "" ) // reduce 함수의 두번째 파라미터인 "" 은, 위 익명 함수의 ac에 최초 할당 된다.
```

- 결과 : "안녕하세요" 라는 값이 반환된다.

## 응? reduce 대신 forEach만 써도 되는거 아닌가?

- 위 예제들을 사실, forEach만 사용해도 된다.

- forEach를 사용해서 바로 위의 예제를 구현해 보자.

  ```javascript
  let sumString = ""
  ["안녕", "하세요"].forEach(
      function (x) {
          sumString = sumString + x;
      }
  );
  ```

- 위 예제와 주석이 제거된 reduce를 예제를 비교해 보자.

  ```javascript
  let sumString = [ "안녕", "하세요" ].reduce(
      function ( ac, current, index, array ) {
         return ac + current; 
      }
  , "");
  ```

- 결과는 동일하지만,

  - forEach는 배열의 loop 결과를 저장하기 위해서, sumString을 선언후 ""를 할당한 뒤 사용해야 했지만,
  - reduce는 배열의 loop 결과를 바로, sumString으로 할당 할 수 있다.

## reduce - 배열에서 string type만 Set으로 만들기

```javascript
[ 1, "안녕", "2", 3].reduce(
    function ( ac, current, index, array ) {
          // 최초 호출될때, ac는 reduce의 두번째 파라미터인 아래에서 넘긴 new Set() 값을 가지고, current는 배열의 0 번째 값인 1이 들어 있을 것이다.
          // 1은 string type이 아니므로, 그냥 ac를 반환한다.
          // 두번째 호출 될 때는 ac는 첫번째 호출 되었을때, return한 값인 new Set()이 그대로 들어 있을 것이고, current는 배열의 1번째 값인 "안녕"이 들어 있을 것이다.
          // "안녕"은 string type이므로, ac.add(current)를 이용해서 Set에 "안녕"을 넣는다. 그리고 ac를 반환한다.
          // 세번째 호출 될 때는 ac는 두번째 호출 되었을때, return한 값인 "안녕"이 들어 있는 Set이 들어 있을 것이고, current는 배열의 2번째 값인 "2"이 들어 있을 것이다.
          // "2"은 string type이므로, ac.add(current)를 이용해서 Set에 "2"을 넣는다. 이제 Set에는 "안녕"과 "2"가 들어 있다. 그리고 ac를 반환한다.
          // 네번째 호출 될 때는 ac는 세번째 호출 되었을때, return한 값인 "안녕"과 "2"가 들어 있는 Set이 들어 있을 것이고, current는 배열의 3번째 값인 3 이 들어 있을 것이다.
          // 3은 string type이 아니므로, "안녕"과 "2"가 들어 있는 ac를 반환한다.
          // 더 이상 돌 item이 없으므로, "안녕"과 "2"가 들어 있는 ac를 최종 반환하고 끝낸다.
        if ( typeof current == "string" ) {
            ac.add(current);
        }
        return ac;
    }
, new Set()); // reduce 함수의 두번째 파라미터인 new Set()은, 위 익명 함수의 ac 에 최초 할당된다.
```

- 결과 : "안녕"과 "2"가 들어 있는 Set이 반환된다.

## 위 예제도, filter와 map 같은걸로 가능할 것 같은데?

- 당근 가능하다. 위 예제는 Set을 반환했지만, filter + map과 reduce의 비교를 위해, 배열을 반환하도록 코드를 수정하겠다. 그리고 각 배열의 마지막에 "하세요"라는 문자를 추가하도록 하겠다.

- 우선 filter + map 을 사용해서, 배열에서 string type만 array로 만들어 보자.

  ```javascript
  [ 1, "안녕", "미안", 3].filter(
      function ( x ) {
         return typeof x == "string";
      }
  ).map(
      function ( x ) {
         return x + "하세요";
      }
  );
  ```

- 그리고 reduce를 활용해, 배열에서 string type만 array로 만들어 보자..

  ```javascript
  [ 1, "안녕", "미안", 3].reduce(
      function ( ac, current, index, array ) {
         if ( typeof current == "string" ) {
             ac.push(current + "하세요");
         }
         return ac;
      }
  , []);
  ```

- 결과는 동일하지만,

  - filter와 map의 조합은 결과를 내기 위해서 배열의 loop를 두번 돌아야 하고, 정확하게는 item 을 6번 가지고 와야 한다. ( filter에서 4번, map에서 2번)
  - reduce는 배열을 한번의 loop를 돌면서 결과를 만들어 낼 수 있다. 정확하게는 item을 4번 가지고 오면 된다.

# 결론?

- 처음에는 공부하기도 귀찮고 해서, 안 썼었는데...
- 다른 강좌를 보다가 예제중에서 이걸 사용하는것들이 있어, 공부를 하게 됐다.
- 지금은?
  - 거의 모든 배열의 loop는 이 함수들을 이용해서 처리하고 있다.
  - 익숙해 지니깐, 참 편하더라고...