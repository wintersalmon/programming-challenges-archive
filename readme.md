# programming-challenges-archive

- 2018 03월 ~ 현재
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


### 명령

[**HELP**](#command-help) 도움말 출력

[**NEW**](#command-new) 해당 문제 기본 파일을 생성하고, 필요한 리소스 파일을 온라인에서 검색해서 다운로드 한다. (예: 입력, 출력, 문제 파일), ```problem_alias``` 를 입력하지 않을 경우 임의의 이름이 주어진다

[**TOGGLE**](#command-toggle) 해당 문제 케이스에 대한 옵션을 토글 한다

[**SHOW**](#command-show) 해당 문제 관련 정보를 출력한다

[**UPDATE**](#command-updsate) (TBD) 해당 문제 케이스 목록을 온라인과 비교하고 추가된 문제를 다운로드 한다

[**ADD**](#command-add) (TBD) 해당 문제에 직접 작성한 테스트 케이스를 추가한다 (`Accepted` 파일을 자동으로 생성한다)

[**RUN**](#command-run) 해당 문제 테스트 케이스를 (전부 또는 일부) 실행한다.

#### Command Help

    $ python manager.py help

	# general
	$ python manager.py help
	$ python manager.py new <judge> <problem> [problem_alias]
	$ python manager.py show <problem_alias>
	
	# manage
	$ python manager.py update <problem_alias>  # NOT IMPLEMENTED
	$ python manager.py toggle <problem_alias> <case> <option>
	$ python manager.py add <case_file_path> <problem_alias> [case_alias]  # NOT IMPLEMENTED
	
	# run
	$ python manager.py run <problem_alias>
	$ python manager.py run <problem_alias> <case>
			# options
			# -d --detail: display compare diff details
			# -s --save:   save run result to temp file


#### Command New

    $ python manager.py new uva 100 the_3n_plus_1

    NEW the_3n_plus_1 (uva / 100)
      ENTER to continue
      ANY other keys to cancel
    Are you sure?:
    NEW readme.md
    NEW solution.py
    NEW problem.pdf
    NEW 809768 in.txt
    NEW 809768 out.txt
    NEW 809769 in.txt
    NEW 809769 out.txt
    NEW 821829 in.txt
    NEW 821829 out.txt
    NEW 827013 in.txt
    NEW 827013 out.txt
    NEW 827361 in.txt
    NEW 827361 out.txt
    COMPLETE

    $ python manager.py new uva 100

    NEW uva_100 (uva / 100)
      ENTER to continue
      ANY other keys to cancel
    Are you sure?:
    NEW readme.md
    NEW solution.py
    SKIP problem.pdf  # 중복된 파일이 이미 존재할 경우 파일 생성을 SKIP
    SKIP 809768 in.txt
    SKIP 809768 out.txt
    SKIP 809769 in.txt
    SKIP 809769 out.txt
    SKIP 821829 in.txt
    SKIP 821829 out.txt
    SKIP 827013 in.txt
    SKIP 827013 out.txt
    SKIP 827361 in.txt
    SKIP 827361 out.txt
    COMPLETE


#### Command Toggle

    $ python manager.py toggle uva_100 809768 skip
    case option added: 809768 skip


#### Command Show

해당 문제 관련 정보를 출력한다

    $ python manager.py show uva_100

    Problem
      name: uva_100
      code: uva/100
      cases: {
      "809768": {
        "options": [
          "skip"
        ]
      }
      "809769": {
        "options": []
      }
      "821829": {
        "options": []
      }
      "827013": {
        "options": []
      }
      "827361": {
        "options": []
      }
    }

#### Command Update

TBD


#### Command Add

TBD


#### Command Run

    # 모든 테스트 케이스 실행
    $ python manager.py run test_abc

    RUNNING test_abc (test/abc)
    - with case a: [ 0.0405] OK
    - with case b: [       ] SKIP
    - with case c: [ 0.3512] FAIL
    - with case d: [ 0.0452] OK
    - with case e: [ 0.2529] FAIL
    DONE


    # 하나의 테스트 케이스만 실행
    $ python manager.py run the_3n_plus_1 827013

    RUNNING the_3n_plus_1 (uva/100)
    - with case 827013: [ 0.0602] OK
    DONE


    $ python manager.py run bicoloring

    RUNNING bicoloring (uva/10004)
    - with case 833508: [ 0.4890] FAIL
    DONE


    # 하나의 테스트 케이스만 실행하고 상세 정보 출력

    $ python manager.py run bicoloring 809768

    RUNNING bicoloring (uva/10004)
    - with case 809768: [ 0.4890] OK
    DONE


    $ python manager.py -d run bicoloring 833508

    RUNNING bicoloring (uva/10004)
    - with case 833508: [ 0.5277] FAIL
    --- FromFile
    +++ ToFile
    @@ -35,166 +35,166 @@
     NOT BICOLORABLE.

     BICOLORABLE.

     BICOLORABLE.

    -NOT BICOLORABLE.

    -NOT BICOLORABLE.

    . . .

    +NOT BICOLORABLE.

    +BICOLORABLE.

    DONE


### 파일 포맷

| name                             | path                                            | description |
| -------------------------------- | ----------------------------------------------- | ----------- |
| `in.txt`                         | `RES_DIR/{judge_alias}/{problem_id}/{case_id}/` | 입력 |
| `out.txt`                        | `RES_DIR/{judge_alias}/{problem_id}/{case_id}/` | 출력 |
| `(judge_alias)_(problem_id).pdf` | `RES_DIR/{judge_alias}/{problem_id}/`           | 문제 PDF |
| `(problem_alias).(case_id).txt`  | `TEMP_DIR/`                                     | 출력 결과 파일 |
| `.conf.json`                     | `SRC_DIR/{judge_alias}/{problem_id}/`           | 문제 설정 값 저장 |
| `readme.md`                      | `SRC_DIR/{judge_alias}/{problem_id}/`           | 문제 특징, 풀이 설명 |
| `solution.py`                    | `SRC_DIR/{judge_alias}/{problem_id}/`           | 풀이 파일 |


### 프로젝트 디렉토리
```
/res  # 문제 풀이 리소스 파일 디렉토리 (입력, 출력, 문제 PDF)
    /test
        /abc
            /a
                in.txt
                out.txt
            /b
                in.txt
                out.txt
            /c
                in.txt
                out.txt

    /uva
    	/100
    	    /827361  # 케이스 이름 혹은 별칭
                in.txt
                out.txt
    		test_abc.pdf  # 문제 설명 PDF 파일

/src  # 문제 풀이 소스 파일 디렉토리
	/test_abc  # 문제 이름
		.conf.json
		readme.md
		solution.py

	/the_3n_plus_1
		.conf.json
		readme.md
		solution.py

/temp         # 실행 결과를 임시 저장하는 디렉토리
/tools        # 자동화 스크립트 디렉토리

.secret.json  # api 비밀키 등을 저장한 설정파일
manager.py
readme.md
```

### ToDo
- 입출력 예제를 Git 에서 제거
- 기존에 있는 케이스 목록을 최신 정보로 업데이트 하는 기능
- 개인 테스트를 자동으로 생산 및 저장하는 기능
- Judege/Problem/Case 목록을 출력 하는 기능
- Udebug 에서 지원하지 않는 다양한 사이트 문제 추가 (입출력 방식의 풀이가 아닌 문제들)
	- Function Based Problems [programmers](https://programmers.co.kr])
	- Answer Based Problems [projecteuler](projecteuler.net)
