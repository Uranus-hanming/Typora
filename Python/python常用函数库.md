[toc]
##### sys

##### collections

> 这个模块实现专门的容器数据类型提供替代Python的通用内置容器 dict，list， set，和tuple。

##### os

##### functools

> functools模块提供了高阶函数功能：函数可以作为或者返回其他函数。通常， 任何可调用对象可以被视为在本模块的函数。

##### itertools

> Python的内置模块itertools就是用来操作迭代器的一个模块，包含的函数都是能够创建迭代器来用于for循环或者next()。其中函数主要可以分为三类，分别是无限迭代器，有限迭代器，组合迭代器。

##### 无限迭代器

###### count()

> count([start=0, step=1]) 接收两个可选整形参数，第一个指定了迭代开始的值，第二个指定了迭代的步长。此外，start参数默认为0，step参数默认为1，可以根据需要来把这两个指定为其它值，或者使用默认参数。

```python
import itertools
for i in itertools.count(10,2):
    print(i)
    if i>20: 
        break

[Running] python -u "e:\pythonee\code\test.py"
10
12
14
16
18
20
22
```

###### cycle()

> cycle(iterable) 是用一个可迭代对象中的元素来创建一个迭代器，并且复制自己的值，一直无限的重复下去。

```python
import itertools
for i in itertools.cycle("abcd"):
    print(i)     # 具有无限的输出，可以按ctrl+c来停止。

[Running] python -u "e:\pythonee\code\test.py"
a
b
c
d
a
b
c
d
a
b
```

###### repeat()

> repeat(elem [,n])是将一个元素重复n遍或者无穷多遍，并返回一个迭代器。

```python
import itertools
for i in itertools.repeat("abcd",5):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
abcd
abcd
abcd
abcd
abcd
```

##### 有限迭代器

###### chain()

> import itertools for i in itertools.product('ab','cd',repeat = 2): #左右两边进行排列组合，用2次，生成元组内元素数为 序列数*重复次数    print(i)

```python
import itertools
for i in itertools.chain('good','bye'):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
g
o
o
d
b
y
e
```

###### groupby()

> groupby(iterable,key=None) 可以把相邻元素按照 key 函数分组，并返回相应的 key 和 groupby，如果key函数为 None，则只有相同的元素才能放在一组。

```python
import itertools
for key, group in itertools.groupby('AaaBBbcCAAa', lambda c: c.upper()):
    print(list(group))

[Running] python -u "e:\pythonee\code\test.py"
['A', 'a', 'a']
['B', 'B', 'b']
['c', 'C']
['A', 'A', 'a']
```

###### accumulate()

> accumulate(iterable [,func]) 可以计算出一个迭代器，这个迭代器是由特定的二元函数的累计结果生成的，如果不指定的话，默认函数为求和函数。

```python
import itertools
for i in itertools.accumulate([0,1,0,1,1,2,3,5]):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
0
1
1
2
3
5
8
13
```

> 如果我们指定这个累计函数，则还能有不同的用法，例如，指定一个最大值函数，或者自己定义的函数。

```python
import itertools
for i in itertools.accumulate([2,1,4,3,5],max):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
2
2
4
4
5
```

##### 组合迭代器

###### product()

> product(*iterables, repeat=1) 得到的是可迭代对象的**笛卡儿积**，*iterables参数表示需要多个可迭代对象。

```python
import itertools
for i in itertools.product([1,2,3],[4,5,6]):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
(1, 4)
(1, 5)
(1, 6)
(2, 4)
(2, 5)
(2, 6)
(3, 4)
(3, 5)
(3, 6)
```

###### repeat()

> repeat 参数则表示这些可迭代序列重复的次数。

```python
import itertools
for i in itertools.product('ab','cd',repeat = 2):
	#左右两边进行排列组合，用2次，生成元组内元素数为 序列数*重复次数
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
('a', 'c', 'a', 'c')
('a', 'c', 'a', 'd')
('a', 'c', 'b', 'c')
('a', 'c', 'b', 'd')
('a', 'd', 'a', 'c')
('a', 'd', 'a', 'd')
('a', 'd', 'b', 'c')
('a', 'd', 'b', 'd')
('b', 'c', 'a', 'c')
('b', 'c', 'a', 'd')
('b', 'c', 'b', 'c')
('b', 'c', 'b', 'd')
('b', 'd', 'a', 'c')
('b', 'd', 'a', 'd')
('b', 'd', 'b', 'c')
('b', 'd', 'b', 'd')
```

###### permutations()

> permutations(iterable,r=None)返回的是可迭代元素中的一个排列组合，并且是按顺序返回的，且不包含重复的结果。

```python
import itertools
for i in itertools.permutations('abc'):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
('a', 'b', 'c')
('a', 'c', 'b')
('b', 'a', 'c')
('b', 'c', 'a')
('c', 'a', 'b')
('c', 'b', 'a')
```

```python
import itertools
for i in itertools.permutations('abc',2):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
('a', 'b')
('a', 'c')
('b', 'a')
('b', 'c')
('c', 'a')
('c', 'b')
```

###### combinations()

> combinations(iterable,r) 返回的是可迭代对象所有的长度为 r 的子序列，注意这与前一个函数 permutation 不同，permutation 返回的是排列，而 combinations 返回的是组合。

```python
import itertools
for i in itertools.combinations('1234',2):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
('1', '2')
('1', '3')
('1', '4')
('2', '3')
('2', '4')
('3', '4')
```

###### combinations_with_replacement()

> combinations_with_replacement(iterable, r) 返回一个可与自身重复的元素组合，用法类似于 combinations 。

```python
import itertools
for i in itertools.combinations_with_replacement('1234',2):
    print(i)

[Running] python -u "e:\pythonee\code\test.py"
('1', '1')
('1', '2')
('1', '3')
('1', '4')
('2', '2')
('2', '3')
('2', '4')
('3', '3')
('3', '4')
('4', '4')
```