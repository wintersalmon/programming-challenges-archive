# Programming Challenges Archive

* 프로젝트 소개
	* [**개요**](#개요)
	* [**기술 스택**](#기술-스택)
	* [**설명**](#설명)
* 프로젝트 구조
    * [**디렉토리**](#프로젝트-디렉토리)
	* [**파일포맷**](#프로젝트-파일포맷)
* 프로젝트 사용법
	* [**설치방법**](#설치방법)
	* [**명령어**](#명령어)
	* [**HELP**](#command-help) 도움말 출력
	* [**LIST**](#command-list) 문제, 케이스 목록 출력
	* [**CREATE**](#command-create) 새로운 문제 생성
	* [**EXECUTE**](#command-execute) 문제 실행
	* [**SKIPCASE**](#command-skip-case) 특정 케이스 생략 설정
	* [**CREATECASE**](#command-create-case) 새로운 케이스 생성
	* [**REMOVECASE**](#command-remove-case) 케이스 삭제
* [**ToDo**](#ToDo)

## 프로젝트 소개
### 개요
- 알고리즘 문제 풀이 보관소 겸 자동화툴
- Online Judge 를 사용하는 알고리즘 문제 풀이의 단점을 개선 하기 위해, 자동화 스크립트와 Udebug API 를 활용하여 효율적인 개발 환경을 구축하는 프로젝트

### 기술 스택
- python (3.6.3)
- requests (2.18.4)
- [Udebug API](https://www.udebug.com/API/) (0.1.0)

### 설명
- online Judge 를 이용해서 알고리즘 풀이를 할 경우 다음과 같은 단점이 있다
	- Python 심사를 최근에 지원하기 시작해서 오류가 발생할 수 있다
	- [로컬 IDE -> 웹 브라이져 -> 심사 -> 결과 확인] 시간소요 및 오류 발생 가능
	- custom 라이브러리를 import 해서 사용하기 힘들다
	- 테스트 케이스를 직접 작성하고 실행해 보기 힘들다
	- 실패한 심사 결과에 대한 정보가 부족하다
		- 전체/일부 케이스 실패
		- 입/출력 양식 오류
		- 예외 발생
- Udebug 라는 사이트는 다음과 같은 장점이 있다
	- 각 문제에 대한 입출력 예제를 얻을 수 있다
	- 입력 예제를 직접 작성하고 그에 해당하는 올바른 출력값을 획득 할 수 있다
	- 제공하는 API 를 이용해서 위 과정을 자동화 할 수 있다
- PCA 를 통해서
	- 디버깅이 쉽다
	- 문제 풀이 시간이 단축된다
	- 온라인 심사 에서는 사용할 수 없는 방법으로 문제를 풀 수 있다
	- 자주 사용하는 기능을 라이브러리로 만들고 import 해서 사용할 수 있다
	- 비슷한 풀이를 참조하고 같은 실수를 반복하는 것을 방지할 수 있다

## 프로젝트 구조
### 프로젝트 디렉토리
```

/res  # 문제 실행에 필요한 리소스 파일을 저장하는 디렉토리 (입력_파일, 출력_파일, 문제_PDF_파일)
    /uva
    	/100
    	    /827361
                in.txt
                out.txt
    		uva_100.pdf

/src  # 문제 소스 파일, 문제 해설 파일, 문제 케이스 설정 파일을 보관하는 디렉토리
    /uva
        /the_3n_plus_1
            .conf.json
            readme.md
            solution.py

/temp  # 문제 실행 결과를 저장하는 디렉토리

/tools  # 프로젝트 스크립트 툴 보관 디렉토리

.secret.json  # udebug api 사용을 위한 사용자 계정 정보를 저장하는 비밀 파일
pca.py  # 스크립트 실행 관리자
readme.md

```

### 프로젝트 파일포맷
| name                            | path                                            | description |
| ------------------------------- | ----------------------------------------------- | ----------- |
| `in.txt`                        | `RES_DIR/{judge_id}/{problem_id}/{case_id}/`    | 케이스 입력 |
| `out.txt`                       | `RES_DIR/{judge_id}/{problem_id}/{case_id}/`    | 케이스 출력 |
| `(judge_id)_(problem_id).pdf`   | `RES_DIR/{judge_id}/{problem_id}/`              | 문제 PDF |
| `(problem_alias).(case_id).txt` | `TEMP_DIR/`                                     | 케이스 출력 결과 |
| `.conf.json`                    | `SRC_DIR/{judge_alias}/{problem_alias}/`        | 문제 설정 파일 |
| `readme.md`                     | `SRC_DIR/{judge_alias}/{problem_alias}/`        | 문제 풀이 해설 |
| `solution.py`                   | `SRC_DIR/{judge_alias}/{problem_alias}/`        | 풀이 풀이 |


## 프로젝트 사용 방법
### Command Help

```
    $ python pca.py help
```

```
    $ python pca.py <COMMAND> [OPTIONS] [PARAMS]

    $ python pca.py help

    $ python pca.py list <judge_alias>/<problem_alias>

    $ python pca.py create <judge_id>/<problem_id> <judge_alias>/<problem_alias>

    $ python pca.py [-sd] [--save --detailed] execute <judge_alias>/<problem_alias>/<case_id>

    $ python pca.py skipcase <judge_alias>/<problem_alias>/<case_id>

    $ python pca.py createcase <judge_alias>/<problem_alias>/<case_id>

    $ python pca.py removecase <judge_alias>/<problem_alias>/<case_id>
```


### Command List
```
    $ python pca.py list <judge_alias>/<problem_alias>
```

```
    $ python pca.py list uva/the_3n_plus_1

    Problem: uva/the_3n_plus_1 ( uva / 100 )
      809768: []
      809769: []
      821829: []
      827013: ['skip']
      827361: []

```

### Command Create
```
    $ python pca.py create <judge_id>/<problem_id> <judge_alias>/<problem_alias>
```

```
    $ python pca.py create uva/100 uva/the_3n_plus_1

    NEW : PATH_TO_PROJECT/src/uva/the_3n_plus_1/.conf.json
    NEW : PATH_TO_PROJECT/src/uva/the_3n_plus_1/solution.py
    NEW : PATH_TO_PROJECT/src/uva/the_3n_plus_1/readme.md
    NEW : PATH_TO_PROJECT/res/uva/100
    NEW : PATH_TO_PROJECT/res/uva/100/809768/in.txt
    NEW : PATH_TO_PROJECT/res/uva/100/809768/out.txt
    .
    .
    .
    NEW : PATH_TO_PROJECT/res/uva/100/uva_100.pdf
```

```
    $ python pca.py create uva/100 simple/uva_100

    NEW : PATH_TO_PROJECT/src/simple/the_3n_plus_1/.conf.json
    NEW : PATH_TO_PROJECT/src/simple/the_3n_plus_1/solution.py
    NEW : PATH_TO_PROJECT/src/simple/the_3n_plus_1/readme.md
    SKIP: PATH_TO_PROJECT/res/uva/100
    SKIP: PATH_TO_PROJECT/res/uva/100/809768/in.txt
    SKIP: PATH_TO_PROJECT/res/uva/100/809768/out.txt
    .
    .
    .
    SKIP: PATH_TO_PROJECT_ROOT/res/uva/100/uva_100.pdf
```

### Command Execute
```
    $ python pca.py execute [OPTIONS] <judge_alias>/<problem_alias>/<case_id>

    -d, --detail : 테스트 케이스 실패시 실패 정보 출력
    -s, --save : 테스트 케이스 실행 결과를 TEMP 폴더에 저장

```

```
    $ python pca.py execute uva/the_3n_plus_1

    Problem: uva/the_3n_plus_1 ( uva / 100 )
    - with case 809768: [ 0.0558] OK
    - with case 809769: [ 0.5927] OK
    - with case 821829: [ 0.2117] OK
    - with case 827013: [       ] SKIP
    - with case 827361: [ 0.0391] OK

```

```
    $ python pca.py execute uva/the_3n_plus_1/809768

    Problem: uva/the_3n_plus_1 ( uva / 100 )
    - with case 809768: [ 0.0540] OK

```

```
    $ python pca.py execute -ds uva/the_3n_plus_1/809768

    Problem: uva/the_3n_plus_1 ( uva / 100 )
    - with case 809768: [ 0.0540] OK

```

### Command Skip Case
```
    $ python pca.py skipcase <judge_alias>/<problem_alias>/<case_id>
```

```
    $ python pca.py skipcase uva/the_3n_plus_1/827013

    Problem: uva/the_3n_plus_1 ( uva / 100 )
      809768: []
      809769: []
      821829: []
     *827013: ['skip']
      827361: []
```

```
    $ python pca.py skipcase uva/the_3n_plus_1/827013

    Problem: uva/the_3n_plus_1 ( uva / 100 )
      809768: []
      809769: []
      821829: []
     *827013: []
      827361: []
```

### Command Create Case
```
    $ python pca.py createcase <judge_alias>/<problem_alias>/<case_id>

```

### Command Remove Case
```
    $ python pca.py removecase <judge_alias>/<problem_alias>/<case_id>
```


## ToDo
- 명령어 실행 프로세스 개선
- Custom Resource 관리 (명령어: create_case, remove_case)
- Solution 파일 Hash 값 변경 감지, 실행 결과 저장
- 프로젝트 초기화/백업 지원
- 시각적인 실행 결과 지원
