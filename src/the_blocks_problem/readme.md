## Instructions

**INSTRUCTIONS**

    MOVE A ONTO B

    MOVE A OVER B

    PILE A ONTO B

    PILE A OVER B

-

**INITIAL VALUES**

	COMMAND A OPTION B

	BLOCK_A is BLOCK that contains A
	BLOCK_B is BLOCK that contains B

-

**CONDITIONS**
if block that has A and B are the same block, the command is considered error and do nothing

	if BLOCK_A == BLOCK_B
		SKIP current instruction

-

**FIRST**
Instructions can be interpreted into smaller instructions

    MOVE A ONTO B
        RETURN all values above A to their INITIAL stack
        RETURN all values above B to their INITIAL stack
        MOVE A to B

    MOVE a OVER b
        RETURN all values above A to their INITIAL stack
        MOVE A to B

    PILE a ONTO b
        RETURN all values above b to their INITIAL stack
        MOVE A and all values above A to B

    PILE a OVER b
        MOVE A and all values above A to B

-

**SECOND**
Instructions can be executed in specific order

	COMMAND A OPTION B

	if COMMAND is MOVE
		RETURN all values above A to their INITIAL stack

	if OPTION is ONTO
		RETURN all values above b to their INITIAL stack

	if COMMAND is MOVE
		MOVE A to B

	elif COMMAND is PILE
		MOVE A and all values above A to B

-

**THIRD**
after return all values to initial stack, move and move all does give the same results


	COMMAND A OPTION B

	if COMMAND is MOVE
		RETURN all values above A to their INITIAL stack

	if OPTION is ONTO
		RETURN all values above b to their INITIAL stack

	MOVE A and all values above A to B

-

**FINAL**

	COMMAND A OPTION B

	if BLOCK_A == BLOCK_B
		SKIP current instruction

	if COMMAND is MOVE
		RETURN all values above A to their INITIAL stack

	if OPTION is ONTO
		RETURN all values above b to their INITIAL stack

	MOVE A and all values above A to B


## example

**init 10**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |

**move 9 onto 1**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |   |
|   | 9 |   |   |   |   |   |   |   |   |

**move 8 over 1**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |   |   |
|   | 9 |   |   |   |   |   |   |   |   |
|   | 8 |   |   |   |   |   |   |   |   |

**move 7 over 1**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 | 6 |   |   |   |
|   | 9 |   |   |   |   |   |   |   |   |
|   | 8 |   |   |   |   |   |   |   |   |
|   | 7 |   |   |   |   |   |   |   |   |

**move 6 over 1**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 |   |   |   |   |
|   | 9 |   |   |   |   |   |   |   |   |
|   | 8 |   |   |   |   |   |   |   |   |
|   | 7 |   |   |   |   |   |   |   |   |
|   | 6 |   |   |   |   |   |   |   |   |

**pile 8 over 6 (error ignored)**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 |   |   |   |   |
|   | 9 |   |   |   |   |   |   |   |   |
|   | 8 |   |   |   |   |   |   |   |   |
|   | 7 |   |   |   |   |   |   |   |   |
|   | 6 |   |   |   |   |   |   |   |   |

**pile 8 over 5**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 |   |   |   |   |
|   | 9 |   |   |   | 6 |   |   |   |   |
|   |   |   |   |   | 7 |   |   |   |   |
|   |   |   |   |   | 6 |   |   |   |   |

**move 2 over 1**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 |   | 3 | 4 | 5 |   |   |   |   |
|   | 9 |   |   |   | 6 |   |   |   |   |
|   | 2 |   |   |   | 7 |   |   |   |   |
|   |   |   |   |   | 6 |   |   |   |   |

**move 4 over 9**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 |   | 3 |   | 5 |   |   |   |   |
|   | 9 |   |   |   | 6 |   |   |   |   |
|   | 2 |   |   |   | 7 |   |   |   |   |
|   | 4 |   |   |   | 6 |   |   |   |   |

**quit**
