# programming-challenges-archive

## 목적
- 알고리즘 문제 풀이를 위한 프레임 자동화 프레임 워크 제작
- 각 알고리즘의 입력, 출력 예제를 활용하여 실행 시간을 단축
- 공통된 라이브러리를 제작하여 문제 풀이에 활용하고 테스트 자동화


## How To Use

### command

```
# commands
python manager.py run <judge_id> <problem_id> [case_id] # find and run all cases or specific case"
python manager.py new <judge_id> <problem_id>  # find judge_problem online and create and download all cases"
python manager.py update <judge_id> <problem_id> <case_id> [*options]  # toggle case options"

# options
# -h --help: display help message
# -v --detail: display compare diff details
# -s --save: save results to temp folder
```

### examples

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

### directory example
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

### file purpose and name format
| format                                  | format     | description |
| ----------------------------------------| ---------- | ----------- |
| `(judge_id)_(problem_id).py`            | `python`   | 풀이         |
| `(judge_id)_(problem_id).pdf`           | `pdf`      | 문제         |
| `in.(case_id).txt`                      | `txt`      | 입력         |
| `out.(case_id).txt`                     | `txt`      | 예상 출력     |
| `(judge_id).(problem_id).(case_id).txt` | `txt`      | 실행 결과     |


### TODO
- improvements
    + improved error handle
    + add more use cases to readme

- new functions
    + download problem pdf
    + create and save custom case
    + view judges, problems, cases
    + up-to-date existing project
