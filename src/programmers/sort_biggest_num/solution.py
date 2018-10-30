import functools


@functools.total_ordering
class Number(object):
    __slots__ = ('_num',)

    def __init__(self, num: int):
        self._num = str(num)

    def __gt__(self, other):
        if isinstance(other, Number):
            src = ''.join((self._num, other._num))
            dst = ''.join((other._num, self._num))
            return int(src) > int(dst)
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, Number):
            return self._num == other._num
        raise NotImplementedError

    def __repr__(self):
        return self._num


def solution(numbers):
    nums = reversed(sorted(Number(n) for n in numbers))
    return str(int(''.join(map(str, nums))))


if __name__ == '__main__':
    print(solution([12, 121]), '12121')
    print(solution([21, 212]), '21221')
    print(solution([6, 10, 2]), '6102')
    print(solution([0, 1, 0]), '100')
    print(solution([0, 0, 0]), '0')
    print(solution([3, 30, 34, 5, 9]), '9533430')
