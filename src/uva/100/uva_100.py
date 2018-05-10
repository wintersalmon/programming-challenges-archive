from sys import stdin


def find_max(start, end, cache):
    current_max = 0
    for value in range(start, end + 1):
        temp = rec_count_operation(value, cache)
        if temp > current_max:
            current_max = temp

    return current_max


def count_operation(value):
    if value <= 1:
        return 1

    count = 1
    while value > 1:
        if value % 2 == 0:
            value = value / 2
        else:
            value = value * 3 + 1
        count += 1

    return count


def rec_count_operation(value, cache):
    if value in cache:
        return cache[value]

    if value % 2 == 0:
        cycle = rec_count_operation(value // 2, cache)
    else:
        cycle = rec_count_operation(value * 3 + 1, cache)

    cache[value] = cycle + 1
    return cache[value]


def load():
    while True:
        line = next(stdin)
        num1, num2 = line.split()
        num1, num2 = int(num1), int(num2)
        yield num1, num2


def main():
    cache = {1: 1}
    for num1, num2 in load():
        if num1 > num2:
            ans = find_max(num2, num1, cache)
        else:
            ans = find_max(num1, num2, cache)

        print(num1, num2, ans, sep=' ')


if __name__ == '__main__':
    main()
