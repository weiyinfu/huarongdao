"""
在1*5的棋盘上放置3枚一模一样的棋子有多少种放法
"""
N = 5
M = 3


def one(state, cnt):
    """
    把一样的元素当成不一样的，最后除以全排列数
    :param state:
    :param cnt:
    :return:
    """
    if cnt == 0: return 1
    s = 0
    for i in range(N):
        if state & (1 << i) == 0:
            s += one(state | (1 << i), cnt - 1)
    return s


def fac(n):
    """
    实现阶乘
    :param n:
    :return:
    """
    if not hasattr(fac, 'ma'):
        fac.ma = dict()
    if n not in fac.ma:
        s = 1
        for i in range(1, n + 1):
            s *= i
        fac.ma[n] = s
    return fac.ma[n]


def two(state, cnt):
    """
    返回的就是组合数，每次让哪一个当第一个都是可以的，所以除以cnt
    :param state:
    :param cnt:
    :return:
    """
    if cnt == 0: return 1
    s = 0
    for i in range(N):
        if state & (1 << i) == 0:
            s += two(state | (1 << i), cnt - 1)
    return s // cnt


def three(state, cnt, pos):
    """
    求组合数最好的写法是按照某种顺序，后面的禁止超越前面的
    :param state:
    :param cnt:
    :param pos:
    :return:
    """
    if cnt == 0:
        return 1
    s = 0
    for i in range(pos, N):
        if state & (1 << i) == 0:
            s += three(state | (1 << i), cnt - 1, i)
    return s


print(one(0, 3) // fac(3))
print(two(0, 3))
print(three(0, 3, 0))
