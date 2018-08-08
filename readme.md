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

### 기능

	# general
	$ python manager.py help
	$ python manager.py new <judge> <problem> [problem_alias]
	$ python manager.py show <problem_alias>
	
	# manage
	$ python manager.py update <problem_alias>
	$ python manager.py toggle <problem_alias> <case> <option>
	$ python manager.py add <case_file_path> <problem_alias> [case_alias]
	
	# run
	$ python manager.py run <problem_alias>
	$ python manager.py run <problem_alias> <case>
			# options
			# -d --detail: display compare diff details
			# -s --save:   save run result to temp file

**new** 해당 문제 기본 파일을 생성하고, 필요한 리소스 파일을 온라인에서 검색해서 다운로드 한다. (예: 입력, 출력, 문제 파일), ```problem_alias``` 를 입력하지 않을 경우 임의의 이름이 주어진다

**show** 해당 문제 관련 정보를 출력한다

**update** 해당 문제 케이스 목록을 온라인과 비교하고 추가된 문제를 다운로드 한다

**toggle** 해당 문제 케이스에 대한 옵션을 토글 한다

**add** 해당 문제에 직접 작성한 테스트 케이스를 추가한다 (```Accepted``` 파일을 자동으로 생성한다)

**run** 해당 문제 테스트 케이스를 (전부 또는 일부) 실행한다.

### 명령 실행 예

```
#### 모든 테스트 케이스 실행 ####

$ python manager.py run test_abc
RUNNING test_abc (test/abc)
- with case a: [ 0.0405] OK
- with case b: [       ] SKIP
- with case c: [ 0.3512] FAIL
- with case d: [ 0.0452] OK
- with case e: [ 0.2529] FAIL
DONE


#### 하나의 테스트 케이스만 실행 ####

$ python manager.py run the_3n_plus_1 827013
RUNNING the_3n_plus_1 (uva/100)
- with case 827013: [ 0.0602] OK
DONE

$ python manager.py run uva 10004 833508
RUNNING uva 10004
- with case 833508: [ 0.4890] FAIL
DONE


#### 하나의 테스트 케이스만 실행하고 상세 정보 출력 ####

$ python manager.py run uva 100 809768
RUNNING uva 10004
- with case 809768: [ 0.4890] OK
DONE

$ python manager.py -v run uva 10004 833508
RUNNING uva 10004
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

```

### 파일 포맷 설명

| format                                  | format   | description |
| --------------------------------------- | -------- | ----------- |
| `solution.py`                           | `python` | 풀이         |
| `problem.pdf`                           | `pdf`    | 문제         |
| `in.(case_id).txt`                      | `txt`    | 입력         |
| `out.(case_id).txt`                     | `txt`    | 예상 출력     |
| `(problem_alias).(case_id).txt`         | `txt`    | 실행 결과 (임시) |
| `(judge_id).(problem_id).(case_id).txt` | `txt`    | 실행 결과 (임시) |

### 프로젝트 디렉토리 설명
```
/res  # 문제 풀이 리소스 파일 디렉토리 (입력, 출력, 케이스)
    /test
        /abc
            in.a.txt
            in.b.txt
            in.c.txt
            out.a.txt
            out.b.txt
            out.c.txt
    /uva
    	/100
    		in.*.txt
    		out.*.txt

/src  # 문제 풀이 소스 파일 디렉토리
	/test_abc
		.conf.json
		problem.pdf
		readme.md
		solution.py
	/the_3n_plus_1
		.conf.json
		problem.pdf
		readme.md
		solution.py

/temp         # 실행 결과를 임시 저장하는 디렉토리
/tools        # 자동화 스크립트 디렉토리
.secret.json  # api 비밀키 등을 저장한 설정파일
manager.py
readme.md
```

### ToDo

- 입출력 예제를 Git 에서 제거하고, 소스 디렉토리를 단순화 한다
- 기존에 있는 케이스 목록을 최신 정보로 업데이트 하는 기능
- 문제 설명 pdf 파일을 다운로드 하는 기능
- 개인 테스트를 자동으로 생산 및 저장하는 기능
- Judege/Problem/Case 목록을 출력 하는 기능
- Udebug 에서 지원하지 않는 다양한 사이트 문제 추가 (입출력 방식의 풀이가 아닌 문제들)
	- Function Based Problems [programmers](https://programmers.co.kr])
	- Answer Based Problems [projecteuler](projecteuler.net)
