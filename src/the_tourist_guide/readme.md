# The Tourist Guide

- Uva: 10099
- Programming Challenges Problem 67 (Chapter 09)

## Solution

다익스트라 알고리즘의 변형 문제
1. 최단거리가 아닌 최대 운송 값을 구한다
3. 경로의 weight 누적값이 아닌 경로상 최소 weight 를 이용한다

1. 그래프를 생성한다 (weight 값에서 1을 미리 빼준다, 가이드가 버스에 함께 타야하기 때문에)
2. 시작점으로 부터 인접 노드를 순회한다 (heapq, reversed-child-iter 를 이용해서 가장 큰 weight 를 가지는 노드를 우선으로 방문한다)
    - 다음 노드의 weight 값이 math.inf 인 경우 값을 갱신한다
    - 다음 노드의 weight 값이 이전 노드의 weight 값보다 작을경우 값을 갱신한다
