"""
在本程序的go函数上加上一个state参数，表示局面，只需要表示每个格点
是否占用即可
"""
li = [
    {
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
        'count': 4
    }
]
r, c = 5, 4
a = [[0] * c for _ in range(r)]
total_count = 0


def canput(shape, x, y):
    for dx, dy in shape:
        i, j = x + dx, y + dy
        if i < 0 or j < 0 or i >= r or j >= c: return False
        if a[i][j] != 0: return False
    return True


def put(val, shape, x, y):
    for dx, dy in shape:
        i, j = x + dx, y + dy
        a[i][j] = val


def go(index, count, pos):
    global total_count
    if count == 0:
        if index == len(li) - 1:
            total_count += 1
        else:
            go(index + 1, li[index + 1]['count'], 0)
        return
    for i in range(pos, r * c):
        x, y = i // c, i % c
        if canput(li[index]['shape'], x, y):
            put(index + 1, li[index]['shape'], x, y)
            go(index, count - 1, i)
            put(0, li[index]['shape'], x, y)


def huarongdao():
    global total_count
    s = 0
    for i in range(6):
        li[1]['count'] = i
        li[2]['count'] = 5 - i
        go(0, li[0]['count'], 0)
        now_s = total_count
        total_count = 0
        s += now_s
        print('横将数', i, now_s)
    print("总数", s)


huarongdao()
