[toc]

###### 1. 如何讀寫cxv文件？

```python
"""
    builtins:
    csv
    random
    filter
    range
    open
    append
    next
    float
    list
    dict
    print
    列表解析 字典解析 集合解析 filter函數 lambda匿名函數
"""
import csv

rf = open('books.csv')
reader = csv.reader(rf)
reader.__next__()
next(reader)
for book in reader:
    print(book)

wf = open('demo.csv', 'w')
writer = csv.writer(wf, delimiter=' ')
writer.writerow(['x', 'y', 'z'])
wf.flush()

with open('books.cxv') as rf:
    reader = csv.reader(rf)
    headers = next(reader)
    with open('books_out.csv', 'w') as wf:
        writer = csv.writer(wf)
        writer.writerow(headers)
        for book in reader:
            price = book[-2]
            if price and float(price) >= 80.00:
                writer.writerow(book)
```

###### 2. 如何在列表、字典、集合中根據條件篩選數據？

```python
如何在列表、字典、集合中根據條件篩選數據？
# 列表解析：[x for x in data if x >= 0]
# filter函數：filter(lambda x:x>=0,data)
# 字典解析：{k:v for k,v in data.items() if v > 90}
# 集合解析：{x for x in s if x % 3 == 0}
# 過濾掉列表 [3,9,-1,10-20,-2...]中的負數
data = [-1, 2, 3, -4, 5]
res = []
for x in data:
    if x >= 0:
        res.append(x)
print(res)

from random import randint

l = [randint(-10, 10) for _ in range(10)]
res = [x for x in l if x >= 0]
res_f = list(filter(lambda x: x >= 0, l))
# 篩選出字典{‘lilei’:79,'jim':88,'lucy':92...}中值高於90的項
d = {'student%d' % i: randint(50, 100) for i in range(1, 21)}
score = {k: v for k, v in d.items() if v >= 90}
g = dict(filter(lambda item: item[1] >= 90, d.items()))
# 篩出集合{77,89,32,20...}中能被3整除的元素
s = {randint(0, 20) for _ in range(20)}
result = {x for x in s if x % 3 == 0}
```

###### 3. 如何為元祖中的每個元素命名，提高程序可讀性？

```python
"""
    builtins:
    enum
    isinstance
    collections
    int
    tuple
"""
# 學生信息系統中數據為固定格式：（名字，年齡，性別，郵箱）
# 方案1： 定義一系列數值常量或枚舉類型
# 元祖拆包
NAME, AGE, SEX, EMAIL = range(4)
# 枚舉
from enum import IntEnum


class StudentEnum(IntEnum):
    NAME = 0
    AGE = 1
    SEX = 2
    EMAIL = 3


# 判斷某個類型的實例
isinstance(StudentEnum.NAME, int)
# 方案2： 使用標準庫中collections.namedtuple 替代內置tuple
from collections import namedtuple

Student = namedtuple('Student', ['name', 'age', 'sex', 'email'])
s = Student('jim', 16, 'male', 'jin123@gmail.com')
print(s.email)
isinstance(s, tuple)
```

###### 4. 如何根據字典中值的大小，對字典中的項排序

```python
"""
    builtins:
    zip
    sorted
    enumerate
"""
# 將字典中的各項轉換為元祖，使用內置函數sorted排序
# 方案1：將字典中的項轉化為（值，鍵）元祖。（列表解析或zip）
from random import randint

d = {k: randint(60, 100) for k in 'abcdefgh'}
l = [(v, k) for k, v in d.items()]  # 元祖列表
l2 = list(zip(d.values(), d.keys()))
sorted(l, reverse=True)

# 方案2：傳遞sorted函數的key函數
p = sorted(d.items(), key=lambda item: item[1], reverse=True)
d1 = {}
for i, (k, v) in enumerate(p, 1):
    d1[k] = (i, v)

p1 = {k: (i, v) for i, (k, v) in enumerate(p, 1)}
print(d)
print(dict(p))
```

###### 5. 如何統計序列中元素的頻度？

```python
"""
    builtins:
    random,randint
    range
    dict，fromkeys
    sorted
    heapq
    collections,Counter
    open
    re
"""
# 方案1：將序列轉換為字典{元素：頻度}，根據字典中的值排序。
from random import randint

data = [randint(0, 20) for _ in range(30)]
d = dict.fromkeys(data, 0)
print(d)
for x in data:
    d[x] += 1

result = sorted([(v, k) for k, v in d.items()], reverse=True)[:3]

import heapq

heapq.nlargest(3, ((v, k) for k, v in d.items()))

# 方案2：使用標準庫collections中的Counter對象。
from collections import Counter

c = Counter(data)
c.most_common(3)

# 案例
txt = open('example').read()
import re

word_list = re.split('\W', txt)
c2 = Counter(word_list)
end = c2.most_common(10)
print(end)
```

###### 6. 如何快速找到多個字典的公共鍵（key）?

```python
"""
    random,randint,sample
    all
    map
    lambda
    reduce
    range
    dict
"""
# 方案1：
from random import randint, sample

sample('abcdefgh', randint(3, 6))
d1 = {k: randint(1, 4) for k in sample('abcdefgh', randint(3, 6))}
d2 = {k: randint(1, 4) for k in sample('abcdefgh', randint(3, 6))}
d3 = {k: randint(1, 4) for k in sample('abcdefgh', randint(3, 6))}

for k in d1:
    if k in d2 and k in d3:
        print(k)

r = [k for k in d1 if k in d2 and k in d3]

dl = [d1, d2, d3]
result1 = [k for k in dl[0] if all(map(lambda d: k in d, dl[1:]))]

# 方案2：利用集合（set）的交集操作
# Step1: 使用字典的key()方法，得到一個字典keys的集合。
# Step2: 使用map函數，得到每個字典keys的集合。
# Step3: 使用reduce函數，取所有字典的keys集合的交集
from functools import reduce

reduce(lambda a, b: a * b, range(1, 11))  # 1-10的階乘
result2 = reduce(lambda a, b: a & b, map(dict.keys, dl))
print(result2)
```

###### 7. 如何讓字典保持有序？

```python
"""
    collections,OrderedDict
    random,shuffle
    list
    enumerate
    itertools,islice
"""
# 使用標準庫collections中的OrderedDict
from collections import OrderedDict

od = OrderedDict()

# 將列表的次序打亂
from random import shuffle

player = list('abcdefgh')
shuffle(player)
for i, p in enumerate(player, 1):
    od[p] = i


def query_by_name(d, name):
    return d[name]


from itertools import islice


def query_by_order(d, a, b=None):
    a -= 1
    if b is None:
        b = a + 1
    return list(islice(od, a, b))


print(query_by_order(od, 4, 6))
```

###### 8. 如何實現用戶的歷史記錄功能（最多n條）

```python
"""
    random,randint
    collections,deque
    pickle
    isdigit,dump,load
    append
"""
# 製作一個簡單的猜數字的小遊戲，如何添加歷史記錄功能，顯示用戶最近猜對的數字？
# 使用容量為n的隊列存儲歷史記錄，使用標準庫collections中的deque，它是一個雙端循環隊列。
# 使用pickle模塊將歷史記錄存儲到硬盤，以便下次啟動使用。
from random import randint
from collections import deque
import pickle


def guess(n, k):
    if n == k:
        print('猜對了，這個數字是%d.' % k)
        return True

    if n < k:
        print('猜大了，比%d小.' % k)
    elif n > k:
        print('猜小了， 比%d大.' % k)
    return False


def main():
    n = randint(1, 100)
    i = 1
    hq = deque([], 5)
    while True:
        line = input('[%d] 請輸入一個數字：' % i)
        if line.isdigit():
            k = int(line)
            hq.append(k)
            pickle.dump(hq, open('save.pkl', 'wb'))
            i += 1
            if guess(n, k):
                break
        elif line == 'quit':
            break
        elif line == 'h?':
            q2 = pickle.load(open('save.pkl', 'rb'))
            print(list(q2))


if __name__ == '__main__':
    main()
```