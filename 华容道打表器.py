import queue
import copy
import time
import json

R, C = 5, 4
a = [[0] * C for _ in range(R)]
all_states = []  # 存储全部的状态
father_state = dict()  # 存储父状态，用于记录走法
shape = [[(0, 0), (0, 1), (1, 0), (1, 1)],
         [(0, 0), (0, 1)],
         [(0, 0), (1, 0)],
         [(0, 0)]]
graph = dict()


def canput(pos):
    """
    判断pos中的点处是否可以放置棋子
    :param pos: 形如[(x1,y1),(x2,y2),(x3,y3)]
    :return:
    """
    for x, y in pos:
        if not legal(x, y): return False
        if a[x][y] != 0: return False
    return True


def put(val, pos):
    """
    将棋盘a上的pos所包含的点的数值置为val，表示放置了棋子或者清空了棋子
    :param val:
    :param pos:
    :return:
    """
    for x, y in pos:
        a[x][y] = val


def caocao():
    for i in range(R):
        for j in range(C):
            shape = [(i, j), (i + 1, j + 1), (i, j + 1), (i + 1, j)]
            if canput(shape):
                put(1, shape)
                # 枚举横将的个数
                for h_cnt in range(6):
                    place_horizon(h_cnt, 5 - h_cnt, 0)
                put(0, shape)


def place_horizon(h_cnt, v_cnt, pos_begin):
    if h_cnt == 0:
        place_vertical(v_cnt, 0)
        return
    for i in range(pos_begin, R * C):
        x, y = i // C, i % C
        shape = [(x, y), (x, y + 1)]
        if canput(shape):
            put(2, shape)
            place_horizon(h_cnt - 1, v_cnt, i + 1)
            put(0, shape)


def place_vertical(v_cnt, pos_begin):
    if v_cnt == 0:
        place_zu(4, 0)
        return
    for i in range(pos_begin, R * C):
        x, y = i // C, i % C
        shape = [(x, y), (x + 1, y)]
        if canput(shape):
            put(3, shape)
            place_vertical(v_cnt - 1, i + 1)
            put(0, shape)


def place_zu(zu_cnt, pos_begin):
    if zu_cnt == 0:
        all_states.append(copy.deepcopy(a))
        return
    for i in range(pos_begin, R * C):
        x, y = i // C, i % C
        shape = [(x, y)]
        if canput(shape):
            put(4, shape)
            place_zu(zu_cnt - 1, i + 1)
            put(0, shape)


def legal(x, y):
    return R > x >= 0 and C > y >= 0


def canmove(board, x, y, d):
    body = set()
    for dx, dy in shape[board[x][y] - 1]:
        i, j = x + dx, y + dy
        body.add((i, j))
    for i, j in body:
        m, n = i + d[0], j + d[1]
        if not legal(m, n): return False
        if board[m][n] != 0 and (m, n) not in body: return False
    return True


def move(board, x, y, d):
    val = board[x][y]
    for dx, dy in shape[val - 1]:
        i, j = x + dx, y + dy
        board[i][j] = 0
    for dx, dy in shape[val - 1]:
        i, j = x + dx + d[0], y + dy + d[1]
        board[i][j] = val


def build_graph():
    q = queue.Queue(len(all_states) // 2)
    for i in all_states:
        # 把已经是终止状态了结点放入队列
        if i[3][1] == 1 and i[3][2] == 1 and i[4][1] == 1 and i[4][2] == 1:
            q.put(i)
            i = tos(i)
            father_state[i] = i
    print('已经是结束状态的局面总数', q.qsize())
    while q.qsize():
        now = q.get()
        now_key = tos(now)
        vis = [[0] * C for _ in range(R)]
        todo = [0] * 4
        for i in range(R):
            for j in range(C):
                if now[i][j] and not vis[i][j]:
                    for dx, dy in shape[now[i][j] - 1]:
                        vis[i + dx][j + dy] = True
                    for di, d in enumerate([(0, -1), (-1, 0), (0, 1), (1, 0)]):
                        if canmove(now, i, j, d):
                            op = todo[di] * 4 + di  # 操作的id
                            todo[di] += 1
                            copy_board = copy.deepcopy(now)
                            move(copy_board, i, j, d)
                            key = tos(copy_board)
                            put_graph(now_key, key, op)
                            if key not in father_state:
                                father_state[key] = now_key
                                q.put(copy_board)


def put_graph(src, des, op):
    if src not in graph:
        graph[src] = dict()
    graph[src][op] = des


def tos(a):
    s = ''
    for i in a:
        for j in i:
            s += str(j)
    return s


def save():
    with open("huarongdao.txt", mode='w') as f:
        for i in father_state:
            f.write(i + "=" + father_state[i] + "\n")
    with open("huarongdao.json", mode='w') as f:
        json.dump(graph, f)


beg = time.time()
caocao()
print('局面总数', len(all_states))
build_graph()
print('可解的局面总数', len(father_state))
save()
end = time.time()
print('总计用时', end - beg, '秒')
