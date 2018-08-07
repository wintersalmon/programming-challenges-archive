## move a onto b
- return all a tops
- return all b tops
- move a to b

## move a over b
- return all a tops
- move a to b

## pile a onto b
- return all b tops
- move all a stacks to b

## pile a over b
- move all a stacks to b


## summary
### prepare
- move => return all a tops
- onto => return all b tops
### do
- move => move a to b
- pile => move all a stack to b


## init
0	1	2	3	4	5	6	7	8	9

## move 9 onto 1
0	1	2	3	4	5	6	7	8	_
	9

## move 8 over 1
0	1	2	3	4	5	6	7	_	_
	9
	8

## move 7 over 1
0	1	2	3	4	5	6	_	_	_
	9
	8
	7

## move 6 over 1
0	1	2	3	4	5	_	_	_	_
	9
	8
	7
	6

## pile 8 over 6 (ignored)
0	1	2	3	4	5	_	_	_	_
	9
	8
	7
	6

## pile 8 over 5
0	1	2	3	4	5	_	_	_	_
	9				8
					7
					6


## move 2 over 1
0	1	_	3	4	5	_	_	_	_
	9				8
	2				7
					6


## move 4 over 9
0	1	_	3	_	5	_	_	_	_
	9				8
	2				7
	4				6

