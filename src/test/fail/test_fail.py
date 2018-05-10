from sys import stdin

for idx, line in enumerate(stdin):
    if idx == 0:
        print('hello world')
    else:
        print(idx)
