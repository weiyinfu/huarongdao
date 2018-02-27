import collections
import pprint
import queue
import json
import matplotlib.pyplot as plt

"""
本程序用于统计一些华容道小游戏的一些特征
比如：状态总数
可解状态总数
"""
ma = dict()
with open("huarongdao.txt")as f:
    ma = dict()
    for i in f:
        k, v = i.strip().split('=')
        ma[k] = {
            'next': v
        }
print('可解状态总数', len(ma))
graph = json.load(open("huarongdao.json"))
same_count = 0
for i in ma:
    if i == ma[i]['next']:
        same_count += 1
print('已经是终止状态局面', same_count)


def get_step(i):
    if i == ma[i]['next']:
        return 0
    if 'step' in ma[i]:
        return ma[i]['step']
    ma[i]['step'] = get_step(ma[i]['next']) + 1
    return ma[i]['step']


step_node_count = dict()
for i in ma:
    ma[i]['step'] = get_step(i)
print("步数与状态数之间的对应关系")
step_count = collections.Counter(map(lambda x: x['step'], ma.values()))
plt.plot(list(step_count.keys()), list(step_count.values()))
plt.title("the state count - the step count")
plt.xlabel('step count')
plt.ylabel('state count')
plt.show()
max_steps = max(step_count.keys())
print("最难的", step_count[max_steps], "种局面：", max_steps, '步')
for i in ma:
    if ma[i]['step'] == max_steps:
        print(i)
# 按照横将个数分成5种状态，统计各个状态可解的个数
for i in ma:
    ma[i]['type'] = collections.Counter(i)['2'] // 2
type_cnt = dict()
for i in ma:
    type_cnt[ma[i]['type']] = type_cnt.get(ma[i]['type'], 0) + 1
print('按照横将个数分类的可解局面个数', type_cnt)
# 求连通分量
component_cnt = 1
for i in ma:
    if 'component' not in ma[i]:
        q = queue.Queue()
        q.put(i)
        while not q.empty():
            state = q.get()
            if 'component' in ma[state]: continue
            ma[state]['component'] = component_cnt
            for son in graph.get(state, dict()).values():
                if 'component' not in ma[son]:
                    q.put(son)
        component_cnt += 1
# 统计各个类型的分支数
type_component = []
for i in ma:
    type_component.append((ma[i]['component']))
component_counter = list(collections.Counter(type_component).items())
pprint.pprint(collections.Counter(type_component))
