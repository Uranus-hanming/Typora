[toc]
###### zip函數

> 用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
>
> 如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用`*`号操作符，可以将元组解压为列表。

```python
zip(iter1 [,iter2 [...]]) --> zip object

print(zip(range(3), 'ABC'))  # ➊ zip 函数返回一个生成器，按需生成元组。
# <zip object at 0x10063ae48>
print(list(zip(range(3), 'ABC')))  # ➋ 为了输出，构建一个列表；通常，我们会迭代生成器。
# [(0, 'A'), (1, 'B'), (2, 'C')]
print(list(zip(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3])))  # ➌ zip 有个奇怪的特性：当一个可迭代对象耗尽后，它不发出警告就停止。
# [(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2)]

from itertools import zip_longest

# ➍ itertools.zip_longest 函数的行为有所不同：使用可选的fillvalue（默认值为 None）填充缺失的值，因此可以继续产出，直到最长的可迭代对象耗尽。
print(list(zip_longest(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3], fillvalue=-1)))
# [(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2), (-1, -1, 3.3)]
```

###### map()函數

- 语法：map(function, iterable, ...)  其中 function 表示函数 ，iterable 表示一个或多个序列
- 描述： 会根据提供的函数对指定序列做映射。第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。

###### filter()函數

- 语法：filter(function, iterable)   其中 function 表示判断函数，iterable 表示可迭代对象。
- 描述：函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。

###### reduce()函數

- 语法：reduce(function, iterable[, initializer]) 其中function 表示函数，有两个参数，iterable 表示可迭代对象，initializer表示可选，初始参数。
- 描述：对参数序列中元素进行累积。函数将一个数据集合（链表，元组等）中的所有数据进行下列操作：用传给 reduce 中的函数 function（有两个参数）先对集合中的第 1、2 个元素进行操作，得到的结果再与第三个数据用 function 函数运算，最后得到一个结果。

```python
from functools import reduce
def add(x, y):
    return x + y
print(reduce(add, [1, 2, 3, 4, 5]))  # 1+2+3+4+5=15
```

###### sorted函數

- sorted(iterable, cmp=None, key=None, reverse=False) --> new sorted list
- 接受4個參數
  - 1.可迭代类型，例如字典、列表、
  - 2.比较函数
  - 3.可迭代类型中某个属性，对给定元素的每一项进行排序
  - 4.降序或升序

- 比較函數經常會用到lambda.

###### 計數器函數Counter

- 计算出一个字符在列表或者字典里面出现的次数

```python
from collections import Counter
c = Counter(list_t)
c.most_common(3)
sorted(c)
sum(c.values())
```

###### sample函數

- sample 函数的作用是第一个参数（列表）获取一个长度为第二个参数的子列表。

###### shuffle函數

- 将序列中的所有元素随机排序
- from random import shuffle

###### OrderedDict函數

- 按照有序插入顺序存储 的有序字典

- 排序

  ```python
  dd = {'banana': 3, 'apple':4, 'pear': 1, 'orange': 2}
  # 按key排序
  kd = collections.OrderedDict(sorted(dd.items(), key=lambda t: t[0]))
  # 按照value排序
  vd = collections.OrderedDict(sorted(dd.items(),key=lambda t:t[1]))
  # 输出
  OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])
  OrderedDict([('pear', 1), ('orange', 2), ('banana', 3), ('apple', 4)])
  ```

###### deque雙端隊

```python
from collections import deque
queue = collections.deque()
```

- 單個數據入隊
  - append(item)，添加一个数据到队列的尾部。与列表的append()方法功能相似。
  - appendleft(item)，添加一个数据到队列的头部。与append()的添加方向相反。
-  可迭代对象入队: extend(iterable)，将一个可迭代对象中的数据按顺序添加到队列的尾部。
-  指定位置插入数据: insert(index, item)，在队列中的指定位置插入一个数据，index为指定的位置索引。
- 队列两端的出队方法。
  - pop()，将队列尾部的数据弹出，并作为返回值。
  - popleft()，将队列头部的数据弹出，并作为返回值。

- deque的copy方法: copy()，拷贝队列。拷贝之后，对原队列进行操作，不会影响到拷贝出来的队列。
- deque返回指定值的数量和索引
  - count(item)，返回队列中指定值的数量，如果值不存在则返回0。
  - index(item)，返回队列中指定值的索引，如果值不存在则报错，如果有多个相同的数据则返回从左到右第一个值的索引。
- deque的翻转和轮转
  - reverse()，将队列翻转。与列表的reverse()方法功能一样。
  - rotate(num)，对队列中的数据进行轮转。
- deque的删除
  - remove(item)，从队列中删除指定的数据，如果指定的数据不存在则报错，如果有多个相同的数据则只会删除从左到右的第一个数据。
  - clear()，将队列清空。
- deque指定队列的长度

###### pickle模塊

- pickle.dump(obj, file[, protocol])

  > 序列化对象，并将结果数据流写入到文件对象中。

- pickle.load(file)

  > 反序列化对象。将文件中的数据解析为一个Python对象。

- pickle.clear_memo()

  > 清空pickler的“备忘”。

###### enumerate函數

> 基本应用就是用来遍历一个集合对象，它在遍历的同时还可以得到当前元素的索引位置。

```python
names = ["Alice","Bob","Carl"]
for index,value in enumerate(names, 1):
    print(f'{index}: {value}')
```

###### dict.fromkeys()

> 用于创建并返回一个新的字典。两个参数：第一个是字典的键，第二个（可选）是传入键的值，默认为None。

```python
from random import randint

data = [randint(0, 20) for _ in range(30)]
d = dict.fromkeys(data, 0)
print(d)
```