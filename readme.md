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

	$ python manager.py [-h]
	$ python manager.py new <judge_id> <problem_id>
	$ python manager.py update <judge_id> <problem_id> <case_id> [option_name, ...]
	$ python manager.py run [-vs] <judge_id> <problem_id> [case_id]

	# options
	# -h --help:   display help message
	# -v --detail: display compare diff details
	# -s --save:   save run result to temp file

**new** : 문제 풀이에 필요한 파일들(소스, 입출력 예제)을 자동으로 생성/다운로드 한다

**update** : 주어진 문제 테스트 케이스에 대한 옵션을 토글 한다

**run** : 주어진 문제에 해당하는 테스트 케이스(전부 또는 일부)를 실행하고 실행 결과를 출력한다

### 명령 실행 예

```
#### run all cases ####

$ python manager.py run test abc
RUNNING test abc
- with case a: [ 0.0405] OK
- with case b: [ 0.0555] OK
- with case c: [ 0.0512] OK
- with case d: [ 0.0452] OK
- with case e: [ 0.0529] OK
DONE

$ python manager.py run uva 100
RUNNING uva 100
- with case 809768: [ 0.0643] OK
- with case 809769: [ 0.5644] OK
- with case 821829: [ 0.2180] OK
- with case 827013: [       ] SKIP
- with case 827361: [ 0.0420] OK
DONE

$ python manager.py run uva 10004
RUNNING uva 10004
- with case 810309: [ 0.0528] OK
- with case 833508: [ 0.4887] FAIL
- with case 836416: [ 0.0424] OK
DONE


#### run one case by name ####

$ python manager.py run uva 100 827013
RUNNING uva 100
- with case 827013: [ 0.0602] OK
DONE

$ python manager.py run uva 10004 833508
RUNNING uva 10004
- with case 833508: [ 0.4890] FAIL
DONE


#### running one case will show details about fail ####

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

.

.

.

+NOT BICOLORABLE.

+BICOLORABLE.

DONE

```

### 파일 포맷 설명
| format                                  | format     | description |
| ----------------------------------------| ---------- | ----------- |
| `(judge_id)_(problem_id).py`            | `python`   | 풀이         |
| `(judge_id)_(problem_id).pdf`           | `pdf`      | 문제         |
| `in.(case_id).txt`                      | `txt`      | 입력         |
| `out.(case_id).txt`                     | `txt`      | 예상 출력     |
| `(judge_id).(problem_id).(case_id).txt` | `txt`      | 실행 결과     |

### 프로젝트 디렉토리 설명
```
/res  # contains resources(ex: input, output, etc.)
    /test
        /abc
            .test_abc.json  # contains settings about current cases
            in.a.txt
            in.b.txt
            in.c.txt
            out.a.txt
            out.b.txt
            out.c.txt
        /fail
        /num
    /uva
        /100
            .uva_100.json
            in.809768.txt
            in.809769.txt
            in.821829.txt
            in.827013.txt
            in.827361.txt
            out.809768.txt
            out.809769.txt
            out.821829.txt
            out.827013.txt
            out.827361.txt
        /101
        /116
        /10004
/src  # contains solutions
    /test
        /abc
            test_abc.py
        /fail
        /num
    /uva
        /100
            uva_100.py
        /101
        /116
        /10004
            uva_10004.py
/temp         # contains saved outputs
/tools        # contains script used in manager.py
.secret.json  # contains secret settings
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
