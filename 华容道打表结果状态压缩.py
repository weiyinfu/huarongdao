"""
本程序用于对打表结果进行压缩
"""
import numpy as np
import time
import json

R = 5
C = 4
body = [[(0, 0)],  # 空格
        [(0, 0,), (0, 1), (1, 0), (1, 1)],  # 曹操
        [(0, 0), (0, 1)],  # 横将
        [(0, 0), (1, 0)],  # 竖将
        [(0, 0)]]  # 卒子


def load():
    """
    加载数据
    :return:
    """
    ma = dict()
    with open("huarongdao.txt")  as f:
        for i in f.readlines():
            k, v = i.strip().split('=')
            ma[k] = v
    graph = json.load(open("huarongdao.json"))
    return ma, graph


def mirror(s):
    # 左右反转
    a = [0] * (R * C)
    for i in range(R):
        for j in range(C):
            a[i * C + j] = s[i * C + C - 1 - j]
    return ''.join(a)


def transform_state(s):
    # 将状态转变为int
    board = [[0] * C for _ in range(R)]
    ans = []
    for i in range(R):
        for j in range(C):
            if not board[i][j]:
                ans.append(s[i * C + j])
                for dx, dy in body[int(s[i * C + j])]:
                    board[i + dx][j + dy] = True
    return int(''.join(ans)[::-1], base=5)


def filt(data):
    ans = dict()
    vis = set()
    for i in data:
        if i == data[i]: continue  # 过滤掉已经成功的状态
        if i not in vis:
            me = transform_state(i)
            mirror_state = mirror(i)
            another = transform_state(mirror_state)
            vis.add(i)
            vis.add(mirror_state)
            if me > another:
                ans[mirror_state] = data[mirror_state]
            else:
                ans[i] = data[i]
    return ans


def run():
    data, graph = load()
    print('过滤之前状态数', len(data))
    data = list(filt(data).items())
    print('过滤之后状态数', len(data))
    a = np.empty(len(data), np.int32)
    for i in range(len(a)):
        for j in graph[data[i][0]]:
            if graph[data[i][0]][j] == data[i][1]:
                a[i] = (transform_state(data[i][0]) << 3) | int(j)
    a.tofile("huarongdao.bin")


print('状态表示最大需要的bit数为', len(bin(int('444433333100', 5))) - 2)
beg = time.time()
run()
end = time.time()
print('用时', end - beg, '秒')
