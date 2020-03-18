## Day 2 학습내용

### 쉘 스크립트

* 명령어 익히기

* 수많은 문제들을 매번 일일이 커맨드 라인에서 사용하는 데에는 한계가 있다. 만약 각각의 도구 대신 쉘 그 자체를 활용할 수 있다면 더 좋지 않을까? 우리가 설계한 프로그램에 커맨드라인 툴들을 모아놓으면 쉘이 스스로 복잡한 작업들을 순차적으로 수행할 수 있다. 이를 위해서 쉘 스크립트를 작성하는 것이다.

* **쉘 스크립트란?**

  간단히 말하자면 쉘 스크립트는 명령어들이 나열되어 있는 파일이다. 쉘은 이 파일을 읽어서 마치 커맨드 라인에 직접 명령어를 입력하여 실행하는 것처럼 수행한다.

  쉘은 시스템의 강력한 커맨드라인 인터페이스라는 점과 스크립트 언어 인터프리터라는 점에서 조금 독특하다.  커맨드라인에서 할 수 있는 작업 대부분이 스크립트를 통해서도 가능하며 스크립트에서 할 수 있는 작업 또한 커맨드라인에서 가능하다.

*  **쉘 스크립트 작성 방법**

  쉘 스크립트를 만들고 성공적으로 실행하려면 세 가지 작업이 필요하다.

1. 스크립트 작성하기=쉘 스크립트는 일반적인 텍스트 파일이다. 따라서 텍스트 편집기가 필요하다. 좋은 텍스트 편집기는 구문 강조 기능이 있어서 스크립트 요소들을 색상별로 표시해준다. 구문 강조 기능은 흔히 발생하는 오류들을 눈에 띄게 해주고, 스크립트를 작성할 때 vim, gedit, kate 등 다양한 편집기를 사용할수 있다.
2. 스크립트를 실행파일로 설정하기=시스템은 여러 이유들로 예전 텍스트 파일들을 프로그램으로 처리하지 않는다. 따라서 스크립트 파일에 실행 권한을 주어야 한다.

3. 쉘이 접근할 수 있는 장소에 저장하기=쉘은 경로명이 명시되어 있지 않아도 실행 가능한 파일들이 존재하는 특정 디렉토리를 자동으로 검색한다. 우리는 최대한의 편의를 위해 이 디렉토리에 작업한 스크립트를 저장할 것이다.

* 쉘 스크립트 코드 예시 (backup)

```shell
if ! [ -d bak ] then #만약 bak라는 directory가 존재한다면, 다음을 행한다
	mkdir bak #bak라는 디렉토리를 만든다
fi #fin, 즉 "끝났다"
cp *.log bak #copy, all log 파일을 bak라는 디렉토리 안에.
```

* 권한 부여

  * ./backup이라는 프로그램이 생기고, chmod +x를 해주면 executable하게 바뀜으로써 실행 가능한 프로그램이 된다.

* 쉘 스크립트 문법

  * loop 돌기

    ```shell
    for VARIABLE in 1, 2, 3, 4, 5, ..., N
    do
    	command1
    	command2
    	commandN
    done
    ```

    ```shell
    #!/bin/bash
    for i in 1, 2, 3, 4, 5
    do
    	echo "welcome $i times"
    done
    ```

    ```shell
    #!/bin/bash
    for i in {1..5}
    do
    	echo "welcome $i times"
    ```

    ```shell
    #!/bin/bash
    for (( c=1; c<=5; c++ ))
    do  
       echo "Welcome $c times"
    done
    ```

    ```shell
    #!/bin/bash
    
    SET=$(seq 0 9)
    for i in $SET
    do
        echo "Running loop seq "$i
        # some instructions
    done
    ```

```
FILENAME="/some/path/my.file.ext"
// 파일 경로 구하기
echo "FilePath: ${FILENAME%/*}"
// 파일 이름 구하기
echo "FileName: ${FILENAME##*/}"
// 파일 확장자 구하기 
echo "Extension: ${FILENAME##*.}"
```

파일 이름에서 특정 부분만 추출하는 방법

* 쉘 스크립트 배열 선언

  * `files=()`라고 하면 배열이 선언된다.
  * `files+="hi"`라고 하면 배열에 hi가 삽입된다.
  * `$files[@]` 라고 하면 배열 전체가 출력된다.
  * ` $files[i]`라고 하면 특정 인덱스만 원소를 뽑아볼 수 있다.

* 쉘 스크립트 달러 기호($)의 의미

  * $ 달러 기호는 변수임을 나타내기 위한 단어이다.
  * 신기한 것은 ```${variable}``` 이라고 하면, 만약 `variable`이 경로를 나타낼 경우 자동으로 `/`가 붙는다는 것이다. 따라서  `${variable}*.cs`라고 하면 그것으로 족하다.

* SSH로 원격 서버 파일 보내기

  * `scp` : secure copy (remote file copy program)의 줄임말로 `ssh`를 이용해 네트워크로 연결된 호스트간에 파일을 주고 받는 명령어다..
  * `로컬 -> 리모트 (보내기)`, `리모트 -> 로컬 (가져오기)`와 `리모트 -> 리모트 (다른 호스트끼리 전송)` 로 복사가 모두 가능다.
  * `ssh`를 이용하기 때문에 password를 입력하거나 ssh 키파일과 같은 identity file을 이용해 파일 송수신이 가능하다.
  * 로컬 서버 → 원격 서버로 파일 전송
    * scp [옵션] [원본 경로 및 파일] [계정명]@[원격지IP주소]:[전송할 경로]
    * 로컬서버 /home/me/wow.html 파일을 IP 111.222.333.444 서버의 /home/abc/ 디렉토리에 전송
    * scp /home/me/wow.html abc@111.222.333.444:/home/abc/

   서버 구축하기: https://cupjoo.tistory.com/98

### 다른 팀원의 코드

```shell
#!/bin/bash
FILEDATE=$(date +%Y%m%d) #파일 이름의 년월일
filename="backup_$FILEDATE.zip"
find . -name "*.cs" | zip $filename -@ # .cs로 끝나는 파일을 찾아 한 번에 zip
for day in `find . -name "day*"`; do # day로 시작하는 폴더만큼 반복
	ls $day/*.cs > /dev/null 2>&1 # 폴더 안에 .cs 파일이 있는지 확인
	if [ "$?" != "0" ] ; then # 없으면
		echo "$day is empty" # 메시지 출력
	fi
done
scp -P 22 $filename lime@192.168.0.17:~/backup # 우분투로 파일 전송
```

```shell
#!/bin/bash
# NOW=$(date +“%Y%m%d%H%M”)
# filename= “”
# function findZip() {
#   filename = find ./test -name “*.cs” -exec zip “./$NOW.zip” {} \;
# }
# function copy_toserver {
#   scp $filename huey@10.211.55.3:/backup/
# }
# findZip
# copy_toserver
```

![img](https://files.slack.com/files-pri/T74H5245A-FSA2N2MAR/screencapture-github-hu2y-codesquad-blob-master-cs16-day2-readme-md-2020-01-06-10_25_45.png)

```shell
ls $day/*.cs > /dev/null 2>&1
	if [ "$?" != "0" ] ; then #오류값이 false이면 다음을 행한다
```

###파일 복사 시(scp 명령)

1. 1543 포트 확인하기
2. 포트가 닫혀있을 경우 —> 1543포트를 열어줄 것
3. 1543 포트로 파일 전송하기 (edited) 

* 결국 해결하지 못했음 - 도커로 다시 시도해보기

### Honux's Feedback

1. 열심히 삽질하자

2. 리눅스는 오픈소스지만 저작권은 배포자 마음이다.

* 예시: 기술지원을 유료로 지불하는 RedHat 리눅스판

* 모놀리식 커널과 마이크로식 커널 [링크]([https://proneer.tistory.com/entry/%EB%AA%A8%EB%86%80%EB%A6%AC%EC%8B%9D-%EC%BB%A4%EB%84%90Monolithic-Kernel-versus-%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C-%EC%BB%A4%EB%84%90Micro-Kernel](https://proneer.tistory.com/entry/모놀리식-커널Monolithic-Kernel-versus-마이크로-커널Micro-Kernel)) [링크]([https://selfish-developer.com/entry/%EB%AA%A8%EB%86%80%EB%A6%AC%EC%8B%9DMonolithic-kernel%EA%B3%BC-%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9CMicro-%EC%BB%A4%EB%84%90](https://selfish-developer.com/entry/모놀리식Monolithic-kernel과-마이크로Micro-커널))

  * 모놀리식 커널
    * 장점 : 각 Component간의 커뮤니케이션이 효율적이다.
    * 단점 : 디바이스 드라이버를 추가/삭제 하려면 커널을 재빌드 해야 한다. 또한 하나가 죽으면 전체 시스템이 죽는다.

  * 마이크로 커널
    * 장점 : 서버를 추가하는 방식이기 때문에 기능을 추가하기 쉽고, 시스템이 견고하며 리얼타임성이 높다.
    * 단점 : 시스템 기능들이 서버의 형태로 존재하기 때문에 커뮤니케이션 오버헤드가 있다.

3. Docker

* 가상머신이 존재하지 않음
* 컴퓨터에 VM을 설치하고 그 위에 운영체제를 깔았다면, 도커는 컨테이너 안에 이미지를 설치하는 형태

4. 네트워크 설정 및 SSH 연결하기

* NAT라는 가상 랜카드로 자동 설정해주기 때문
* <그림으로 보는 네트워크> 공부 필요

5. 명령어 써보기

   ```shell
   sudo systemctl status sshd #ssh+d는 demon
   ```

6. 여러가지 이슈

* bash 스크립트 사용법을 간단하게라도 익히자.

  * 기존에 많이 만들어져 있는 명령어를 최대한 사용할 수 있다는 장점

  * 1번, 2번 뭔가 나눠져 있다는데 꼭 찾아보기로.

    ```ls cs1/*.txt 2>/dev/null #정상적인 결과만 나오고 에러메시지는 나오지 않는다.```

    ```ls cal/*.txt 2>error.txt cat error.txt #에러메시지가 기록되고 스크립트에는 뜨지 않는다.```

* vim 사용법을 익혀야 리눅스 설정파일을 바꿀 수 있다. 조금이라도 쓸 수는 있어야 한다.

* 패스워드 없이 SSH 로그인하기

  * 공개키 비밀키 방식
  * https://opentutorials.org/module/432/3742
  * AWS 리눅스의 관리 방식

* Docker로 누군가가 작성했던 내용. 이걸 한번 해보자.

  * https://gist.github.com/Hyune-c/0403b92b7738dc202c54ac17ba84b083