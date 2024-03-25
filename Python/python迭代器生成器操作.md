[toc]
##### 1. 如何實現可迭代對象和迭代器對象？

```python
"""
    Iterable
    Iterator
    requests
    len
"""

# 如何實現可迭代對象和迭代器對象？
# Iterable 可迭代對象的基類；Iterator 迭代器對象(一次性，用完就沒了，不可再生，不同的迭代器互不干擾)的基類
from collections import Iterable, Iterator
import requests

# url = 'http://wthrcdn.etouch.cn/weather_mini?city=深圳'
# r = requests.get(url)
# r.json()
# print(r.text)
l = [1, 2, 3, 4, 5, 6]


class WeatherIterator(Iterator):
    def __init__(self, cities):
        self.cities = cities
        self.index = 0

    def __next__(self):
        if self.index == len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        self.index += 1
        return self.get_weather(city)

    def get_weather(self, city):
        url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + city
        r = requests.get(url)
        data = r.json()['data']['forecast'][0]
        return city, data['high'], data['low']


class WeatherIterable(Iterable):
    def __init__(self, cities):
        self.cities = cities

    def __iter__(self):
        return WeatherIterator(self.cities)


def show(w):
    for x in w:
        print(x)


w = WeatherIterable(['深圳', ['廣州'], ['南寧']] * 10)
show(w)
```

##### 2. 如何使用生成器函數實現可迭代對象？

```python
"""
    collections,Iterable
    map
    all
    range
    yield
"""

# 如何使用生成器函數實現可迭代對象？
# 將該類的__iter__方法實現成生成器函數，每次yield返回一個素數。
def f():
    print('in f 1')
    yield 1
    print('in f 2')
    yield 2
    print('in f 3')
    yield 3


from collections import Iterable


class PrimeNumbers(Iterable):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __iter__(self):
        for k in range(self.a, self.b):
            if self.is_prime(k):
                yield k

    def is_prime(self, k):
        return False if k < 2 else all(map(lambda x: k % x, range(2, k)))
        # if k < 2:
        #     return False
        #
        # # [2, k-1]
        # # for x in range(2, k):
        # #     if k % x == 0:
        # #         return False
        # all(map(lambda x: k % x, range(2, k)))
        # return True


def my_test(a, b):
    for k in range(a, b):
        if is_prime(k):
            yield k


def is_prime(k):
    return False if k < 2 else all(map(lambda x: k % x, range(2, k)))


pn = my_test(1, 30)
for n in pn:
    print(n)
```

##### 3. 實現一個連續浮點數發生器FloatRange(和range類似)，根據給定範圍（start,end）和步進值(step)產生一些列連續浮點數

```python
"""
    decimal, Decimal
    reduce
    reversed
    實現一個連續浮點數發生器FloatRange(和range類似)，根據給定範圍（start,end）和步進值(step)產生一些列連續浮點數，如迭代FloatRange(3.0,4.0,0.2)可產生序列：
    正向：3.0 -> 3.2 -> 3.4 -> 3.6 -> 3.8 -> 4.0
    反向：4.0 -> 3.8 -> 3.6 -> 3.4 -> 3.2 -> 3.0
"""
from decimal import Decimal
from functools import reduce

reduce(Decimal.__add__, [Decimal('0.2')] * 30)

l = [1, 2, 3, 4, 5]
reversed(l)
l.__reversed__()


class FloatRange():
    # 構造器
    def __init__(self, a, b, step):
        self.a = Decimal(str(a))
        self.b = Decimal(str(b))
        self.step = Decimal(str(step))

    def __iter__(self):
        t = self.a
        while t <= self.b:
            yield float(t)
            t += self.step

    def __reversed__(self):
        t = self.b
        while t >= self.a:
            yield float(t)
            t -= self.step


fr = FloatRange(3.0, 4.0, 0.2)
for x in fr:
    print(x)
print('-' * 20)
for x in reversed(fr):
    print(x)
```

##### 4. 有某個文本文件，我們想讀取其中某範圍的內容如100~300行之間的內容，python中文件是可迭代對象，我們是否可以使用類似列表切片的方式得到一個100~300行文件內容的生成器？

```python
"""
    itertools,islice
    enumerate
    range
    list
    有某個文本文件，我們想讀取其中某範圍的內容如100~300行之間的內容，python中文件是可迭代對象，我們是否可以使用類似列表切片的方式得到一個100~300行文件內容的生成器？
"""
# 如何對可迭代對象做切片操作？
l = list(range(10))
g = l[3]
# 等價於：
l.__getitem__(3)
# 切片重載下列方法
l.__getitem__(slice(2, 8))
l.__getitem__(slice(2, 8, 2))

# 解決方案：使用itertools.islice，它能返回一個迭代對象切片的生成器。
from itertools import islice


# f = open('')
# for line in islice(f, 100 - 1, 300):
#     print(line)


def my_islice(iterable, start, end, step=1):
    tmp = 0
    for i, x in enumerate(iterable):
        if i >= end:
            break
        if i >= start:
            if tmp == 0:
                tmp = step
                yield x
            tmp -= 1


print(list(my_islice(range(100, 200), 10, 20, 3)))
print(list(islice(range(100, 200), 10, 20, 3)))
```

##### 5. 如何在一個for語句中迭代多個可迭代對象？

```python
"""
    random,randint
    range
    zip
    append
    sum
    map
    list
    chain
    reduce
"""

# 如何在一個for語句中迭代多個可迭代對象？
# 方案一：並行，使用內置函數zip，它能將多個可迭代對象合併，每次迭代返回一個元祖。
from random import randint

chinese = [randint(60, 100) for _ in range(20)]
math = [randint(60, 100) for _ in range(20)]
english = [randint(60, 100) for _ in range(20)]
t = []
for s1, s2, s3 in zip(chinese, math, english):
    t.append([s1, s2, s3])

[sum(s) for s in zip(chinese, math, english)]

list(map(sum, zip(chinese, math, english)))

list(map(lambda s1, s2, s3: s1 + s2 + s3, chinese, math, english))
list(map(lambda *args: args, chinese, math, english))
list(zip(chinese, math, english))

# 串行：使用標準庫中的itertools.chain, 它能將多個可迭代對象連接。
from itertools import chain

c1 = [randint(60, 100) for _ in range(20)]
c2 = [randint(60, 100) for _ in range(20)]
c3 = [randint(60, 100) for _ in range(20)]
c4 = [randint(60, 100) for _ in range(20)]
len([x for x in chain(c1, c2, c3, c4) if x > 90])

s = 'abc\ka;dak,asldf\t5475|dslf:sdl/kjf'
list(map(lambda ss: ss.split('|'), s.split(';')))
from functools import reduce

r = list(reduce(lambda it_s, sep: chain(*map(lambda ss: ss.split(sep), it_s)), '\\/;,|:\t', [s]))
print(r)
```