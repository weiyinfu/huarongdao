import tkinter
import tkinter.font as tkfont
import random
import numpy as np

"""
界面小游戏，玩华容道
按键为：上下左右，ctrl+上下左右
向每一个方向移动都可能有两种：
如果是第一种直接按就行，
如果是第二种就需要按下ctrl再按方向键

按空格，请求AI帮助
按ctrl+N，重新加载局面
"""


def loaddata():
    """
    加载表格数据，表示面对每个局面应该怎么走
    :return:
    """
    ma = dict()
    data = np.fromfile("huarongdao.bin", np.int32)
    for i in data:
        ma[i >> 3] = i & 7
    return ma


GRIDWIDTH = 100
GAP = 2  # 木块之间的间隔
R = 5  # 行数
C = 4  # 列数
direction = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # 方向
root = tkinter.Tk()
data = loaddata()
all_states = list(data.keys())
ca = tkinter.Canvas(root, width=GRIDWIDTH * 4, height=GRIDWIDTH * 5)
ca.pack()
recs = [{'color': 'white', 'shape': (1, 1), 'body': [(0, 0)]},
        {'color': 'red', 'shape': (2, 2), 'body': [(0, 0), (0, 1), (1, 0), (1, 1)]},
        {'color': 'green', 'shape': (1, 2), 'body': [(0, 0), (0, 1)]},
        {'color': 'black', 'shape': (2, 1), 'body': [(0, 0,), (1, 0)]},
        {'color': 'grey', 'shape': (1, 1), 'body': [(0, 0)]},
        ]
# 精灵数组，存储画布上的对象
spirite = [[0] * C for _ in range(R)]
# 棋盘，存储数据
board = [[0] * C for _ in range(R)]
info = None  # 画布上的文字信息


def load_state(s):
    """
    加载游戏状态
    :param s: 长度为20的字符串
    :return:
    """
    global spirite, board, info
    ca.delete(info)
    # 先把旧的精灵清空
    for i in spirite:
        for j in i:
            ca.delete(j)
    spirite = [[0] * C for _ in range(R)]
    board = decode(s)
    # s为长度为20的字符串，此函数加载状态
    vis = [[0] * C for _ in range(R)]
    for i in range(R):
        for j in range(C):
            val = board[i][j]
            rec = recs[val]
            if val and not vis[i][j]:
                sp = ca.create_rectangle(
                    j * GRIDWIDTH + GAP,
                    i * GRIDWIDTH + GAP,
                    (j + rec['shape'][1]) * GRIDWIDTH - GAP,
                    (i + rec['shape'][0]) * GRIDWIDTH - GAP,
                    fill=rec['color']
                )
                for dx, dy in recs[val]['body']:
                    vis[i + dx][j + dy] = True
                    spirite[i + dx][j + dy] = sp


def legal(x, y):
    return R > x >= 0 and C > y >= 0


def canmove(board, x, y, d):
    """
    位于（x，y）处的棋子是否可以向方向d移动
    :param x:
    :param y:
    :param d:
    :return:
    """
    body = set()
    val = board[x][y]
    for dx, dy in recs[val]['body']:
        body.add((x + dx, y + dy))
    for dx, dy in recs[val]['body']:
        i, j = x + dx + d[0], y + dy + d[1]
        if not legal(i, j): return False
        if board[i][j] != 0 and (i, j) not in body: return False
    return True


def move(x, y, d):
    """
    把位于x,y处的棋子向方向d移动
    :param x:
    :param y:
    :param d: 形如（dx，dy）
    :return:
    """
    if not legal(x, y): return
    # 需要更改精灵，数据，显示三部分
    val = board[x][y]
    sp = spirite[x][y]
    ca.move(sp, GRIDWIDTH * d[1], GRIDWIDTH * d[0])
    for dx, dy in recs[val]['body']:
        i, j = x + dx, y + dy
        board[i][j] = 0
        spirite[i][j] = 0

    for dx, dy in recs[val]['body']:
        i, j = x + dx + d[0], y + dy + d[1]
        board[i][j] = val
        spirite[i][j] = sp


def encode(board):
    """
    将棋盘局面转化为int
    :param board:
    :return:
    """
    s = ''
    vis = [[False] * C for _ in range(R)]
    for i in range(R):
        for j in range(C):
            if not vis[i][j]:
                s += str(board[i][j])
                for dx, dy in recs[board[i][j]]['body']:
                    vis[i + dx][j + dy] = True
    return int(s[::-1], 5)


def mirror(board):
    """
    棋盘左右反转，不改变原数据
    :param board:
    :return: 反转后的棋盘
    """
    ans = [[0] * C for _ in range(R)]
    for i in range(R):
        for j in range(C):
            ans[i][j] = board[i][C - 1 - j]
    return ans


def decode(s):
    # 将int解析为棋盘局面
    a = [[0] * C for _ in range(R)]
    vis = [[False] * C for _ in range(R)]
    for i in range(R):
        for j in range(C):
            if not vis[i][j]:
                val = s % 5
                s //= 5
                for dx, dy in recs[val]['body']:
                    vis[i + dx][j + dy] = True
                    a[i + dx][j + dy] = val
    return a


def over():
    return board[3][1] == 1 and board[3][2] == 1 and board[4][1] == 1 and board[4][2] == 1


def get_todo(board):
    vis = [[0] * C for _ in range(R)]
    todo = [[] for _ in range(4)]
    for i in range(R):
        for j in range(C):
            if board[i][j] and not vis[i][j]:
                for d in range(len(direction)):
                    if canmove(board, i, j, direction[d]):
                        todo[d].append((i, j))
                    for dx, dy in recs[board[i][j]]['body']:
                        vis[i + dx][j + dy] = True
    return todo


def operate(op):
    global info
    todo = get_todo(board)
    d = op % 4  # 方向
    which = min(op // 4, len(todo[d]) - 1)  # 操作第几个
    if which < 0: return
    move(*todo[d][which], direction[d])
    if over():
        font = tkfont.Font(root, name='微软雅黑', size=30)
        info = ca.create_text(C / 2 * GRIDWIDTH, R / 2 * GRIDWIDTH, text="您赢了", font=font)


def help_move(board):
    # 查表走一步
    state = encode(board)
    if state in data:
        op = data[state]
        return op
    state = encode(mirror(board))
    if state in data:
        op = data[state]
        d = (2, 1, 0, 3)[op % 4]  # 移动的方向，需要镜像回来
        todos = get_todo(mirror(board))
        x, y = todos[op % 4][op // 4]  # 移动的位置
        y = C - 1 - y  # 现在y是右上角，需要转换为左上角
        y -= recs[board[x][y]]['shape'][1] - 1
        todos = get_todo(board)
        return 4 * todos[d].index((x, y)) + d


def keydown(evt):
    print(evt.state, evt.keycode)
    control_is_down = (evt.state & 4)
    if evt.keycode == 32:
        m = help_move(board)
        print(m)
        if m is None:
            print("电脑不知道咋走")
            return
        operate(m)
    if control_is_down and evt.keycode == ord('N'):
        load_state(random.choice(all_states))
        return
    if over():
        print("游戏已经结束了，按ctrl+n开启新游戏")
        return
    direction_keys = (37, 38, 39, 40)
    if evt.keycode in direction_keys:
        op = direction_keys.index(evt.keycode)
        if control_is_down: op += 4
        operate(op)


root.title("press space to get help")
load_state(random.choice(all_states))
root.bind("<Key>", keydown)
ca.focus()
root.mainloop()
