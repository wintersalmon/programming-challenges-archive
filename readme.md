## programming-challenges-archive

### 목적
- 알고리즘 문제 풀이를 위한 프레임 자동화 프레임 워크 제작
- 각 알고리즘의 입력, 출력 예제를 활용하여 실행 시간을 단축
- 공통된 라이브러리를 제작하여 문제 풀이에 활용하고 테스트 자동화


### running exmaple
``` bash
$./run.sh test echo
RUNNING test_echo
- with case 'default': done
- with case 1: done
- with case 11: done
- with case 2: done
- with case 3: done
COMPLETE

$./run.sh test echo 11
RUNNING test_echo
- with case 11: done
COMPLETE

$./run.sh test echo default
RUNNING test_echo
- with case default: done
COMPLETE
```

### directory example
```
compare.py
run.sh
/uva  # category
	/100  # problem with only one input case
	    uva_100.pdf
		uva_100.py
		uva_100.ans.txt
		uva_100.in.txt
		uva_100.out.txt
	/116  # problem with more then one input case
	    uva_116.pdf
		uva_116.py
		/case01 
            uva_116.ans.txt
            uva_116.in.txt
            uva_116.out.txt
        /case02 
            uva_116.ans.txt
            uva_116.in.txt
            uva_116.out.txt
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
