"""
4*5个小格子
4+1*4+2+2*4=18
4种棋子
状态描述：2**20表示棋盘是否占用，用一个int即可

对于一个状态，其实可以用20bit表示，因为总状态数就是38万，每个状态
都可以映射为一个int
"""

r, c = 5, 4


def add(x, y):
    """
    :param x: 棋盘状态，int，0表示空白，1表示已经被占
    :param y: 一个tuple数组，表示准备占据的位置
    :return: 放置之后的棋盘状态
    """
    for i, j in y:
        p = i * c + j  # 准备占据的位置
        if i < 0 or j < 0 or i >= r or j >= c:  # 如果越界了，放不下
            return -1
        if x & (1 << p):  # 如果已经被占据，放不下
            return -1
        x |= (1 << p)
    return x


fac_map = dict()


def fac(n):
    if n == 0: return 1
    if n not in fac_map:
        fac_map[n] = fac(n - 1) * n
    return fac_map[n]


def caocao():
    s = 0
    for i in range(r):
        for j in range(c):
            res = add(0, [(i, j), (i + 1, j + 1), (i, j + 1), (i + 1, j)])
            if res == -1: continue
            for h_cnt in range(6):
                cnt = place_horizon(res, h_cnt, 5 - h_cnt) // (fac(h_cnt) * fac(5 - h_cnt))
                s += cnt
    return s


"""
统计横将数为0，1，2，3，4，5，6时的状态总数
"""
h_map = dict()


def place_horizon(state, h_cnt, v_cnt):
    if h_cnt == 0:
        return place_vertical(state, v_cnt)
    if (state, h_cnt, v_cnt) not in h_map:
        s = 0
        for i in range(r):
            for j in range(c):
                res = add(state, [(i, j), (i, j + 1)])
                if res == -1: continue
                s += place_horizon(res, h_cnt - 1, v_cnt)
        h_map[(state, h_cnt, v_cnt)] = s
    return h_map[(state, h_cnt, v_cnt)]


v_map = dict()


def place_vertical(state, v_cnt):
    # 如果已经无将可放，那么可以开始放置卒子了
    # 剩下六个位置，c（6，2），选出两个空白位置
    if v_cnt == 0: return 15
    if (state, v_cnt) not in v_map:
        s = 0
        for i in range(r):
            for j in range(c):
                res = add(state, [(i, j), (i + 1, j)])
                if res == -1:
                    continue
                s += place_vertical(res, v_cnt - 1)
        v_map[(state, v_cnt)] = s
    return v_map[(state, v_cnt)]

s = caocao()
print(s)
