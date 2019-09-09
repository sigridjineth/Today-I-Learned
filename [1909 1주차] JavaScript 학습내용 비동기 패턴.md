# [1909 1주차] JavaScript 학습내용 비동기 패턴

다음의 내용은 여러 블로그 및 아티클을 바탕으로 학습한 것이다. 자체적으로 정리한 것도 있지만 블로그에서 내용을 가져와 나만의 언어로 다시 풀어낸 것도 있다. 더욱 자세히 알고 싶다면 참고 링크를 확인하여 원문을 찾아보기 바란다. 

해당 파일은 2019년 9월 1주차의 자바스크립트 학습 사항을 정리한 것이다.

## 콜백 함수에 대하여

### 콜백 함수는 왜 사용하는가?

자바스크립트의 변수에는 숫자와 문자, 객체 등을 담을 수 있다. 심지어 함수도 저장이 가능하다. 기본적으로 함수는 객체이므로, 프로토타입 체인이 존재한다. 모든 프로토타입의 객체는 함수를 가리키는 constructor 속성을 지닌다. 함수는 자바스크립트에서 <strong>1급 객체</strong>라서 코드 재사용이나 정보의 구성 및 은닉 등에 사용되는 모듈화의 근간이다.

참고로, 자바스크립트의 1급 객체는 다음의 조건을 충족하여야 한다.

1. 변수나 데이터 구조 안에 담을 수 있다.
2. 파라미터로 전달할 수 있다.
3. 반환값으로 사용할 수 있다.
4. 할당에 사용된 이름과 관계없이, 고유한 구별이 가능하다.
5. 동적인 프로퍼티(Property) 할당이 가능하다.

자바스크립트에서 함수는 1급 객체가 될 수 있는 조건을 모두 충족한다. 함수를 변수에 담을 수 있으며, 다른 함수의 파라미터로 넘길 수 있다. 따라서 우리는 함수를 인자로 사용하는 콜백 패턴(Callback pattern)을 ES6 문법에서 사용할 수 있다. 즉, 자바스크립트에서 함수형 프로그래밍이 가능하다는 것이다. 함수형 프로그래밍은 함수를 인자처럼 사용하는 것을 의미한다.

일반적으로 콜백함수, 또는 higher-order function은 파라미터로 함수를 전달하며, 전달받은 함수는 전달된 함수를 내부에서 실행한다. 먼저, jQuery에서 작동하는 간단한 형태의 콜백함수에 대하여 살펴보자.

```javascript
$("#btn_1").click(function() {
	alert("button1 is clicked")
});
```

위의 코드의 경우, click 함수의 인자로 함수를 전달하고 있다. click 함수가 실행되면 동작한다. 전달받은 함수(click 함수) 내부에서 전달된 함수(alert 함수)를 실행한다는 점에서 전형적인 자바스크립트의 콜백함수이다.

```javascript
var friends = ["Mike", "Stacy", "Andy", "Rick"]; friends.forEach(function (eachName, index){ console.log(index + 1 + ". " + eachName); // 1. Mike, 2. Stacy, 3. Andy, 4. Rick });
```

위의 코드의 경우, forEach라는 함수 안에 새로운 함수를 넣었다. friends 변수 내부의 인자 값을 입력받아 "1. Mike"와 같은 방식으로 출력한다. 지금까지 자바스크립트를 활용하면 콜백함수를 자연스럽게 쓰고 있었음을 깨닫는 순간이다.

### 콜백함수는 어떻게 작동하는가?

앞서 언급했다시피, 자바스크립트의 모든 것은 객체이다. 함수도 무려 일급객체이므로 함수를 마치 변수처럼 return값으로 사용할 수 있다. 특정 함수를 다른 함수의 인자처럼 사용하려면 함수의 이름만 넘겨주면 된다. 주의해야 할 점은 콜백 함수는 전달된 즉시 실행될 필요가 없다는 점이다. 전달받은 함수 내부에서 전달된 함수는 나중에 호출된다.

[Captain Pangyo]([https://joshua1988.github.io/web-development/javascript/javascript-asynchronous-operation/#%EC%BD%9C%EB%B0%B1-%ED%95%A8%EC%88%98%EB%A1%9C-%EB%B9%84%EB%8F%99%EA%B8%B0-%EC%B2%98%EB%A6%AC-%EB%B0%A9%EC%8B%9D%EC%9D%98-%EB%AC%B8%EC%A0%9C%EC%A0%90-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0](https://joshua1988.github.io/web-development/javascript/javascript-asynchronous-operation/#콜백-함수로-비동기-처리-방식의-문제점-해결하기)) 에서 콜백함수의 비동기 작동방식에 대해 기깔찬 비유를 했다. 콜백 함수의 동작 방식은 마치 식당의 자리예약과도 같다. 이해를 돕기 위해 강남역 근처에서 근무하는 직장인을 상정해보자.

점심에는 어디를 가나 사람이 많다. 대기자 명단에 이름을 쓰고 자리가 났다고 연락이 오기 전까지 다른 식당을 돌아다닌다. 만약 식당에 자리가 생기면 문자로 연락이 온다고 가정하자. 그 문자를 받는 시점이 바로 콜백함수가 호출되는 지점이다. 손님 입장에서는 자리가 나기 전까지 식당에서 기다리지 않고 커피를 마신다던지, 잠시 쇼핑을 하러 갈 수도 있다.

자리가 났을 때만 연락이 오므로, 가서 계속 기다릴 필요가 없다. 직접 식당 안으로 들어가 자리가 났는 지 확인할 필요도 없다. 자리가 준비된 지점, 즉 데이터가 준비된 시점에만 우리가 희망하는 동작을 수행할 수 있는 것이다.

#### 코드 살펴보기

```javascript
var loading = function(path, done){
  console.log('전달받은 경로', path)
  done(path + 'sample.txt')
}

loading('/folder/text', function(result){
  console.log('완료!', result)
}
```

해당 파트의 예시는 다음의 [블로그](https://codevkr.tistory.com/52?category=719249)에서 가져왔음을 밝힌다.

우선 loading의 변수에 *function(path, done)*이 저장되어 있다. path는 문자열을 전달받고, done은 함수를 전달받는다. 아래 *loading* 함수를 호출하여 path의 인자와 함수 인자를 전달하고 있다. 

즉, 맨 처음 줄에서 함수를 구현해두고 아래 6행에서 loading 함수를 호출하는 것이다. 구체적으로, path에서 넘어간 데이터를 2행에서 출력한 다음 콜백함수 done을 호출하여 기존의 path에 'sample.txt' 문자열을 붙인다. 마지막 7행에서 전달된 문자열을 출력한다.

콜백함수 패턴을 활용하면 작업을 요청할 수 있을 뿐만 아니라, 작업 완료 시 알림을 받을 수 있는 콜백함수를 같이 받을 수 있다. 따라서 비동기 작업을 순서대로 수행할 수 있다.

### 콜백함수는 클로저다

클로저가 무엇인가? 외부함수의 변수에 접근할 수 있는 내부 함수를 일컫는 말로써, 스코프 체인이라고도 불린다. 클로저는 외부함수가 리턴된 이후에도 외부함수의 변수에 접근할 수 있다. 구체적인 정의는 다음의 [링크](http://chanlee.github.io/2013/12/10/understand-javascript-closure/)를 참조하라.

자바스크립트에서 함수는 일급 객체이다. 즉, 함수를 다른 함수의 인자로 전달할 수 있다는 뜻이다. 이렇게 전달되는 함수의 이름을 functional arguments, 줄여서 funargs라고 부른다. funargs를 전달받는 함수를 higher-order function이라고 명명한다. 그런데 특정 함수를 다른 함수에서 인자로 사용하려고 하면 나타나는 문제가 있다. 이에 대해 알아보자.

#### Upward funargs problem

해당 내역은 Eloquent JavaScript를 영한으로 번역해 놓은 다음의 [블로그](http://graphy21.blogspot.com/2016_06_02_archive.html)에서 학습하였고, 대부분의 예시를 가져왔음을 밝힌다. 

이 문제는 함수가 다른 함수를 리턴하고 이미 선언되어 버린 변수를 사용하면서 나타난다. 일반적으로 프로그램에서 함수가 리턴되면, 내부에 있던 local 변수는 소멸되지만 리턴된 함수의 경우 그 로컬변수가 유지되기 때문이다. 없어진 놈을 찾으려고 난리를 치는 격이다.

변수를 찾기 위해서 이미 변수가 사라진 부모 컨텍스트로 접근하여 문제가 발생한다. 이를 해결하기 위하여 각 함수가 생성되는 순간, (즉 컨텍스트가 생성되는 순간) *Scope* 라는 프로퍼티를 활용하여 부모의 정보를 저장해둔다. 이후 새로운 객체정보(Activation Object)와 부모의 정보를 담은 *Scope* 정보를 조합하여 새로운 스코프체인 정보를 생성한다.

```javascript
function makeAdder(amount) { 
 return function (number) {
   return number + amount;
 };
}
var addTwo = makeAdder(2);
addTwo(3); // 5
```

다음은 클로저를 설명하는 예문이다. 그런데 <code>makeAdder(2)(3)</code>의 값도 5가 나온다. 일반적인 프로그램에서 함수가 리턴하면, 그 내부에 있는 local 변수는 소멸된다. 하지만 리턴된 익명함수의 경우 내부의 로컬변수가 유지된다.

```javascript
function createFunction() {
 var local = 100;
 return function () {return local; };
}
createFunction()(); // 100
```

위의 예시도 명확하다. *CreateFunction* 함수 내부에서 local 변수를 선언했지만, 리턴된 익명함수 내부에서 로컬 변수가 날라가지 않고 여전히 100을 리턴한다. 이러한 방식으로 부모 컨텍스트가 끝난 이후에도 상위 변수를 참조할 수 있는 방법을 마련해둔 것이다. 이러한 형태의 스코프를 static scope 또는 lexical scope라고 부른다.

``` javascript
function foo() {
	var x = 10;
	return function bar() {
		console.log(x);
	};
}

var returnFunc = foo();
var x = 20;
returnFunc(); // 20이 아니다! 10이다: 원래의 부모 변수 x값을 유지하고 있음
```

#### Downward funargs problem

두 번째 문제의 경우, 첫 번째와 달리 부모 컨텍스트는 존재하지만 식별자(identifier)를 찾기 어려운 경우를 의미한다. 어느 스코프에 있는 식별자를 활용해야 할 것인가? 부모의 스코프 체인을 사용해야 하는 지, 실행될 때 호출함수의 컨텍스트의 스코프 체인을 사용해야 할 지 모호한 것이다. 

이러한 경우, 모호함을 해결하기 위하여 함수가 정의될 때 부모의 스코프(static scope)를 사용하게 된다. 다시 말해 자바스크립트는 무조건 함수가 생성되는 시점에 저장된 정보를 사용하는 것으로 정해두었다.

```javascript
var x = 10;
function foo(){
  console.log(x);
}

(function(funArg){
  var x = 20;
  funArg();
})(foo); // 10: 함수가 실행되는 시점이 아니라 생성되는 시점을 기준으로 값을 반환
```

그런데 많은 함수가 같은 부모의 scope를 공유하는 지점이 올 수도 있다. global 컨텍스트에 정의되어 있는 다양한 함수가 있는 경우가 좋은 예시다. 하나의 함수 *scope* 속성에 있는 변수를 변경하면, 같은 부모 *scope* 를 공유하는 함수에도 모두 영향을 미치게 된다.

``` javascript
function baz() {
  var x = 1;
  return {
    foo: function foo() { return ++x; }, // 2
    bar: function bar() { return --x; } // 0
  };}

var closures = baz();

console.log(
  closures.foo(), // 2
  closures.bar()  // 1： 1-1의 0이 아니라 2-1을 반환한 것이다.
```

따라서 loop 내부에 여러 가지 함수를 만들 경우 혼란이 발생할 수 있다. 

예를 들면 다음과 같다.

``` javascript
var data = []; //function-scoped 이므로 for문이 끝나야 한다

for (var k = 0; k < 3; k++) {
  data[k] = function () {
    console.log(k);
  };}

data[0](); // 3이에요, 0이 아니구요.
data[1](); // 3이에요, 1이 아니구요.
data[2](); // 3이에요, 2가 아니구요.
```

```javascript
let data = []; //block-scoped 단위로 hoisting이 일어남

for (let k = 0; k < 3; k++) {
  data[k] = function () {
    console.log(k);
  };}

data[0](); // 0
data[1](); // 1
data[2](); // 2
```

loop 함수 내부에서 counter를 찍을 때, 자칫하면 loop 안에 생성된 함수들이 모두 같은 counter 값을 가질 수도 있다. loop 안에 생성된 함수들이 모두 부모 scope와 같은 클로져를 공유하기 때문이다. 

이러한 문제를 ES6에서 block 기반의 scope를 도입하여 let과 const로 해결할 수 있다. 참고로 ES6 문법에 따라 let에서 변수의 재선언은 불가능하지만, 재할당은 할 수 있다.

#### 예시: filter()를 활용하여 클로저 만들기

아래의 내용은 [다음의 블로그](http://toyo.dothome.co.kr/?p=145) 에서 내용을 학습하고, 가져왔음을 밝힌다.

filter를 사용해서 **3의 배수를 리턴하는 클로저**를 만들어보자.

```javascript
var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]; //1~10의 배열 만들기
arr.filter(function(n){
  return n%3 == 0 // [3, 6, 9]
}) // n에 arr의 값들이 대입되어 3의 배수가 리턴된다.
```

위의 예시를 응용하여 **'2의 배수', '3의 배수' 를 만드는 클로저**를 만들어보자.

```javascript
var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
var generateFilter = function(x){
  return function(n){
    return n % x == 0; // 나누어 떨어지는 녀석을 가져오자
  }
}

var filter2x = generateFilter(2); // 2의 배수만을 가져오자
var filter3x = generateFilter(3); // 3의 배수만을 가져오자

arr.filter(filter2x); [2, 4, 6, 8, 10]
arr.filter(filter3x); [3, 6, 9]
```

#### This Value

This는 원래 스코프체인을 검색하지 않는 녀석으로, 실행할 때의 문맥과 연관있는 객체였다. 하지만 ES6에서 arrow function을 지원하기 위하여 변수 객체의 속성이 되었다. arrow function은 부모 컨텍스트에서 함수가 정의된 시점의 부모 문맥의 this를 자신의 this로 갖게 된다. (이를 lexical this라고 부른다) 

다시 정의하면, global context에서 this는 global variable object를 가리킨다. 결국, this는 변수 객체를 가리키는 꼴이 된다. 하지만 함수 문맥에서는 호출될 때마다 this의 값이 달라질 수 있다.

```javascript
function foo() {
  alert(this);}
// 호출자는 foo()를 호출했고, this라는 녀석을 foo()에게 던져주었다.

foo(); // global 객체다.
foo.prototype.constructor(); // foo.prototype

var bar = {
  baz: foo
};

bar.baz(); // bar에서 baz는 foo다. bar에서 foo는 this이므로, 최종적인 결과값은 bar다.

(bar.baz)(); // global 객체다.

var otherFoo = bar.baz;
otherFoo(); // global 객체다.
```

this에 대한 자세한 사항은 다음의 [링크1](http://dmitrysoshnikov.com/ecmascript/chapter-3-this/), [링크2](http://huns.me/development/258)에 나와있는데, 학습하고 올려보도록 하겠다.

## Promise 패턴

#### 콜백 지옥(Callback Hell)

Promise 패턴은 콜백 함수의 가독성을 해결하기 위하여 사용한다. 하지만 가독성의 문제가 있음을 유념해야 한다. 

아래의 코드는 [Captain Pangyo]([https://joshua1988.github.io/web-development/javascript/javascript-asynchronous-operation/#%EC%BD%9C%EB%B0%B1-%ED%95%A8%EC%88%98%EB%A1%9C-%EB%B9%84%EB%8F%99%EA%B8%B0-%EC%B2%98%EB%A6%AC-%EB%B0%A9%EC%8B%9D%EC%9D%98-%EB%AC%B8%EC%A0%9C%EC%A0%90-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0](https://joshua1988.github.io/web-development/javascript/javascript-asynchronous-operation/#콜백-함수로-비동기-처리-방식의-문제점-해결하기))에서 가져왔다.

```javascript
$.get('url', function (response) {
	parseValue(response, function (id) {
		auth(id, function (result) {
			display(result, function (text) {
				console.log(text);
			});
		});
	});
});
```

비동기 처리 로직을 위하여 콜백 함수를 연속해서 사용하면 '콜백 지옥' 이 발생한다. 이를 콜백 지옥(Callback Hell)이라고 한다. 콜백 안의 콜백을 연속으로 무는 경우 가독성도 떨어지고 로직을 변경하기도 어렵다. Promise 패턴은 콜백 지옥을 해결하기 위하여 사용한다. 

### Promise 패턴의 규칙

자바스크립트의 Promise 패턴은 다음의 규칙을 지킨다.

![프로미스](https://hackernoon.com/hn-images/1*0mBlni5vsYZE2wFzfVv8EA.png)

위의 사진에 나오는 용어를 간단하게 설명해보도록 하자.

* fulfilled(처리 완료) - 작업 성공
* rejected(거부 됨) - 작업 실패
* pending(보류 됨) - 작업 시작 이전
* settled(해결 됨) - 처리 완료 또는 거부 됨

프로세스를 설명해보겠다.

* Promise는 pending 상태이다. 작업을 시작하지 않은 보류 상태(pending)인 것이다. 작업을 진행하다가 fulfill 또는 reject 상황으로 상태가 전환된다. 
* 먼저 성공되었을 경우, fulfill 상태가 되며 이후 then()이 호출된다. settled 상태로 전환된다. 만약 rejected 상태가 되었을 경우, catch()가 호출되어 에러를 핸들링한다.
* 만약 Promise가 여러 개라면, 순서 대로 적용된다. a, b, c가 선언되었다면 a, b, c의 순서대로 실행한다. 이를 보고 순차적으로 체이닝(연결)되었다고 표현한다.

Promise 패턴을 이해하기 위해 다음의 코드를 참조하자. 아래의 코드는 다음의 [블로그](https://codevkr.tistory.com/53?category=719249)에서 가져왔다.

```javascript
var loading = function(path) {
	return new Promise(function(resolve, reject)) {
		console.log('전달받은 경로', path)

		if(path === '/system/'){
			reject('시스템에는 접근이 불가능합니다')
		}
		resolve(path + 'sample.txt')
	}
}

loading('/folder/text/').then(function(result)) { //성공하면 콜백함수가 실행되고
	console.log(result)
}.catch(function(error)){ //실패하면 catch 함수의 콜백함수가 실행된다
	console.log('error', error)
}

hello('Lee').then(function(result)) {
	console.log(result)
}.catch(function(e)){
	console.log(e)
}
```

*then()* 으로 프라미스가 서로 체이닝(Promise Chaining)되어 있어 실행 순서를 파악하기도 쉽고 가독성도 깔끔하다. 만약 *then()*에서 중간에 오류가 발생하면 *then()*은 모두 건너뛰고 바로 *catch()*로 넘어간다. then 하나, catch 하나를 쌍으로 두고 에러를 헨들링할 수도 있다.

프라미스에 대한 자세한 내용은 다음의 [링크 1](https://developers.google.com/web/fundamentals/primers/promises?hl=ko), [링크 2]([https://joshua1988.github.io/web-development/javascript/promise-for-beginners/#promise%EA%B0%80-%EB%AD%94%EA%B0%80%EC%9A%94](https://joshua1988.github.io/web-development/javascript/promise-for-beginners/#promise가-뭔가요))에서 참조할 수 있다.

## 비동기 함수 Await/Async

우선 Node.js에서는 7.6 버전부터 지원한다. 최근에 나온 문법이니 버전에 유의해야 한다.

이해를 돕기 위해 **getJSON** 함수를 예시로 살펴보도록 하자. 해당 파트는 [[6 Reasons Why JavaScript’s Async/Await Blows Promises Away (Tutorial)](https://hackernoon.com/6-reasons-why-javascripts-async-await-blows-promises-away-tutorial-c7ec10518dd9) 아티클을 참조했다.

```javascript
const makeRequest = () =>
  getJSON()
    .then(data => {
      console.log(data)
      return "done"
    })

makeRequest()
```

위의 코드는 Promise를 통해 구현했다. Promise를 반환하고 JSON 오브젝트의 로그를 남기고, *done* 을 반환한다.

```javascript
const makeRequest = async () => {
  console.log(await getJSON())
  return "done"
}

makeRequest()
```

위의 코드는 async/await로 구현한 예시이다. 차이점이 있다면 await은 async가 선언되어야 사용 가능하다는 점이며, 모든 async 함수는 promise를 반환하며 *done* 이라는 문자열을 resolve한다. *await getJSON()*을 통해 *console.log()* 의 호출이 promise가 resolved된 이후에 가져올 것이라고 예측할 수 있다.

async/await는 간결하고 깔끔하다는 호평을 받는다. 에러 핸들링의 과정에서도 간결하다. 다음의 코드를 참조하자.

```javascript
const makeRequest = async () => {
  try {
    // 아래의 파싱은 fail된다.
    const data = JSON.parse(await getJSON())
    console.log(data)
  } catch (err) { // catch 블락이 에러를 파싱한다
    console.log(err)
  }
}
```

다만, Promise가 reject 되었다면 해당 오류를 그 자리에서 throw한다. 따라서 try~catch 구문을 통해 reject 상황을 대비할 수 있다.

```javascript
var hello = function(name){
	return new Promise(function(resolve, reject){
		if(name === ''){
			reject('The name is in void')
		}
		resolve('Mr'+name+'Hello')
	}
}

var asyncHello = async function(name){ //비동기 선언
	try {
		var result = await hello(name)
		console.log(result)
		return '비동기함수 종료'
	}catch(e){
		return e
	}
}

asyncHello('').then(function(result)){
	console.log(result)
}
```

비동기 함수인 Callback, Promise, async/await에 대해 공부하였는데 뒤로 갈 수록 가독성이 개선되고 코드 효율성이 좋아진다는 것을 알 수 있었다. 하지만, 세 가지 방법 모두 비동기 작업을 순차적으로 진행하기 위해 사용한다는 공통점이 있다.

## 참조

1. [[JavaScript\] 비동기 함수(Async/Await)](https://codevkr.tistory.com/54?category=719249)
2. [자바스크립트 async와 await](https://joshua1988.github.io/web-development/javascript/js-async-await/)
3. [[자바스크립트] 자바스크립트의 콜백함수 이해하기! _ v2](https://yubylab.tistory.com/entry/자바스크립트의-콜백함수-이해하기)
4. [[자바스크립트\] 변수로 자바스크립트 이해하기](https://yubylab.tistory.com/entry/자바스크립트-변수로-자바스크립트-이해하기)
5. [[[Javascript ] 프로토타입 이해하기](https://medium.com/@bluesh55/javascript-prototype-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0-f8e67c286b67)
6. [객체 지향 프로그래밍(생성자와 프로토타입)](https://www.zerocho.com/category/JavaScript/post/573c2acf91575c17008ad2fc)
7. [변수로 자바스크립트 이해하기](https://iamawebdeveloper.tistory.com/21)
8. [JavaScript. The Core](http://graphy21.blogspot.com/2016_06_02_archive.html)
9. [[[JS] 자바스크립트의 The Execution Context (실행 컨텍스트) 와 Hoisting (호이스팅)](https://velog.io/@imacoolgirlyo/JS-%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%EC%9D%98-Hoisting-The-Execution-Context-%ED%98%B8%EC%9D%B4%EC%8A%A4%ED%8C%85-%EC%8B%A4%ED%96%89-%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8-6bjsmmlmgy](https://velog.io/@imacoolgirlyo/JS-자바스크립트의-Hoisting-The-Execution-Context-호이스팅-실행-컨텍스트-6bjsmmlmgy))
10. [[JavaScript] 클로저(Closure) 함수와 스코프 체인(Scope Chain)](https://wanzargen.tistory.com/30)
11. [var, let, const 차이점은?](https://gist.github.com/LeoHeo/7c2a2a6dbcf80becaaa1e61e90091e5d)
12. [자바스크립트 클로저 쉽게 이해하기](http://chanlee.github.io/2013/12/10/understand-javascript-closure/)

13. [자바스크립트의 Async/Await 가 Promises를 사라지게 만들 수 있는 6가지 이유](https://hackernoon.com/6-reasons-why-javascripts-async-await-blows-promises-away-tutorial-c7ec10518dd9)
14. [함수](https://gist.github.com/qodot/1845fd02f14807d2eee9c58270ff1b2a)
15. [async/await이 promise보다 좋은 이유](https://ithub.tistory.com/223))

16. [[Async, 비동기와 동기] Promise에서 Await까지](https://velog.io/@rohkorea86/Promiseis-%EB%B9%84%EB%8F%99%EA%B8%B0%EB%8F%99%EA%B8%B0%EC%97%90%EC%84%9C-Promise%EA%B9%8C%EC%A7%80)
