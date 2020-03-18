## [JavaScript] Rest Parameter, Arguments, and Spread Parameter

> Rest 파라미터 (Rest Parameter)**

Rest 파라미터는 Spread 연산자(...)를 사용하여 함수의 파라미터를 작성한 형태를 말한다. 즉, Rest 파라미터를 사용하면 함수의 파라미터로 오는 값들을 "배열"로 전달받을 수 있다.

(Java에서 public static void func(String... strs){...} 이런식의 가변인자와 유사)

사용 방법은 파라미터 앞에 (...)을 붙인다.

| 12345 | function foo(...rest) {  console.log(Array.isArray(rest)); // true  console.log(rest); // [ 1, 2, 3, 4, 5 ]}foo(1, 2, 3, 4, 5); |      |
| ----- | ------------------------------------------------------------ | ---- |
|       |                                                              |      |

\* function foo(param1, param2, ...rest){~~} 처럼 앞에 파라미터는 일반적인 파라미터로 받을 수 있고 그 뒤부터는 Rest 파라미터로 받을 수 있다.

\- 단, Rest파라미터는 항상 제일 마지막 파라미터로 있어야 한다. 예를들어 function foo(...rest, param1, param2){~}는 사용 불가능하다.

> **arguments VS rest 파라미터**

ES5에서도 가변 인자 함수의 경우 arguments 객체를 통해 인자값을 확인할 수 있었다.

| 1234 | var foo = function () {  console.log(arguments);};foo(1, 2); // { '0': 1, '1': 2 } |      |
| ---- | ------------------------------------------------------------ | ---- |
|      |                                                              |      |

그렇다면 arguments와 rest파라미터의 차이점은 무엇일까?

답부터 말하면 arguments는 유사 배열 객체고 rest는 배열이다.

유사 배열 객체(array-like object)는 간단하게 순회가능한(iterable) 특징이 있고 length 값을 알 수 있는 특징이 있는 것이다. 즉, 배열처럼 사용할 수 있는 객체를 말한다.

무슨 말이냐면 arguments는 유사배열객체이기 때문에 Array 오브젝트의 메서드를 사용할 수 없다.

따라서 ES6에서는 arrow function에 arguments는 사용할 수 없을 뿐더러 Rest 파라미터를 사용하면 더 유연한 코드를 작성할 수 있는 것이기 때문에 Rest 파라미터 사용을 권장한다.

> **Spread 연산자 (Spread Operator)**

Spread 연산자는 연산자의 대상 배열 또는 이터러블(iterable)을 "개별" 요소로 분리한다.

| 123456789 | // 배열console.log(...[1, 2, 3]); // -> 1, 2, 3 // 문자열console.log(...'Helllo');  // H e l l l o // Map과 Setconsole.log(...new Map([['a', '1'], ['b', '2']]));  // [ 'a', '1' ] [ 'b', '2' ]console.log(...new Set([1, 2, 3]));  // 1 2 3[Colored by Color Scripter](http://colorscripter.com/info#e) |      |
| --------- | ------------------------------------------------------------ | ---- |
|           |                                                              |      |

이터러블(iterable)은 Array, String, Map, Set, DOM구조다.

iterator를 생성해서 next()로 순회할 수 있는 자료구조가 이터러블이라고 생각하면 된다.

\* 함수의 파라미터로 사용하는 방법

| 12345678 | // ES6function foo(x, y, z) {  console.log(x); // 1  console.log(y); // 2  console.log(z); // 3}const arr = [1, 2, 3];foo(...arr);// Array를 받아서 각 매개변수로 전달되었다. |      |
| -------- | ------------------------------------------------------------ | ---- |
|          |                                                              |      |

> **Rest와 헷갈리지 않기!**

Rest는 함수 선언문의 파라미터에 Spread(...)연산자를 이용해서 받으면 가변인자를 받아 배열로 만들어서 사용하는 것이고, 함수 호출문의 파라미터에 Spread(...)연산자를 이용해서 호출하면 배열이 해당 매개변수로 각각 매핑되는 것은 다르다.

| 1234567891011121314 | //Restfunction foo(param, ...rest) {  console.log(param); // 1  console.log(rest);  // [ 2, 3 ]}foo(1, 2, 3); //Spread호출function bar(x, y, z) {  console.log(x); // 1  console.log(y); // 2  console.log(z); // 3}bar(...[1, 2, 3]); |      |
| ------------------- | ------------------------------------------------------------ | ---- |
|                     |                                                              |      |

\- 또한 Rest에서는 선언에서 Spread연산자를 제일 뒤에만 써야하지만, Spread호출에서는 중간중간 사용해도 상관없다.

\* **배열에서 사용하는 방법 (가독성UP)**

| 12345678 | //ES5var arr = [1, 2, 3];console.log(arr.concat([4, 5, 6])); // [ 1, 2, 3, 4, 5, 6 ] // ES6const arr = [1, 2, 3];// ...arr은 [1, 2, 3]을 개별 요소로 분리한다console.log([...arr, 4, 5, 6]); // [ 1, 2, 3, 4, 5, 6 ] |      |
| -------- | ------------------------------------------------------------ | ---- |
|          |                                                              |      |

\- concat() 대신 가독성이 더 좋아졌다.

| 1234567891011121314151617 | // ES5var arr1 = [1, 2, 3];var arr2 = [4, 5, 6]; // apply 메소드의 2번째 인자는 배열. 이것은 개별 인자로 push 메소드에 전달된다.//Array.prototype.push.apply(arr1, arr2);//arr1.push(arr2); => [1,2,3,[4,5,6]]console.log(arr1); // [ 1, 2, 3, 4, 5, 6 ] // ES6const arr1 = [1, 2, 3];const arr2 = [4, 5, 6]; // ...arr2는 [4, 5, 6]을 개별 요소로 분리한다arr1.push(...arr2); // == arr1.push(4, 5, 6); console.log(arr1); // [ 1, 2, 3, 4, 5, 6 ] |      |
| ------------------------- | ------------------------------------------------------------ | ---- |
|                           |                                                              |      |

\- push를 개별 요소로 전달할 수 있으니 훨씬 간결하고 가독성 또한 좋아졌다.

\* **객체에서 사용하기**

| 123456789 | const o1 = { x: 1, y: 2 };const o2 = { ...o1, z: 3 };console.log(o2); // { x: 1, y: 2, z: 3 } const target = { x: 1, y: 2 };const source = { z: 3 };// Object.assign를 사용하여도 동일한 작업을 할 수 있다.// Object.assign은 타깃 객체를 반환한다console.log(Object.assign(target, source)); // { x: 1, y: 2, z: 3 } |      |
| --------- | ------------------------------------------------------------ | ---- |
|           |                                                              |      |

\* 참고 사이트

http://poiemaweb.com/es6-extended-parameter-handling

https://jeong-pro.tistory.com/117