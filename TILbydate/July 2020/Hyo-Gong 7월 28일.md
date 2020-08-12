## Hyo-Gong 7월 28일

### HTTP API

* 그런 REST API로 괜찮은가?
  * [https://github.com/jypthemiracle/Today-I-Learned/blob/1e1edc0baa033b1b8e50f46e5e402d0011025f9a/TILbydate/Mar%202020/2020.03.27%20TIL.md](https://github.com/jypthemiracle/Today-I-Learned/blob/1e1edc0baa033b1b8e50f46e5e402d0011025f9a/TILbydate/Mar 2020/2020.03.27 TIL.md)
* 인수테스트에 대하여

### Node.js Auth

### 준비

* 웹 앱에서 인증을 구현하려면 세션과 쿠키를 주로 사용한다.
  * 서버: 접속한 브라우져 정보를 세션에 저장, 세션 아이디를 브라우져에게 쿠키로 전달한다.
  * 브라우져: 쿠키에 담긴 세션 아이디를 저장, 다음 요청부터는 헤더에 세션 아이디를 담아 서버로 전송한다.
  * 서버: 이 값을 가지고 이전에 접속한 브라우져임을 식별할 수 있다.

#### Passport

* 인증을 위해 만들어진 미들웨어
* http://www.passportjs.org/docs/

#### Strategy 인증전략

* 유저네임/비밀번호 인증은 passport-local

  * 페북/트위터는 passport-facebook, passport-twitter, jwt 방식은 passport-jwt
  * ```userNameField```와 ```passwordField```를 지정하여 이를 비교하는 방식으로 구현할 수 있다.
  * 저장소 참고: https://github.com/jypthemiracle/node-practice/blob/master/crong/apps/router/index.ts
  * 예시 코드

  ```javascript
  module.exports = () => {
    passport.use(
      new LocalStrategy(
        {
          usernameField: "userId", // req.body.userId
          passwordField: "password" // req.body.password
        },
  
        // id,password는 프론트에서 보낸것을받음
        async (userId, password, done) => {
          try {
            const user = await db.User.findOne({ where: { userId } });
            if (!user) {
              return done(null, false, {
                reason: "존재하지 않는 사용자 입니다."
              });
            }
            const result = await bcrypt.compare(password, user.password);
            if (result) {
              // result는 현재 true임
              return done(null, user);
            }
            return done(null, false, { reason: "비밀번호가 틀립니다." }); //else 문.
          } catch (e) {
            console.error(e);
            return done(e);
          }
        }
      )
    );
  };
  // https://velog.io/@wndtlr1024/passport-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%A0%84%EB%9E%B5
  ```

#### Session의 사용

* 세션을 사용하려면 express-session import해야 한다.
* **쿠키(cookie) 객체가 요청한 클라이언트로 전송**될 것이다.

```typescript
// src/index.ts

import session from 'express-session';

app.use(session({
  name: 'mysession', // 쿠키에 저장될 세션키 이름
  secret: 'qwer1234', // 세션 암호화를 위한 시크릿 
  resave: true, // 옵션 참고
  saveUninitialize: true, // 옵션 참고 
}))
```

```typescript
// src/index.ts

app.get('/debug', (req, res) => {
  res.json({
    'req.session': req.session, // 세션 데이터
    'req.user': req.user, // 유저 데이터(뒷 부분에서 설명)
    'req._passport': req._passport, // 패스포트 데이터(뒷 부분에서 설명)
  })
});
```

```json
// localhost:3000/debug
{
  "req.session": {
    "cookie": {
      "originalMaxAge": null,
      "expires": null,
      "httpOnly": true,
      "path": "/"
    }
  }
}
```

### SerializeUser, DeserializeUser

#### serializeUser

* 사용자 정보 객체를 세션에 아이디로 저장한다.
* 매개변수로 user를 받아 done 함수에 두번째 인자로 user.id를 넘긴다.

```javascript
    passport.serializeUser((user, done) => {
        return done(null, user.id);
    });
```

#### deserializeUser

* passport의 세션 미들웨어가, 세션에 저장한 아이디를 통해서 사용자 정보 객체를 불러온다.

* serializeUser에 저장했던 id를 받아서 데이터베이스에서 사용자 정보를 조회한다.

```javascript
    passport.deserializeUser( async (id, done) => {
        try {
            const user = await db.user.findOne({
                where : { id },
            });
            return done(null, user);
        } catch (e) {
            console.error(e);
            return done(e);
        }
    });
```

#### 참고하면 좋은 링크

* https://jeonghwan-kim.github.io/dev/2020/06/20/passport.html

* https://github.com/jeonghwan-kim/post_passport
* [https://velog.io/@mollang/20.01.13-%EB%83%89%EC%9E%A5%EA%B3%A0-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%93%A4%EC%96%B4%EA%B0%80%EA%B8%B0-%EC%A0%84-46k5c5ik2s](https://velog.io/@mollang/20.01.13-냉장고-프로젝트-들어가기-전-46k5c5ik2s)