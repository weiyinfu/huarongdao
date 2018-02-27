"""
本程序展示一种通用的计算棋子在棋盘上放置方法种数的算法

将棋盘最右最下多放置一层，就能够实现位运算快速检测，如果不在棋盘周围多放置一层
会出现错误（无法准确判断越界错误）。
"""
import time

li = [{
        'shape': [(0, 0), (0, 1), (1, 0), (1, 1)],
        'count': 1,
        'desc': '曹操',
    }, {
        'shape': [(0, 0), (0, 1)],
        'count': 0,
        'desc': '横将数',
    }, {
        'shape': [(0, 0), (1, 0)],
        'count': 5,
        'desc': '竖将数'
    }, {
        'shape': [(0, 0)],
        'count': 4,
        'desc': '卒子'
    }
]
r, c = 5, 4


def init():
    """
    将每个棋子的形状转化为int，从而便于快速利用位运算来判断是否某个位置被占据
    :return:
    """
    for i in li:
        sha = 0
        for dx, dy in i['shape']:
            p = dx * (c + 1) + dy
            sha |= (1 << p)
        i['shapeMask'] = sha


def get_init_state():
    """
    在棋盘的右面，下面添加一行
    :return:
    """
    state = 0
    for i in range(r + 1):
        state |= (1 << (i * (c + 1) + c))
    for i in range(c + 1):
        state |= (1 << (r * (c + 1) + i))
    return state


init()

fac_map = dict()


def fac(n):
    """
    计算阶乘
    :param n:
    :return:
    """
    if n not in fac_map:
        s = 1
        for i in range(1, n + 1):
            s *= i
        fac_map[n] = s
    return fac_map[n]


def put(state, shape, pos):
    """
    在pos处放置shape形状的棋子
    :param state: 棋盘状态，二进制形式，1表示占用，0表示不占用
    :param shape: 形如[(x1,y1),(x2,y2),(x3,y3)],表示棋子的形状
    :param pos: 放置棋子的左上角的位置
    :return: 如果能放下，返回棋盘状态；如果放不下，返回-1
    """
    if state & (shape << pos): return -1
    return state | (shape << pos)


go_map = dict()
use = 0


def solve(state, index, count):
    """
    第二种方法计算棋子放置种数，这种方法的优势在于能够更加充分地利用
    动态规划，参数越少越能够充分利用节点
    :param state:
    :param index:
    :param count:
    :return:
    """
    global use
    key = (state, index, count)
    use += 1
    if key not in go_map:
        use -= 1
        s = 0
        if count == 0:
            if index == len(li) - 1:
                s = 1
            else:
                s = solve(state, index + 1, li[index + 1]['count'])
        else:
            for i in range((r + 1) * (c + 1)):
                res = put(state, li[index]['shapeMask'], i)
                if res == -1: continue
                s += solve(res, index, count - 1)
        go_map[key] = s
    return go_map[key]


def go(state, index, count, pos):
    global use
    key = (state, index, count, pos)
    use += 1
    if key not in go_map:
        use -= 1
        s = 0
        if count == 0:
            if index == len(li) - 1:
                s = 1
            else:
                s = go(state, index + 1, li[index + 1]['count'], 0)
        else:
            for i in range(pos, (r + 1) * (c + 1)):
                res = put(state, li[index]['shapeMask'], i)
                if res == -1: continue
                s += go(res, index, count - 1, i)
        go_map[key] = s
    return go_map[key]


def huarongdao():
    global use
    beg = time.time()
    s = 0
    for i in range(6):
        li[1]['count'] = i
        li[2]['count'] = 5 - i
        go_map.clear()
        now_s = go(get_init_state(), 0, li[0]['count'], 0)
        print('横将数', i, now_s, '状态节点数', len(go_map), '无需计算就返回的次数', use)
        use = 0
        s += now_s
    print("总数", s)
    end = time.time()
    print('用时', end - beg)


def huarongdao2():
    global use
    beg = time.time()
    s = 0
    for i in range(6):
        li[1]['count'] = i
        li[2]['count'] = 5 - i
        go_map.clear()
        now_s = solve(get_init_state(), 0, li[0]['count'])
        for j in li:
            now_s //= fac(j['count'])
        print('横将数', i, now_s, '状态节点数', len(go_map), '无需计算就返回的次数', use)
        use = 0
        s += now_s
    print("总数", s)
    end = time.time()
    print('用时', end - beg)


print(bin(get_init_state()))
huarongdao()
huarongdao2()
