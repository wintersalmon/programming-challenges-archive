# programming-challenges-archive

## 목적
- 알고리즘 문제 풀이를 위한 프레임 자동화 프레임 워크 제작
- 각 알고리즘의 입력, 출력 예제를 활용하여 실행 시간을 단축
- 공통된 라이브러리를 제작하여 문제 풀이에 활용하고 테스트 자동화


## How To Use

### command
```
# run
manager.sh run <judge_name> <problem_num>  # find and run all cases
manager.sh run <judge_name> <problem_num> [case_num]  # run specific case and show details if case fails

# create
manager.sh create <judge_name> <problem_num>  # find judge_problem online and create and download all cases

```

### examples

```
#### run all cases ####
$./run.sh test echo
RUNNING test_echo
- with case default: [.1770] OK
- with case 01: [.1773] OK
- with case 02: [.1427] OK
- with case 03: [.1593] OK
- with case 11: [.1497] OK
DONE test_echo


#### run one case by name ####
$./run.sh test echo default
RUNNING test_echo
- with case default: [.1752] OK
DONE test_echo

$./run.sh test echo 02
RUNNING test_echo
- with case 02: [.1571] OK
DONE test_echo

$./run.sh test echo_fail
RUNNING test_echo_fail
- with case default: [.1643] FAILED
DONE test_echo_fail


#### running one case will show details about fail ####
$./run.sh test echo_fail default
RUNNING test_echo_fail
- with case default: [.1639] FAILED
--- Answer
+++ Current
@@ -1,5 +1,5 @@
 hello world

 1

 2

-3.14

-400
+3

+4
DONE test_echo_fail

```

### directory example
```
compare.py
/.tools
    compare.py
    load.py
    settings.py
/uva
	/100
	    /case
            uva_100.ans.txt
            uva_100.in.txt
            uva_100.out.txt
        uva_100.pdf
		uva_100.py
	/116  # problem with more then one input case
		/case
            uva_116.ans.txt
            uva_116.in.txt
            uva_116.out.txt
        /case_01
            uva_116.ans.txt
            uva_116.in.txt
            uva_116.out.txt
        uva_116.pdf
		uva_116.py
create.sh
run.sh
```

### file purpose and name format
| format                      | format     | description |
| ----------------------------| ---------- | ----------- |
| `(category)_(name).py`      | `python`   | 풀이         |
| `(category)_(name).pdf`     | `pdf`      | 문제         |
| `(category)_(name).in.txt`  | `txt`      | 입력         |
| `(category)_(name).ans.txt` | `txt`      | 예상 출력     |
| `(category)_(name).out.txt` | `txt`      | 실행 결과     |


### TODO
- error handle
    + run parameter error
    + target directory does not exist
    + target file does not exist

- more tools
    + create project
    + create project cases
    + auto download and create project from web
