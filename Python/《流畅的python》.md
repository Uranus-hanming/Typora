[toc]
### 1 一摞Python风格的纸牌

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(deck, key=spades_high):
	print(card)
```

##### 獲取一個紙牌對象

```python
beer_card = Card('7', 'diamonds')
```

##### __getitem__ 方法提供

- 抽取特定的一張紙牌

  ```python
  deck = FrenchDeck()
  deck[0]
  ```

- 随机抽取一张纸牌

  ```python
  from random import choice
  choice(deck)
  ```

- 自动支持切片（slicing）操作

  ```python
  deck[12::13]
  ```

- 將一摞牌变成可迭代

  ```python
  for card in deck:
  	print(card)
  for card in reversed(deck):
      print(card)
  ```

##### 排序

```python
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
def spades_high(card):
	rank_value = FrenchDeck.ranks.index(card.rank)
	return rank_value * len(suit_values) + suit_values[card.suit]
	
# 有了 spades_high 函数，就能对这摞牌进行升序排序了：
for card in sorted(deck, key=spades_high):
	print(card)
```

##### python风格

- python最好的品质之一是一致性；
- python的设计思想完全体现在python的数据模型上，而数据模型所描述的API，为使用最地道的语言特性来构建你自己的对象提供了工具；
- python解释器碰到特殊的句法时，会使用特殊方法去激活一些基本的对象操作；
- 中缀运算符的基本原则就是不改变操作对象，而是产出一个新的值。
- 在切片和区间操作里不包含区间范围的最后一个元素。
  - 当只有最有一个位置信息时，我们也可以快速看出切片和区间里有几个元素：range(3)和my_list[:3]都返回3个元素；
  - 当起止位置信息都可见时，我们可以快速计算出切片和区间的长度，用后一个数减去第一个下标（stop-start）即可；
  - 可以利用任意一个下标来把序列分割成不重叠的两部分，只要携程my_list[:x]和mylist[x:]就可以了。
- python的一个惯例：如果一个函数或者方法对对象进行的是就地改动，那它就应该返回None，好让调用者知道传入的参数发生了变动，而且并未产生新的的对象。

##### 如何使用特殊方法

- 特殊方法的存在是为了被 Python 解释器调用的，你自己并不需要调用它们：
  - 也就是说没有 my_object.\__len__() 这种写法，而应该使用 len(my_object)。
  - 在执行 len(my_object) 的时候，如果my_object 是一个自定义类的对象，那么 Python 会自己去调用其中由你实现的 \__len__ 方法。
- 然而如果是 Python 内置的类型，比如列表（list）、字符串（str）、字节序列（bytearray）等，那么 CPython 会抄个近路，\__len__ 实际上会直接返回 PyVarObject 里的 ob_size 属性。PyVarObject 是表示内存中长度可变的内置对象的 C 语言结构体。直接读取这个值比调用一个方法要快很多。
- 很多时候，特殊方法的调用是隐式的，比如 for i in x: 这个语句，背后其实用的是 iter(x)，而这个函数的背后则是 x.\__iter__() 方法。当然前提是这个方法在 x 中被实现了。
- \_\_init\_\_ 方法，目的是在你自己的子类的\__init__ 方法中调用超类的构造器。
- 通过内置的函数（例如 len、iter、str，等等）来使用特殊方法是最好的选择。这些内置函数不仅会调用特殊方法，通常还提供额外的好处，而且对于内置的类来说，它们的速度更快。

### 2 數據結構

##### 内置序列类型

- 容器序列: list、tuple 和 collections.deque

  > 这些序列能存放不同类型的数据。
  >
  > 容器序列存放的是它们所包含的任意类型的对象的引用

- 扁平序列: str、bytes、bytearray、memoryview 和 array.array

  > 这类序列只能容纳一种类型。
  >
  > 扁平序列里存放的是值而不是引用；
  >
  > 扁平序列是一段连续的内存空间，它里面只能存放诸如字符、字节和数值这种基础类型。

- 可变序列: list、bytearray、array.array、collections.deque 和 memoryview
- 不可变序列: tuple、str 和 bytes

##### 列表表達式

- 列表推导不会有变量泄露的问题
- 列表推导可以帮助我们把一个序列或是其他可迭代类型中的元素过滤或是加工，然后再新建一个列表。

```python
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
```

##### map/filter 组合

```python
beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
```

##### 生成器表达式

```python
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
    print(tshirt)
```

##### 元祖

- 元祖其实是对数据的记录：元祖中的每个元素都存放了记录中一个字段的数据，外加这个字段的位置。

###### 元祖拆包

```python
city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)
```

- 不使用中间变量交换两个变量的值

  ```python
  b, a = a, b
  ```

- 用 * 运算符把一个可迭代对象拆开作为函数的参数

  ```python
  divmod(*t)
  ```

- 让一个函数可以用元组的形式返回多个值，然后调用函数的代码就能轻松地接受这些返回值

  ```python
  import os 

  path, filename = os.path.split('/home/luciano/.ssh/idrsa.pub')
  print(path)  # /home/luciano/.ssh
  print(filename)  # idrsa.pub
  ```

- 函数用 *args 来获取不确定数量的参数

  ```py
  >>> a, b, *rest = range(5)
  >>> a, b, rest
  (0, 1, [2, 3, 4])

  >>> *rest， a, b = range(5)
  >>> a, b, rest
  ([0, 1, 2], 3, 4)
  ```

- 嵌套元祖拆包

###### 具名元组

- 创建一个具名元祖需要两个参数，一个是类名，另一个是类的各个字段的名字。后者可以是由数个字符串组成的可迭代对象，或者是由空格分隔开的字段名组成的字符串。

- 存放在对应字段里的数据要以一串参数的形式传入到构造函数中，注意元祖的构造函数只接受单一的可迭代对象。

- 可以通过字段名或位置来获取一个字段的信息。

- _fields类属性：是一个包含这个类所有字段名称的元祖

- _make()：通过接受一个可迭代对象来生成这个类的一个实例，它的作用跟City(*delhi_data)是一样的

  ```python
  from collections import namedtuple
  
  City = namedtuple('City', 'name country population coordinates')
  LatLong = namedtuple('LatLong', 'lat long')
  delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
  delhi = City._make(delhi_data)
  result = City(*delhi_data)
  print(delhi)
  print(result)
  >>> City(name='Delhi NCR', country='IN', population=21.935, coordinates=LatLong(lat=28.613889, long=77.208889))
  ```

```python
from collections import namedtuple
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))

>>> tokyo
City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722,
139.691667))
>>> tokyo.population
36.933
```

##### 切片

- 用s[a : b : c]的形式对s在a和b之间以c为间隔取值。c的值为负值意味着反向取值。

- 操作方式

  1. 对对象进行切片

  2. 多维切片

  3. 省略

  4. 给切片赋值

     > 把切片放在赋值语句的左边，或把它作为del操作的对象，我们就可以对序列进行嫁接、切除或就地修改操作。
     >
     > 如果赋值的对象是一个切片，那么赋值语句的右侧必须是个可迭代对象。即便只有单独一个值，也要把它转换成可迭代的序列。

##### 对序列使用+和*

- 不修改原有的操作对象，而是构建一个全新的序列。

```py
board = [['_'] * 3 for i in range(3)]
>>> board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
```

##### 序列的增量赋值

- +=对可变序列来说，变量名会不会被关联到新的对象，完全取决于类型有没有实现\__iadd__方法，使用id()查看。

##### 增量操作

- 对不可变序列进行重复拼接操作的话，效率会很低，因为每次都有一个新对象，而解释器需要把原来对象中的元素先复制到新的对象里，然后再追加新的元素。
- str 是一个例外，因为对字符串做 += 实在是太普遍了，所以 CPython 对它做了优化。为 str初始化内存的时候，程序会为它留出额外的可扩展空间，因此进行增量操作的时候，并不会涉及复制原有字符串到新位置这类操作。

##### list.sort方法

- list.sort方法会就地排序列表，因此不会把原列表复制一份。

- 内置函数sorted会新建一个列表作为返回值。可以接受任何形式的可迭代对象作为参数，甚至包括不可变序列或生成器。

- reverse

  > 如果被设定为True，被排序的序列里的元素会以降序输出。

- key

  > 一个只有一个参数的函数，这个函数会被用在序列里的每一个元素上，所产生的结果将是排序算法依赖的对比关键字。

##### sorted 函数的key

> 一个只有一个参数的函数，这个函数会被用在序列里的每一个元素上，所产生的结果将是排序算法依赖的对比关键字。比如说，在对一些字符串排序时，可以用 key=str.lower 来实现忽略大小写的排序，或者是用 key=len 进行基于字符串长度的排序。这个参数的默认值是恒等函数（identity function），也就是默认用元素自己的值来排序。

- sorted会新建一个列表作为返回值。

- sorted方法可以接受任何形式的可迭代对象作为参数，甚至包括不可变序列或生成器。而不管 sorted 接受的是怎样的参数，它最后都会返回一个列表。

- Python 的排序算法——Timsort——是稳定的，意思是就算两个元素比不出大小，在每次排序的结果里它们的相对位置是固定的。

  ```python
  >>> fruits = ['grape', 'raspberry', 'apple', 'banana']
  >>> sorted(fruits)
  ['apple', 'banana', 'grape', 'raspberry'] ➊
  >>> fruits
  ['grape', 'raspberry', 'apple', 'banana'] ➋
  >>> sorted(fruits, reverse=True)
  ['raspberry', 'grape', 'banana', 'apple'] ➌
  >>> sorted(fruits, key=len)
  ['grape', 'apple', 'banana', 'raspberry'] ➍
  >>> sorted(fruits, key=len, reverse=True)
  ['raspberry', 'banana', 'grape', 'apple'] ➎
  >>> fruits
  ['grape', 'raspberry', 'apple', 'banana'] ➏
  >>> fruits.sort() ➐
  >>> fruits
  ['apple', 'banana', 'grape', 'raspberry'] ➑
  """
  ❶ 新建了一个按照字母排序的字符串列表。
  ❷ 原列表并没有变化。
  ❸ 按照字母降序排序。
  ❹ 新建一个按照长度排序的字符串列表。因为这个排序算法是稳定的，grape 和 apple 的长度都是 5，它们的相对位置跟在原来的列表里是一样的。
  ❺ 按照长度降序排序的结果。结果并不是上面那个结果的完全翻转，因为用到的排序算法是稳定的，也就是说在长度一样时，grape 和 apple的相对位置不会改变。
  ❻ 直到这一步，原列表 fruits 都没有任何变化。
  ❼ 对原列表就地排序，返回值 None 会被控制台忽略。
  ❽ 此时 fruits 本身被排序。
  """
  ```


##### 用bisect来管理已排序的序列

> bisect(haystack, needle)在haystack里搜索needle的位置，该位置满足的条件是，把needle插入这个位置之后，haystack还能保持升序。也就是这个函数返回的位置前面的值，都小于或等于needle的值。

###### 用bisect.insort插入新元素

> insort(seq, item)把变量item插入到序列seq中，并能保持seq的升序顺序。

##### 数组

- 数组在背后存的并不是float对象，而是数字的机器翻译，也就是字节表述。因此要存放1000万个浮点数，数组（array）的效率更高。
- 一个只包含数字的列表，用array.array比list更高效。
- 频繁对序列作出先进先出的操作，deque（双端队列）的速度更快。
- 包含操作（比如检查一个元素是否出现在一个集合中）的频率很高，用set（集合）会更合适。

```python
>>> from array import array ➊ 引入 array 类型。
>>> from random import random
>>> floats = array('d', (random() for i in range(10**7))) ➋ 利用一个可迭代对象来建立一个双精度浮点数组（类型码是 'd'），这里我们用的可迭代对象是一个生成器表达式。
>>> floats[-1] ➌ 查看数组的最后一个元素。
0.07802343889111107
>>> fp = open('floats.bin', 'wb')
>>> floats.tofile(fp) ➍ 把数组存入一个二进制文件里。
>>> fp.close()
>>> floats2 = array('d') ➎ 新建一个双精度浮点空数组。
>>> fp = open('floats.bin', 'rb')
>>> floats2.fromfile(fp, 10**7) ➏ 把 1000 万个浮点数从二进制文件里读取出来。
>>> fp.close()
>>> floats2[-1] ➐ 查看新数组的最后一个元素。
0.07802343889111107
>>> floats2 == floats ➑ 检查两个数组的内容是不是完全一样。
True
```

##### memoryview

> 是一个内置类，它能让用户在不复制内容的情况下操作同一个数组的不同切片，即在数据结构之间共享内存

##### 队列

###### collections.deque类（双向队列）

> 是一个线程安全、可以快速从两端添加或者删除元素的数据类型。

```python
from collections import deque
dq = deque(range(10), maxlen=10) ➊ maxlen 是一个可选参数，代表这个队列可以容纳的元素的数量，而且一旦设定，这个属性就不能修改了。
dq.rotate(3) ➋ 队列的旋转操作接受一个参数 n，当 n > 0 时，队列的最右边的 n个元素会被移动到队列的左边。当 n < 0 时，最左边的 n 个元素会被移动到右边。
dq.appendleft(-1) ➌ 当试图对一个已满（len(d) == d.maxlen）的队列做尾部添加操作的时候，它头部的元素会被删除掉。
dq.extend([11, 22, 33]) ➍ 在尾部添加 3 个元素的操作会挤掉 -1、1 和 2。
dq.extendleft([10, 20, 30, 40]) ➎ extendleft(iter) 方法会把迭代器里的元素逐个添加到双向队列的左边，因此迭代器里的元素会逆序出现在队列里。
```

##### dict字典 - 映射类型

- isinstance可以用来判定某个数据是否为广义上的映射类型

  ```py
  my_dict = {}
  isinstance(my_dict, abc.Mapping)
  ```

- 标准库里的所有映射类型都是利用dict来实现的

###### 可散列的数据类型

> 如果一个对象是可散列的，那么在这个对象的声明周期中，它的散列值是不变的，而且这个对象需要实现\_\_hash__()方法。另外可散列对象还要有\_\_qe\_\_()方法，这样才能跟其他键做比较。如果两个可散列对象是相等的，那么它们的散列值一定是一样的。

###### 用setdefault处理找不到的键

```python
"""创建从一个单词到其出现情况的映射"""
"""获取单词的出现情况列表，如果单词不存在，把单词和一个空列表
放进映射，然后返回这个空列表，这样就能在不进行第二次查找的情况
下更新列表了。"""

import sys
import re

WORD_RE = re.compile(r'\w+')
index = {}
with open(sys.argv[0], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index.setdefault(word, []).append(location)

print(index)
# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, len(index[word]))
```

###### defaultdict：处理找不到的键的一个选择

> 在用户创建defaultdict对象的时候，需要给构造方法提供一个可调用对象，这个可调用对象会在\_\_getitem\_\_碰到找不到的键的时候被调用，让\_\_getitem\_\_返回某种默认值。

###### 特殊方法\_\_missing\_\_

>  所有的映射类型在处理找不到的键的时候，都会牵扯到\_\_missing\_\_方法。
>
>  如果有一个类继承了 dict，然后这个继承类提供了 \__missing__ 方法，那么在 \__getitem__ 碰到找不到的键的时候，Python 就会自动调用它，而不是抛出一个 KeyError 异常。

```python
class StrKeyDict0(dict):  # ➊ StrKeyDict0 继承了 dict。
    """在查询的时候把非字符串的键转换为字符串"""

    def __missing__(self, key):
        if isinstance(key, str):  # ➋ 如果找不到的键本身就是字符串，那就抛出 KeyError 异常。
            raise KeyError(key)
        return self[str(key)]  # ➌ 如果找不到的键不是字符串，那么把它转换成字符串再进行查找。

    def get(self, key, default=None):
        try:
            return self[key]  # ➍get 方法把查找工作用 self[key] 的形式委托给 __getitem__，这样在宣布查找失败之前，还能通过 __missing__ 再给某个键一个机会.
        except KeyError:
            return default  # ➎ 如果抛出 KeyError，那么说明 __missing__ 也失败了，于是返回default.

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()  # ➏ 先按照传入键的原本的值来查找（我们的映射类型中可能含有非字符串的键），如果没找到，再用 str() 方法把键转换成字符串再查一次


d = StrKeyDict0([('2', 'two'), ('4', 'four')])
print(d['2'])

```

###### 字典的变种

-  collections.OrderedDict

  > 这个类型在添加键的时候会保持顺序，因此键的迭代次序总是一致的。

- collections.ChainMap

  > 这类型可以容纳数个不同的映射对象，然后在进行键查找操作的时候，这些对象会被当作一个整体被逐个查找，直到键被找到为止。

- collections.Counter

  > 这个映射类型会给键准备一个整数计数器。每次更新一个键的时候都会增加这个计数器。

- 子类化UserDict

 ```python
  """"无论是添加、更新还是查询操作，StrKeyDict 都会把
  非字符串的键转换为字符串"""
  import collections

  class StrKeyDict(collections.UserDict):  # ➊ StrKeyDict 是对 UserDict 的扩展。
      def __missing__(self, key):  # ➋
          if isinstance(key, str):
              raise KeyError(key)
          return self[str(key)]
    
      def __contains__(self, key):
          return str(key) in self.data  # ➌ 这里可以放心假设所有已经存储的键都是字符串。因此，只要在 self.data 上查询就好了,
    
      def __setitem__(self, key, item):
          self.data[str(key)] = item  # ➍ __setitem__ 会把所有的键都转换成字符串
  d = StrKeyDict0([('2', 'two'), ('4', 'four')])
  print(d['2'])
 ```

###### 不可变映射类型MappingProxyType

> types模块中引入了一个封装类名叫MappingProxyType。如果给这个类一个映射，它就返回一个只读的映射视图。虽然是个只读视图，但是它是动态的。这意味着如果对原映射做出改动，我们通过这个视图可以观察到，但是无法通过这个视图对原映射做出修改。

```python
from types import MappingProxyType

d = {1: 'A'}
d_proxy = MappingProxyType(d)
```

###### 大多数映射类型都提供的方法：

1. setdefault

   > setdefaul方法可以用来更新字典里存放的可变值，比如列表，从而避免了重复键搜索。

2. update

   > update方法让批量更新成为可能，它可以用来插入新值或者更新已有键值对，它的参数可以是包含（key, value）这种键值对的可迭代对象，或者关键字参数。映射类型的构造方法也会利用update方法来让用户可以使用别的映射对象、可迭代对象或者关键字参数来创建新对象。

##### 集合类型

- 集合的本质是许多唯一对象的聚集。因此，集合可以用于去重。
- 集合实现了很多基础的中缀 运算符：合集|、&交集、-差集
- 查找功能速度极快（得益于集合背后的散列表）
- 空集必须写成set()
- 除了空集，集合的字符串表示形式总是以{...}的形像{1, 2, 3}这种字面量句法相比于构造方法set([1,2,3])要更快且更易读。

##### 字典dict和集合set类型背后的实现 - 散列表

###### dict的实现

- 键必须是可散列的

  > 所有由用户自定义的对象默认都是可散列的，因为它们的散列值由id()来获取，而且它们都是不相等的。

  1.  支持hash()函数，并且通过\__hash__()方法所得到的散列值是不变的；
  2.  支持通过\__eq__()方法来检测相等性；
  3.  若a == b为真，则hash(a) == hash(b) 也为真；

- 字典在内存上的开销巨大

  > 由于字典使用了散列表，而散列表又必须是稀疏的，这导致它在空间上的效率低下。

  - 用元祖取代字典就能节省空间的原因：
    1. 避免了散列表所耗费的空间；
    2. 无需把记录中字段的名字在每个元素里都存一遍

- 键查询很快

  > dict的实现是典型的空间换时间：字典类型有着巨大的内存开销，但它们提供了无视数据量大小的快速访问--只要字典能被装在内存里。

- 键的次序取决于添加顺序

  > 当往 dict 里添加新键而又发生散列冲突的时候，新键可能会被安排存放到另一个位置。

- 往字典里添加新键可能会改变已有键的顺序

  > 无论何时往字典里添加新的键，Python 解释器都可能做出为字典扩容的决定。扩容导致的结果就是要新建一个更大的散列表，并把字典里已有的元素添加到新表里。这个过程中可能会发生新的散列冲突，导致新散列表中键的次序变化。要注意的是，上面提到的这些变化是否会发生以及如何发生，都依赖于字典背后的具体实现，因此你不能很自信地说自己知道背后发生了什么。如果你在迭代一个字典的所有键的过程中同时对字典进行修改，那么这个循环很有可能会跳过一些键——甚至是跳过那些字典中已经有的键。
  >
  > 由此可知，不要对字典同时进行迭代和修改。如果想扫描并修改一个字典，最好分成两步来进行：首先对字典迭代，以得出需要添加的内容，把这些内容放在一个新字典里；迭代结束之后再对原有字典进行更新。

###### set的实现

> set 和 frozenset的实现也依赖散列表，但在它们的散列表里存放的只有元素的引用。

- 集合里的元素必须是可散列的；
- 集合很消耗内存；
- 可以很高效地判断元素是否存在于某个集合；
- 元素的次序取决于被添加到集合里的次序；
- 往集合里添加元素，可能会改变集合里已有元素的次序；

##### 文本和字节序列

###### unicode标准

- 字符的标识，即码位，是0~1114111的数字（十进制），在Unicode标准中以4~6个十六进制数字表示，而且加前缀“U+”。
- 字符的具体表述取决于所用的编码。编码是在码位和字节序列之间转换时使用的算法。
- 把码位转换成字节序列的过程是编码；把字节序列转换成码位的过程是解码。

###### 二进制序列类型

- bytes或bytearray对象的各个元素是介于0~255（含）之间的整数。

###### 处理UnicodeEncodeError

```python
city = 'São Paulo'
city.encode('utf_8')
city.encode('utf_16')
city.encode('cp437', errors='ignore') # error='ignore' 处理方式悄无声息地跳过无法编码的字符
city.encode('cp437', errors='replace') # 编码时指定 error='replace'，把无法编码的字符替换成 '?'；
city.encode('cp437', errors='xmlcharrefreplace') # 'xmlcharrefreplace' 把无法编码的字符替换成 XML 实体。
```

###### 处理UnicodeDecodeError

> 不是每一个字节都包含有效的 ASCII 字符，也不是每一个字符序列都是有效的 UTF-8 或 UTF-16。

### 特殊方法

> Python 解释器碰到特殊的句法时，会使用特殊方法去激活一些基本的对象操作。
>
> 特殊方法的存在是为了被 Python 解释器调用的。

##### \__len__

> Return the number of items in a container.

##### \__getitem__

> Return self[key]

- 使类自动支持切片（slicing）操作
- 使類變成可迭代的

##### \__init__

##### \__iter__

##### \__abs__

> 如果输入是整数或者浮点数，它返回的是输入值的绝对值；如果输入是复数（complex number），那么返回这个复数的模

##### \__repr__

> 得到一个对象的字符串表示形式

##### \__add__

> 算術運算符 +

##### \__mul__

> 算術運算符 *

##### \__bool__

> 判斷真假 返回 True 或者 False。

### 元祖嵌套列表

```python
# t[2] 被改动了，但是也有异常抛出
t = (1, 2, [30, 40])
t[2] += [50, 60]
print(t)
```

### 一个浮点型数组的创建、存入文件和从文件读取的过程

```python
from array import array
from random import random

# array.tofile 和 array.fromfile
floats = array('d', (random() for i in range(10 ** 7)))
print(floats[-1])
fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()
floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10 ** 7)
fp.close()
print(floats2[-1])
```

### 雙向隊列

```python
from collections import deque

dq = deque(range(10), maxlen=10)
```

### 不可變映射類型

```python
from types import MappingProxyType

d = {1: 'A'}
d_proxy = MappingProxyType(d)
d[2] = "b"
print(d_proxy)
```

##### 可散列类型的定义

> 如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的，而且这个对象需要实现 \_\_hash\_\_() 方法。另外可散列对象还要有 \_\_qe\_\_() 方法，这样才能跟其他键做比较。如果两个可散列对象是相等的，那么它们的散列值一定是一样的……

### 學習方式總結

> 從整體到局部：首先從整體上去把握（整體的結構是什麼？--what，整體的內容是什麼？又分為哪些部分？目的是什麼？為什麼存在？--why。通過通讀一遍的方式，把握整體的脈絡、主旨、大意，肯定會遇到問題，先對問題有個基本的印象，以便日後有針對性地掃除問題），然後從局部去逐一理解（作者為了達成目的使用了設麼方法，或者提供了什麼工具？--how），如何解決問題？wha?why?how?找到問題的突破口，引入負熵，通過搜索或尋求幫助，通過記錄筆記可以更好地實現目標。
>
> 我發現，再晦澀的內容，通過整體到局部，通過刻意練習，不斷地拆解，不斷地引入負熵理解問題，逐一去解決問題，不斷掃除障礙，掃除知識盲區，通過時間慢慢去消化，都可以將開始難以理解的內容得心應手，你的理解和能力也會有有一個質的飛越。

- Unicode 字符串、二进制序列、Unicode 文本、ASCII 文本、字节序列、码位、bytes 对象、str 对象、bytearray 类型、memoryview、array.array
- 把码位转换成字节序列的过程是编码 .encode()
- 把字节序列转换成码位的过程是解码 .decode()

```python
s = 'café'
len(s) # 'café' 字符串有 4 个 Unicode 字符。
4
b = s.encode('utf8') # 使用 UTF-8 把 str 对象编码成 bytes 对象。
b
b'caf\xc3\xa9' # bytes 字面量以 b 开头
len(b) # 字节序列 b 有 5 个字节（在 UTF-8 中，“é”的码位编码成两个字节）。
5
b.decode('utf8') # 使用 UTF-8 把 bytes 对象解码成 str 对象。
'café
```

- bytes 或 bytearray 对象的各个元素是介于 0~255（含）之间的整数

```python
cafe = bytes('café', encoding='utf_8') # bytes 对象可以从 str 对象使用给定的编码构建。
cafe # b'caf\xc3\xa9'
cafe[0] # 99 各个元素是 range(256) 内的整数。
cafe[:1] # b'c'
cafe_arr = bytearray(cafe)
cafe_arr # bytearray(b'caf\xc3\xa9') bytearray 对象没有字面量句法，而是以 bytearray() 和字节序列字面量参数的形式显示。
cafe_arr[-1:] # bytearray(b'\xa9') bytearray 对象的切片还是 bytearray 对象。
```

- 虽然二进制序列其实是整数序列，但是它们的字面量表示法表明其中有ASCII 文本。因此，各个字节的值可能会使用下列三种不同的方式显示。
  - 可打印的 ASCII 范围内的字节（从空格到 ~），使用 ASCII 字符本身。
  - 制表符、换行符、回车符和 \ 对应的字节，使用转义序列\t、\n、\r 和 \\。
  - 其他字节的值，使用十六进制转义序列（例如，\x00 是空字节）。

- memoryview 类不是用于创建或存储字节序列的，而是共享内存，让你访问其他二进制序列、打包的数组和缓冲中的数据切片，而无需复制字节序列

### 一等函数

> python函数的一等本性：可以把函数赋值给变量、传给其他函数、存储在数据结构中，以及访问函数的属性，供框架和一些工具使用。

##### 一等函数

- 在运行时创建
- 能赋值给变量或数据结构中的元素
- 能作为参数传给函数
- 能作为函数的返回结果

##### 高阶函数

- 接受函数为参数，或者把函数作为结果返回的函数是高阶函数(map,sorted,reduce)

- 常用的高阶函数：sorted、map、filter、reduce

- 归约函数

  - sum和reduce的通用思想是**把某个操作连续应用到序列的元素上**，累计之前的结果，把一系列值归约成一个值。
  - all(iterable)：如果iterable的每个元素都是真值，返回True；all([])返回True。
  - any(iterable)：只要iterable中有元素是真值，就返回True；all([])返False。

- 匿名函数lambda

  > 为了使用高阶函数，有时创建一次性的小型函数更便利。这就是匿名函数存在的原因。
  >
  > lambda只能使用纯表达式，即lambda函数的定义体中不能赋值，也不能使用while和try等python语句。
  >
  > 在参数列表中最适合使用匿名函数。

  - 除了作为参数传给高阶函数之外，python很少使用匿名函数。如果使用lambda表达式导致一段代码难以理解，则可以像下面进行重构：
    1. 编写注释，说明lambda表达式的作用；
    2. 研究一会儿注释，并找出一个名称来概括注释；
    3. 把lambda表达式转换成def语句，使用那个名称来定义函数；
    4. 删除注释

- 7种可调用对象

  - 用户定义的函数(使用 def 语句或 lambda 表达式创建)

  - 内置函数(使用 C 语言（CPython）实现的函数，如 len 或 time.strftime)

  - 内置方法(使用 C 语言实现的方法，如 dict.get)

  - 方法(在类的定义体中定义的函数)

  - 类

    ```
    调用类时会运行类的 __new__ 方法创建一个实例，然后运行__init__ 方法，初始化实例，最后把实例返回给调用方。因为 Python没有 new 运算符，所以调用类相当于调用函数。（通常，调用类会创建那个类的实例，不过覆盖 __new__ 方法的话，也可能出现其他行为。
    ```

  - 类的实例(如果类定义了\ \__call\_\_ 方法，那么它的实例可以作为函数调用)
  - 生成器函数(使用 yield 关键字的函数或方法。调用生成器函数返回的是生成器对象)

- 可调用对象

  - python中一切皆对象，函数也是对象，同时也是可调用对象（callable）。
  - 关于可调用对象，我们平时自定义的函数、内置函数和类都属于可调用对象，但凡是可以把一对括号()应用到某个对象身上都可称之为可调用对象，判断对象是否为可调用对象可以用函数 callable()
  - 一个类实例要变成一个可调用对象，只需要实现一个特殊方法\__call__()。

- 列出常规对象没有而函数有的属性

  ```python
  >>> class C: pass # ➊
  >>> obj = C() # ➋
  >>> def func(): pass # ➌
  >>> sorted(set(dir(func)) - set(dir(obj))) # ➍
  ['__annotations__', '__call__', '__closure__', '__code__', '__defaults__',
  '__get__', '__globals__', '__kwdefaults__', '__name__', '__qualname__']
  ```


###### 生成器函数

- 生成器函数是使用yield关键字的函数或方法；
- 调用生成器函数返回的是生成器对象；

###### 用户定义的可调用类型

> 只需要实现实例方法\__call__，任何python对象都可以表现得像函数。
>
> 实现\__call||方法的类是创建函数类对象的简便方式，此时必须在内部维护一个状态，让它在调用之间可用。装饰器就是这样，装饰器必须是函数，而且有时要在多次调用之间“记住”某些事。

```python
import random


class BingoCage:
    def __init__(self, items):
        self._items = list(items)  # ➊ __init__ 接受任何可迭代对象；在本地构建一个副本，防止列表参数的意外副作用.
        random.shuffle(self._items)  # ➋ shuffle 定能完成工作，因为 self._items 是列表。

    def pick(self):  # ➌ 起主要作用的方法。
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')  # ➍ 如果 self._items 为空，抛出异常，并设定错误消息。

    def __call__(self):  # ➎ bingo.pick() 的快捷方式是 bingo()。
        return self.pick()


bingo = BingoCage(range(3))
print(bingo.pick())
print(bingo())
```

###### 函数内省

- dir()函数：查看函数对象的所有属性；

- 函数使用\__dict__属性存储赋予它的用户属性；

- 函数注解

  ```
  def clip(text:str, max_len:'int > 0'=80) -> str:
  函数声明中的各个参数可以在 : 之后增加注解表达式。
  如果参数有默认值，注解放在参数名和 = 号之间。
  如果想注解返回值，在 ) 和函数声明末尾的 : 之间添加 -> 和一个表达式。那个表达式可以是任何类型。
  注解不会做任何处理，只是存储在函数的 __annotations__ 属性
  ```

###### 用户定义的函数的属性

| 名称              | 类型           | 说明                                      |
| ----------------- | -------------- | ----------------------------------------- |
| \_\_annotations__ | dict           | 参数和返回值的注解                        |
| \_\_call__        | method-wrapper | 实现 () 运算符；即可调用对象协议          |
| \_\_closure__     | tuple          | 函数闭包，即自由变量的绑定（通常是 None） |
| _\_code__         | code           | 编译成字节码的函数元数据和函数定义体      |
| _\_defaults__     | tuple          | 形式参数的默认值                          |
| _\_get__          | method-wrapper | 实现只读描述符协议                        |
| _\_globals__      | dict           | 函数所在模块中的全局变量                  |
| _\_kwdefaults__   | dict           | 仅限关键字形式参数的默认值                |
| _\_name__         | str            | 函数名称                                  |
| _\_qualname__     | str            | 函数的限定名称，如 Random.choice          |

###### 参数处理机制

> ython 最好的特性之一是提供了极为灵活的参数处理机制。

- 如果不想支持数量不定的定位参数，但是想支持仅限关键字参数，在签名中放一个 *

  ```python
  >>> def f(a, *, b):
  ... return a, b
  ...
  >>> f(1, b=2)
  (1, 2)
  ```

###### 函数注解

> 用于为函数声明中的**参数**和**返回值**附加元数据。
>
> 函数声明中的各个参数可以在 : 之后增加注解表达式。
>
> ​	如果参数有默认值，注解放在参数名和 = 号之间。
>
> ​	如果想注解返回值，在 ) 和函数声明末尾的 : 之间添加 -> 和一个表达式。那个表达式可以是任何类型。注解中最常用的类型是类（如 str 或 int）和字符串（如 'int >0'）
>
> 注解不会做任何处理，只是存储在函数的 _\_annotations__ 属性（一个字典）中
>
> 注解对 Python 解释器没有任何意义。注解只是**元数据**，可以供 IDE、框架和装饰器等工具使用。





###### 支持函数式编程的包 - operator模块

> 在函数式编程中，经常需要把算术运算符当作函数使用。
>
> operator 模块为多个算术运算符提供了对应的函数：算术运算符函数
>
> itemgetter 使用 [] 运算符，因此它不仅支持序列，还支持映射和任何实现 \__getitem__ 方法的类。

- 使用reduce函数和一个匿名函数计算阶乘

  ```python
  from functools import reduce
  def fact(n):
  	return reduce(lambda a, b: a*b, range(1, n+1))
  ```

- 使用 reduce 和 operator.mul 函数计算阶乘

  ```python
  from functools import reduce
  from operator import mul
  def fact(n):
  	return reduce(mul, range(1, n+1))
  ```

- operator 模块中还有一类函数，能替代从序列中取出元素或读取对象属性的 lambda 表达式：因此，itemgetter 和 attrgetter 其实会自行构建函数：

  - 使用itemgetter排序一个元祖列表

    ```python
    metro_data = [
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
    ]

    from operator import itemgetter
    # 按照国家代码（第 2 个字段）的顺序打印各个城市的信息。
    for city in sorted(metro_data, key=itemgetter(1)):
        print(city)
    ```

  - 如果把多个参数传给 itemgetter，它构建的函数会返回提取的值构成的元组：

    ```python
    metro_data = [
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
    ]

    from operator import itemgetter

    cc_name = itemgetter(1, 0)
    for city in metro_data:
        print(cc_name(city))

    """('JP', 'Tokyo')
    ('IN', 'Delhi NCR')
    ('MX', 'Mexico City')
    ('US', 'New York-Newark')
    ('BR', 'Sao Paulo')"""
    ```

  - attrgetter

    > 它创建的函数根据名称提取对象的属性。
    >
    > 如果把多个属性名传给 attrgetter，它也会返回提取的值构成的元组。
    >
    > 此外，如果参数名中包含 .（点号），attrgetter 会深入嵌套对象，获取指定的属性。

    ```python
    metro_data = [
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
    ]
    
    from collections import namedtuple
    
    LatLong = namedtuple('LatLong', 'lat long')  # ➊ 使用 namedtuple 定义 LatLong。
    Metropolis = namedtuple('Metropolis', 'name cc pop coord')  # ➋ 再定义 Metropolis。
    
    # ➌ 使用 Metropolis 实例构建 metro_areas 列表；注意，我们使用嵌套的元组拆包提取 (lat, long)，然后使用它们构建 LatLong，作为 Metropolis 的 coord 属性。
    metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) for name, cc, pop, (lat, long) in metro_data]
    print(metro_areas[0])
    # Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722, long=139.691667))
    
    Metropolis(name='Tokyo', cc='JP', pop=36.933, coord=LatLong(lat=35.689722, long=139.691667))
    print(metro_areas[0].coord.lat)  # ➍ 深入 metro_areas[0]，获取它的纬度。
    # 35.689722
    
    from operator import attrgetter
    
    name_lat = attrgetter('name', 'coord.lat')  # ➎ 定义一个 attrgetter，获取 name 属性和嵌套的 coord.lat 属性。
    for city in sorted(metro_areas, key=attrgetter('coord.lat')):  # ➏ 再次使用 attrgetter，按照纬度排序城市列表。
        print(name_lat(city))  # ➐ 使用标号❺中定义的 attrgetter，只显示城市名和纬度。
    """('Sao Paulo', -23.547778)
    ('Mexico City', 19.433333)
    ('Delhi NCR', 28.613889)
    ('Tokyo', 35.689722)
    ('New York-Newark', 40.808611)"""

  - methodcaller

    > methodcaller创建的函数会在对象上调用参数指定的方法。

    ```python
    from operator import methodcaller
    
    s = 'The time has come'
    upcase = methodcaller('upper')
    print(upcase(s))
    'THE TIME HAS COME'
    hiphenate = methodcaller('replace', ' ', '-')
    print(hiphenate(s))
    'The-time-has-come'
    
    str.upper(s)
    'THE TIME HAS COME'
    ```

###### 使用functools.partial冻结参数

- functools.partial

  > 用于部分应用一个函数。部分应用是指，基于一个函数创建一个新的可调用对象，把原函数的某些参数固定。使用这个函数可以把接受一个或多个参数的函数改编成需要回调的API，这样参数更少。

  - 使用partial把一个两参数函数改编成需要单参数的可调用对象

    ```python
    from operator import mul
    from functools import partial
    triple = partial(mul, 3)
    triple(7)
    21
    >>> list(map(triple, range(1, 10)))
    [3, 6, 9, 12, 15, 18, 21, 24, 27]
    ```

### 装饰器

> 函数装饰器用于在源码中“标记”函数，以某种方式增强函数的行为

- 装饰器的特性：
  - 能把被装饰的函数替换成其他函数。
  - 装饰器在加载模块时立即执行，而被装饰的函数只在明确调用时运行。
- 函数中赋值时想把解释器当成全局变量，要使用global声明。
- python内置了三个用于装饰方法的函数：property、calssmethod和staticmethod


- 装饰器是可调用的对象，其参数是另一个函数（被装饰的函数）

  ```python
  @decorate
  def target():
  	print('running target()')

  # 上述代码的效果与下述写法一样：
  def target():
  	print('running target()')
  target = decorate(target)
  ```

- 装饰器通常把函数替换成另一个函数

  ```python
  def deco(func):
      def inner():
          print('running inner()')
  
      return inner
  @deco
  def target():
  	print('running target()')
      
  target() # 调用被装饰的 target 其实会运行 inner。
  # running inner()
  print(target) # 审查对象，发现 target 现在是 inner 的引用。
  ```


- 装饰器在加载模块时立即执行

  > 装饰器的一个关键特性是，它们在被装饰的函数定义之后立即运行。这通常是在导入时（即 Python 加载模块时）
  >
  > register 装饰器原封不动地返回被装饰的函数，但是这种技术并非没有用处。很多 Python Web 框架使用这样的装饰器把函数添加到某种中央注册处，例如把 URL 模式映射到生成 HTTP 响应的函数上的注册处。这种注册装饰器可能会也可能不会修改被装饰的函数。


 ```python
# 函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行。
  registry = []  # ➊ registry 保存被 @register 装饰的函数引用。


  def register(func):  # ➋ register 的参数是一个函数。
      print('running register(%s)' % func)  # ➌ 为了演示，显示被装饰的函数。
      registry.append(func)  # ➍  把 func 存入 registry。
      return func  # ➎ 返回 func：必须返回函数；这里返回的函数与通过参数传入的一样。


  @register  # ➏ f1 和 f2 被 @register 装饰。
  def f1():
      print('running f1()')


  @register
  def f2():
      print('running f2()')


  def f3():  # ➐ f3 没有装饰。
      print('running f3()')


  def main():  # ➑ main 显示 registry，然后调用 f1()、f2() 和 f3()。
      print('running main()')
      print('registry ->', registry)
      f1()
      f2()
      f3()


  if __name__ == '__main__':
      main()  # ➒ 只有把 registration.py 当作脚本运行时才调用 main()。

  """
  running register(<function f1 at 0x000002BD10616488>)
  running register(<function f2 at 0x000002BD10616620>)
  running main()
  registry -> [<function f1 at 0x000002BD10616488>, <function f2 at 0x000002BD10616620>]
  running f1()
  running f2()
  running f3()
  """
  # ，register 在模块中其他函数之前运行（两次）。调用register 时，传给它的参数是被装饰的函数
  # 加载模块后，registry 中有两个被装饰函数的引用：f1 和 f2。这两个函数，以及 f3，只在 main 明确调用它们时才执行。
  """
  1.装饰器函数与被装饰的函数在同一个模块中定义。实际情况是，装饰器通常在一个模块中定义，然后应用到其他模块中的函数上。
  2.register 装饰器返回的函数与通过参数传入的相同。实际上，大多数装饰器会在内部定义一个函数，然后将其返回。
  """
 ```

  - 如果导入 registration.py 模块（不作为脚本运行）

    ```python
    import registration
    running register(<function f1 at 0x10063b1e0>)
    running register(<function f2 at 0x10063b268>)
    
    # 此时查看 registry 的值，得到的输出如下：
    registration.registry
    [<function f1 at 0x10063b1e0>, <function f2 at 0x10063b268>]
    ```

##### 闭包

> 闭包指延伸了作用域的函数，其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。函数是不是匿名的没有关系，关键是它**能访问定义体之外定义的非全局变量**。
>
> 闭包是一种函数，它会保留定义函数时存在的自由变量的绑定，这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定。只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量。
>
> 闭包不仅在装饰器中有用，而且还是回调式异步编程和函数式编程风格的基础。

```python
"""闭包
	series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)
"""
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value) # series是自由变量
        total = sum(series)
        return total / len(series)

    return averager
```



```python
"""
调用 Averager() 或make_averager() 得到一个可调用对象 avg，它会更新历史值，然后计算当前均值。
"""


# 计算移动平均值的类
class Averager():
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)


# avg = Averager()


# 计算移动平均值的高阶函数
def make_averager():
    series = []

    def averager(new_value):
        # 没有给 series 赋值，我们只是调用 series.append，并把它传给 sum 和 len。也就是说，我们利用了列表是可变的对象这一事实。
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager


avg = make_averager()
print(avg(10))
print(avg(11))
print(avg(12))
```

- 计算移动平均值的高阶函数，不保存所有历史值，但有缺陷

  ```python
  """
  当 count 是数字或任何不可变类型时，count += 1 语句的作用其实与 count = count + 1 一样。因此，我们在 averager 的定义体中为 count 赋值了，这会把 count 变成局部变量。total 变量也受这个问题影响。
  
  对数字、字符串、元组等不可变类型来说，只能读取，不能更新。如果尝试重新绑定，例如 count = count + 1，其实会隐式创建局部变量 count。这样，count 就不是自由变量了，因此不会保存在闭包中。为了解决这个问题，Python 3 引入了 nonlocal 声明
  """
  def make_averager():
      count = 0
      total = 0
  
      def averager(new_value):
          count += 1  # 在 averager 的定义体中为 count 赋值了，这会把 count 变成局部变量
          total += new_value
          return total / count
  
      return averager
  ```


- nonlocal的作用

  > 把变量标记为自由变量，即使在函数中为变量赋予新值了，也会变成自由变量。如果为 nonlocal 声明的变量赋予新值，闭包中保存的绑定会更新。

 ```python
# 计算移动平均值，不保存所有历史（使用 nonlocal 修正）
def make_averager():
  count = 0
  total = 0
  def averager(new_value):
    nonlocal count, total
    count += 1
    total += new_value
    return total / count
  return averager
 ```

- 应用于装饰器，也是回调式异步编程和函数式编程风格的基础

- 如果在函数中赋值时想让解释器把 b 当成全局变量，要使用 global 声明：



- 装饰器不修改被装饰的函数

  - 促销策略函数无需使用特殊的名称（即不用以 _promo 结尾）。
  - @promotion 装饰器突出了被装饰的函数的作用，还便于临时禁用某个促销策略：只需把装饰器注释掉。
  - 促销折扣策略可以在其他模块中定义，在系统中的任何地方都行，只要使用 @promotion 装饰即可。

 ```python

from abc import ABC, abstractmethod
from collections import namedtuple

  Customer = namedtuple('Customer', 'name fidelity')


  class LineItem:

      def __init__(self, product, quantity, price):
          self.product = product
          self.quantity = quantity
          self.price = price

      def total(self):
          return self.price * self.quantity


  class Order:  # 上下文
      def __init__(self, customer, cart, promotion=None):
          self.customer = customer
          self.cart = list(cart)
          self.promotion = promotion

      def total(self):
          if not hasattr(self, '__total'):
              self.__total = sum(item.total() for item in self.cart)
          return self.__total

      def due(self):
          if self.promotion is None:
              discount = 0
          else:
              discount = self.promotion.discount(self)
          return self.total() - discount

      def __repr__(self):
          fmt = '<Order total: {:.2f} due: {:.2f}>'
          return fmt.format(self.total(), self.due())


  promos = []  # ➊ promos 列表起初是空的。


  def promotion(promo_func):  # ➋ promotion 把 promo_func 添加到 promos 列表中，然后原封不动地将其返回。
      promos.append(promo_func)
      return promo_func


  @promotion  # ➌ 被 @promotion 装饰的函数都会添加到 promos 列表中。
  def fidelity(order):
      """为积分为1000或以上的顾客提供5%折扣"""
      return order.total() * .05 if order.customer.fidelity >= 1000 else 0


  @promotion
  def bulk_item(order):
      """单个商品为20个或以上时提供10%折扣"""
      discount = 0
      for item in order.cart:
          if item.quantity >= 20:
              discount += item.total() * .1
      return discount


  @promotion
  def large_order(order):
      """订单中的不同商品达到10个或以上时提供7%折扣"""
      distinct_items = {item.product for item in order.cart}
      if len(distinct_items) >= 10:
          return order.total() * .07
      return 0


  def best_promo(order):  # ➍ best_promos 无需修改，因为它依赖 promos 列表。
      """选择可用的最佳折扣
      """
      return max(promo(order) for promo in promos)
 ```

- 装饰器会修改被装饰的函数(通常，它们会定义一个内部函数，然后将其返回，替换被装饰的函数。使用内部函数的代码几乎都要靠闭包才能正确运作。)

##### 一个简单的装饰器，输出函数的运行时间

```python
# 在每次调用被装饰的函数时计时，然后把经过的时间、传入的参数和调用的结果打印出来。
import time


def clock(func):
    def clocked(*args):  # ➊ 定义内部函数 clocked，它接受任意个定位参数。
        t0 = time.perf_counter()
        result = func(*args)  # ➋ 这行代码可用，是因为 clocked 的闭包中包含自由变量 func。
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result

    return clocked  # ➌ 返回内部函数，取代被装饰的函数。示例 7-16 演示了 clock 装饰器的用法。


@clock
def snooze(seconds):
    time.sleep(seconds)


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


if __name__ == '__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))

"""
**************************************** Calling snooze(.123)
[0.13714430s] snooze(0.123) -> None
**************************************** Calling factorial(6)
[0.00000200s] factorial(1) -> 1
[0.00008190s] factorial(2) -> 2
[0.00011430s] factorial(3) -> 6
[0.00013500s] factorial(4) -> 24
[0.00015500s] factorial(5) -> 120
[0.00017970s] factorial(6) -> 720
6! = 720
"""
```

```python
@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)
# 等价于：
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)

factorial = clock(factorial)
```

- factorial 会作为 func 参数传给 clock。然后， clock 函数会返回 clocked 函数，Python 解释器在背后会把 clocked 赋值给 factorial。其实，导入clockdeco_demo 模块后查看 factorial 的 \__name__ 属性，会得到如下结果：

  ```python
  clockdeco_demo.factorial.__name__
  # 'clocked'
  ```

- 所以，现在 factorial 保存的是 clocked 函数的引用。自此之后，每次调用 factorial(n)，执行的都是clocked(n)。clocked 大致做了下面几件事：
  - (1) 记录初始时间 t0。
  - (2) 调用原来的 factorial 函数，保存结果。
  - (3) 计算经过的时间。
  - (4) 格式化收集的数据，然后打印出来。
  - (5) 返回第 2 步保存的结果。

- 装饰器的典型行为：把被装饰的函数替换成新函数，二者接受相同的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做些额外操作。

- 上面实现的 clock 装饰器有几个缺点：不支持关键字参数，而且遮盖了被装饰函数的\ \__name\_\_ 和 \_\_doc\_\_ 属性。使用functools.wraps 装饰器把相关的属性从 func 复制到 clocked 中。此外，这个新版还能正确处理关键字参数。

  - functools.wraps装饰器把相关的属性从func复制到clocked中

    ```python
    # 在每次调用被装饰的函数时计时，然后把经过的时间、传入的参数和调用的结果打印出来。
    import time
    import functools
    
    
    def clock(func):
        @functools.wraps(func)
        def clocked(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - t0
            name = func.__name__
            arg_lst = []
            if args:
                arg_lst.append(', '.join(repr(arg) for arg in args))
            if kwargs:
                pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
                arg_lst.append(', '.join(pairs))
            arg_str = ', '.join(arg_lst)
            print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
            return result
    
        return clocked
    
    
    @clock
    def snooze(seconds):
        time.sleep(seconds)
    
    
    @clock
    def factorial(n):
        return 1 if n < 2 else n * factorial(n - 1)
    
    
    if __name__ == '__main__':
        print('*' * 40, 'Calling snooze(.123)')
        snooze(.123)
        print('*' * 40, 'Calling factorial(6)')
        print('6! =', factorial(6))
        print(factorial.__name__)
    
    """
    **************************************** Calling snooze(.123)
    [0.13714430s] snooze(0.123) -> None
    **************************************** Calling factorial(6)
    [0.00000200s] factorial(1) -> 1
    [0.00008190s] factorial(2) -> 2
    [0.00011430s] factorial(3) -> 6
    [0.00013500s] factorial(4) -> 24
    [0.00015500s] factorial(5) -> 120
    [0.00017970s] factorial(6) -> 720
    6! = 720
    factorial
    """
    ```


##### functools.lru_cache装饰器

- 使用functools.lru_cache做备忘，这是一项优化技术
- 它把耗时的函数的结果保存起来，避免传入相同的参数时重复计算。
- 。LRU 三个字母是“LeastRecently Used”的缩写，表明缓存不会无限制增长，一段时间不用的缓存条目会被扔掉。
- 除了优化递归算法之外，lru_cache 在从 Web 中获取信息的应用中也能发挥巨大作用。

 ```python
import time
import functools


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result

    return clocked


# 生成第 n 个斐波纳契数，递归方式非常耗时
@clock
def fibon(n):
    if n < 2:
        return n
    return fibon(n - 2) + fibon(n - 1)

# 使用缓存实现，速度更快。
# 注意，必须像常规函数那样调用 lru_cache。这一行中有一对括号：@functools.lru_cache()。这么做的原因是，lru_cache 可以接受配置参数
@functools.lru_cache()
@clock  # 这里叠放了装饰器：@lru_cache() 应用到 @clock 返回的函数上。
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


if __name__ == '__main__':
    print(fibonacci(30))
 ```

- lru_cache 可以使用两个可选的参数来配置

  - maxsize 参数指定存储多少个调用的结果。缓存满了之后，旧的结果会被扔掉，腾出空间。为了得到最佳性能，maxsize 应该设为 2 的幂。
  - typed 参数如果设为 True，把不同参数类型得到的结果分开保存，即把通常认为相等的浮点数和整数参数（如 1 和 1.0）区分开。

  ```python
  functools.lru_cache(maxsize=128, typed=False)
  ```

- 因为 lru_cache 使用字典存储结果，而且键根据调用时传入的定位参数和关键字参数创建，所以被 lru_cache 装饰的函数，它的所有参数都必须是可散列的。

##### functools.singledispatch装饰器

- 可以把整体方案拆分成多个模块，甚至可以为你无法修改的类提供专门的函数。
- @singledispatch 装饰的普通函数会变成泛函数（generic function）：根据第一个参数的类型，以不同方式执行相同操作的一组函数。
- singledispatch 机制的一个显著特征是，你可以在系统的任何地方和任何模块中注册专门函数。如果后来在新的模块中定义了新的类型，可以轻松地添加一个新的专门函数来处理那个类型。此外，你还可以为不是自己编写的或者不能修改的类添加自定义函数。

```python
"""
只要可能，注册的专门函数应该处理抽象基类（如 numbers.Integral和 abc.MutableSequence），不要处理具体实现（如 int 和list）。这样，代码支持的兼容类型更广泛。例如，Python 扩展可以子类化 numbers.Integral，使用固定的位数实现 int 类型。
"""
from functools import singledispatch
from collections import abc
import numbers
import html


@singledispatch  # ➊ @singledispatch 标记处理 object 类型的基函数。
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)


@htmlize.register(str)  # ➋ 各个专门函数使用 @«base_function».register(«type») 装饰。
def _(text):  # ➌ 专门函数的名称无关紧要；_ 是个不错的选择，简单明了。
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)


@htmlize.register(numbers.Integral)  # ➍ 为每个需要特殊处理的类型注册一个函数。numbers.Integral 是int 的虚拟超类。
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)


@htmlize.register(tuple)  # ➎ 可以叠放多个 register 装饰器，让同一个函数支持不同类型。
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

print(htmlize(['alpha', 66, {3, 2, 1}]))
"""
<ul>
<li><p>alpha</p></li>
<li><pre>66 (0x42)</pre></li>
<li><pre>{1, 2, 3}</pre></li>
</ul>"""
```

##### 叠放装饰器

- 把 @d1 和 @d2 两个装饰器按顺序应用到 f 函数上，作用相当于 f =d1(d2(f))。

  ```python
  @d1
  @d2
  def f():
  	print('f')
      
  # 等同于：
  def f():
  	print('f')
  f = d1(d2(f))
  ```

##### 参数化装饰器

```python
registry = set()  # ➊ registry 现在是一个 set 对象，这样添加和删除函数的速度更快。


def register(active=True):  # ➋ register 接受一个可选的关键字参数。
    def decorate(func):  # ➌ decorate 这个内部函数是真正的装饰器；注意，它的参数是一个函数。
        print('running register(active=%s)->decorate(%s)' % (active, func))
        if active:  # ➍ 只有 active 参数的值（从闭包中获取）是 True 时才注册 func。
            registry.add(func)
        else:
            registry.discard(func)  # ➎ 如果 active 不为真，而且 func 在 registry 中，那么把它删除。
        return func  # ➏ decorate 是装饰器，必须返回一个函数。

    return decorate  # ➐ register 是装饰器工厂函数，因此返回 decorate。


@register(active=False)  # ➑ @register 工厂函数必须作为函数调用，并且传入所需的参数。
def f1():
    print('running f1()')


# （@register()），即要返回真正的装饰器 decorate。这里的关键是，register() 要返回 decorate，然后把它应用到被装饰的函数上。
@register()  # ➒ 即使不传入参数，register 也必须作为函数调用
def f2():
    print('running f2()')


def f3():
    print('running f3()')


f1()
print(registry)
```

- 如果不使用 @ 句法，那就要像常规函数那样使用 register；
- 若想把 f添加到 registry 中，则装饰 f 函数的句法是 register()(f)；
- 不想添加（或把它删除）的话，句法是 register(active=False)(f)。

```
>>> from registration_param import * 
running register(active=False)->decorate(<function f1 at 0x10073c1e0>)
running register(active=True)->decorate(<function f2 at 0x10073c268>)
>>> registry # ➊ 导入这个模块时，f2 在 registry 中。
{<function f2 at 0x10073c268>}
>>> register()(f3) # ➋ register() 表达式返回 decorate，然后把它应用到 f3 上。
running register(active=True)->decorate(<function f3 at 0x10073c158>)
<function f3 at 0x10073c158>
>>> registry # ➌ 前一行把 f3 添加到 registry 中。
{<function f3 at 0x10073c158>, <function f2 at 0x10073c268>}
>>> register(active=False)(f2) # ➍ 这次调用从 registry 中删除 f2。
running register(active=False)->decorate(<function f2 at 0x10073c268>)
<function f2 at 0x10073c268>
>>> registry # ➎ 确认 registry 中只有 f3。
{<function f3 at 0x10073c158>}
```

- 参数化clock装饰器

  ```python
  import time
  
  DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'
  
  
  def clock(fmt=DEFAULT_FMT):  # ➊ clock 是参数化装饰器工厂函数。
    def decorate(func):  # ➋ decorate 是真正的装饰器。
        def clocked(*_args):  # ➌ clocked 包装被装饰的函数。
            t0 = time.time()
            _result = func(*_args)  # ➍ _result 是被装饰的函数返回的真正结果。
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)  # ➎ _args 是 clocked 的参数，args 是用于显示的字符串。
            result = repr(_result)  # ➏ result 是 _result 的字符串表示形式，用于显示。
            print(fmt.format(**locals()))  # ➐ 这里使用 **locals() 是为了在 fmt 中引用 clocked 的局部变量。
            return _result  # ➑ clocked 会取代被装饰的函数，因此它应该返回被装饰的函数返回的值。
        return clocked  # ➒ decorate 返回 clocked。
    return decorate  # ➓ clock 返回 decorate。
  
  
  if __name__ == '__main__':
    @clock()
    # @clock('{name}: {elapsed}s')
    # @clock('{name}({args}) dt={elapsed:0.3f}s')
    def snooze0(seconds):
        time.sleep(seconds)
  
  
    for i in range(3):
        snooze0(.123)
  """
  [0.12412500s] snooze(0.123) -> None
  [0.12411904s] snooze(0.123) -> None
  [0.12410498s] snooze(0.123) -> None
  """
  ```


### 标识、相等性和别名

- == 运算符比较两个对象的值（对象中保存的数据），而 is 比较对象的标识。

- == 比较的是值，调用\__eq__ 方法
- is 运算符比较两个对象的标识；id() 函数返回对象标识的整数表示。
- 对象 ID 的真正意义在不同的实现中有所不同。在 CPython 中，id() 返回对象的内存地址，但是在其他 Python 解释器中可能是别的值。关键是，ID 一定是唯一的数值标注，而且在对象的生命周期中绝不会变。

##### 元祖的相对不可变性

- 元组与多数 Python 集合（列表、字典、集，等等）一样，保存的是对象的引用。
- 如果引用的元素是可变的，即便元组本身不可变，元素依然可变。也就是说，元组的不可变性其实是指 tuple 数据结构的物理内1容（即保存的引用）不可变，与引用的对象无关。
- str、bytes 和 array.array 等单一类型序列是扁平的，它们保存的不是引用，而是在连续的内存中保存数据本身（字符、字节和数字）。

- copy模块：提供的 deepcopy 和 copy 函数能为任意对象做深复制和浅复制。

##### 函数的参数作为引用时

- 共享传参指函数的各个形式参数获得实参中各个引用的副本。也就是说，函数内部的形参是实参的别名。

 ```python
def f(a, b):
    a += b
    return a


x = 1
y = 2
f(x, y)  # 3
# x, y  # ➊ (1, 2) 数字 x 没变。
a = [1, 2]
b = [3, 4]
f(a, b)  # [1, 2, 3, 4]
# a, b ➋ 列表 a 变了。
# ([1, 2, 3, 4], [3, 4])
t = (10, 20)
u = (30, 40)
f(t, u)  # (10, 20, 30, 40)
# t, u ➌ 元组 t 没变。
# ((10, 20), (30, 40))
 ```

##### 避免使用可变的对象作为参数的默认值。

```python
class HauntedBus:
    """备受幽灵乘客折磨的校车"""

    def __init__(self, passengers=[]):  # ➊ 如果没传入 passengers 参数，使用默认绑定的列表对象，一开始是空列表。
        self.passengers = passengers  # ➋ 这个赋值语句把 self.passengers 变成 passengers 的别名，而没有传入 passengers 参数时，后者又是默认列表的别名。

    def pick(self, name):
        self.passengers.append(name)  # ➌ 在 self.passengers 上调用 .remove() 和 .append() 方法时，修改的其实是默认列表，它是函数对象的一个属性。

    def drop(self, name):
        self.passengers.remove(name)


bus1 = HauntedBus(['Alice', 'Bill'])
print(bus1.passengers)
# ['Alice', 'Bill']
bus1.pick('Charlie')
bus1.drop('Alice')
print(bus1.passengers)  # ➊ 目前没什么问题，bus1 没有出现异常。
# ['Bill', 'Charlie']
bus2 = HauntedBus()  # ➋ 一开始，bus2 是空的，因此把默认的空列表赋值给self.passengers。
bus2.pick('Carrie')
print(bus2.passengers)
# ['Carrie']
bus3 = HauntedBus()  # ➌ bus3 一开始也是空的，因此还是赋值默认的列表。
print(bus3.passengers)  # ➍ 但是默认列表不为空！
# ['Carrie']
bus3.pick('Dave')
print(bus2.passengers)  # ➎ 登上 bus3 的 Dave 出现在 bus2 中。
# ['Carrie', 'Dave']
print(bus2.passengers is bus3.passengers)  # ➏ 问题是，bus2.passengers 和 bus3.passengers 指代同一个列表。
# True
print(bus1.passengers)  # ➐ 但 bus1.passengers 是不同的列表。
# ['Bill', 'Charlie']

print(dir(HauntedBus.__init__))
# ['__annotations__', '__call__', ..., '__defaults__', ...]
print(HauntedBus.__init__.__defaults__)
# (['Carrie', 'Dave'],)
print(HauntedBus.__init__.__defaults__[0] is bus2.passengers)
# True
```

##### 防御可变参数

```python
class TwilightBus:
    """让乘客销声匿迹的校车"""

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []  # ➊ 这里谨慎处理，当 passengers 为 None 时，创建一个新的空列表。
        else:
            self.passengers = passengers  # ➋ 然而，这个赋值语句把 self.passengers 变成 passengers 的别名，而后者是传给 __init__ 方法的实参的别名。
            
    """
        在内部像这样处理乘客列表，就不会影响初始化校车时传入的参数了。此外，这种处理方式还更灵活：现在，传给 passengers 参数的值可以    是元组或任何其他可迭代对象，例如 set 对象，甚至数据库查询结果，因为 list 构造方法接受任何可迭代对象。自己创建并管理列表可以确保支持所需的 .remove() 和 .append() 操作，这样 .pick() 和    .drop() 方法才能正常运作。
    """
            # self.passengers = list(passengers)  # 创建 passengers 列表的副本；如果不是列表，就把它转换成列表。

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)  # ➌ 在 self.passengers 上调用 .remove() 和 .append() 方法其实会修改传给构造方法的那个列表。

```

- 每个对象都会统计有多少引用指向自己。当引用计数归零时，对象立即就被销毁：CPython 会在对象上调用 \__del__ 方法（如果定义了），然后释放分配给对象的内存。
- 正是因为有引用，对象才会在内存中存在。当对象的引用数量归零后，垃圾回收程序会把对象销毁。但是，有时需要引用对象，而不让对象存在的时间超过所需时间。这经常用在缓存中。
- 弱引用不会增加对象的引用数量。引用的目标对象称为所指对象（referent）。因此我们说，弱引用不会妨碍所指对象被当作垃圾回收。

##### WeakValueDictionary 类

> 实现的是一种可变映射，里面的值是对象的弱引用。被引用的对象在程序中的其他地方被当作垃圾回收后，对应的键会自动从 WeakValueDictionary 中删除。因此，WeakValueDictionary 经常用于缓存。

##### 变量保存的是引用

- 简单的赋值不创建副本。
- 对 += 或 *= 所做的增量赋值来说，如果左边的变量绑定的是不可变对象，会创建新对象；如果是可变对象，会就地修改。
- 为现有的变量赋予新值，不会修改之前绑定的变量。这叫重新绑定：现在变量绑定了其他对象。如果变量是之前那个对象的最后一个引用，对象会被当作垃圾回收。
- 函数的参数以别名的形式传递，这意味着，函数可能会修改通过参数传入的可变对象。这一行为无法避免，除非在本地创建副本，或者使用不可变对象（例如，传入元组，而不传入列表）。
- 使用可变类型作为函数参数的默认值有危险，因为如果就地修改了参数，默认值也就变了，这会影响以后使用默认值的调用。
- 在 CPython 中，对象的引用数量归零后，对象会被立即销毁。如果除了循环引用之外没有其他引用，两个对象都会被销毁。
- 在cpython中，立即回收使用的主要算法是引用计数（后来增加了分代回收算法）。在对象上调用\__del__方法，然后释放分配给对象的内存。
- 某些情况下，可能需要保存对象的引用，但不留存对象本身。例如，有一个类想要记录所有实例。这个需求可以使用弱引用实现，这是一种低层机制，是weakref 模块中 WeakValueDictionary、WeakKeyDictionary 和WeakSet 等有用的集合类，以及 finalize 函数的底层支持。
- 分代垃圾回收程序，能把引用循环中不可获取的对象销毁。

##### 弱引用

- 正是因为有引用，对象才会在内存中存在。

- 有时需要引用对象，而不让对象存在的时间超过所需时间。这经常用在缓存中。

- 弱引用不会增加对象的引用数量。所以，若引用不会妨碍所指对象被当作垃圾回收。

- 弱引用是可调用的对象，返回的是被引用的对象；如果所指对象不存在了，返回None

  ```python
  import weakref

  a_set = {0, 1}
  wref = weakref.ref(a_set)  # ➊ 创建弱引用对象 wref，下一行审查它。
  print(wref)
  # <weakref at 0x100637598; to 'set' at 0x100636748>
  print(wref())  # ➋ 调用 wref() 返回的是被引用的对象，{0, 1}
  # {0, 1}
  a_set = {2, 3, 4}  # ➌ a_set 不再指代 {0, 1} 集合，因此集合的引用数量减少了。但是 _变量仍然指代它.
  print(wref())  # ➍ 调用 wref() 依旧返回 {0, 1}。
  # {0, 1}
  print(wref() is None)  # ➎ 计算这个表达式时，{0, 1} 存在，因此 wref() 不是 None。但是，随后 _ 绑定到结果值 False。现在 {0, 1} 没有强引用了.
  # False
  print(wref() is None)  # ➏ 因为 {0, 1} 对象不存在了，所以 wref() 返回 None。
  # True
  ```

- WeakValueDictionary简介

  > WeakValueDictionary 类实现的是一种可变映射，里面的值是对象的弱引用。被引用的对象在程序中的其他地方被当作垃圾回收后，对应的键会自动从 WeakValueDictionary 中删除。因此，WeakValueDictionary 经常用于缓存。

  ```python
  class Cheese:
        def __init__(self, kind):
            self.kind = kind
    
        def __repr__(self):
            return 'Cheese(%r)' % self.kind
  
  
    import weakref
  
    stock = weakref.WeakValueDictionary()  # ➊ stock 是 WeakValueDictionary 实例。
    catalog = [Cheese('Red Leicester'), Cheese('Tilsit'),
               Cheese('Brie'), Cheese('Parmesan')]
    for cheese in catalog:
        stock[cheese.kind] = cheese  # ➋ stock 把奶酪的名称映射到 catalog 中 Cheese 实例的弱引用上。
  
    print(sorted(stock.keys()))
    # ['Brie', 'Parmesan', 'Red Leicester', 'Tilsit'] ➌ stock 是完整的。
    del catalog
    print(sorted(stock.keys()))
  
    # ['Parmesan'] ➍ 删除 catalog 之后，stock 中的大多数奶酪都不见了，这是WeakValueDictionary 的预期行为。为什么不是全部呢？
    del cheese
    print(sorted(stock.keys()))
  ```

### 符合python风格的对象

> 得益于 Python 数据模型，自定义类型的行为可以像内置类型那样自然。实现如此自然的行为，靠的不是继承，而是鸭子类型（duck typing）：我们只需按照预定行为实现对象所需的方法即可。

> 我们通过一个简单的类说明了如何利用数据模型处理 Python 的其他功能：提供不同的对象表示形式、实现自定义的格式代码、公开只读属性，以及通过 hash() 函数支持集合和映射。
>
> 目的是说明，如何使用特殊方法和约定的结构，定义行为良好且符合 Python 风格的类。

##### Vector2d 实例有多种表示形式

```python
from array import array
import math


class Vector2d:
    typecode = 'd'  # ➊ typecode 是类属性，在 Vector2d 实例和字节序列之间转换时使用。

    def __init__(self, x, y):
        self.x = float(x)  # ➋ 在 __init__ 方法中把 x 和 y 转换成浮点数，尽早捕获错误，以防调用 Vector2d 函数时传入不当参数。
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x,
                            self.y))  # ➌ 定义 __iter__ 方法，把 Vector2d 实例变成可迭代的对象，这样才能拆包（例如，x, y = my_vector）。这个方法的实现方式很简单，直接调用生成器表达式一个接一个产出分量。

    def __repr__(self):
        # 如果硬编码 class_name 的值，那么 Vector2d 的子类（如ShortVector2d）要覆盖 __repr__ 方法，只是为了修改 class_name的值。从实例的类型中读取类名，__repr__ 方法就可以放心继承。
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)  # ➍ __repr__ 方法使用 {!r} 获取各个分量的表示形式，然后插值，构成一个字符串；因为 Vector2d 实例是可迭代的对象，所以 *self 会把x 和 y 分量提供给 format 函数。

    def __str__(self):
        return str(tuple(self))  # ➎ 从可迭代的 Vector2d 实例中可以轻松地得到一个元组，显示为一个有序对。

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +  # ➏ 为了生成字节序列，我们把 typecode 转换成字节序列，然后……
                bytes(array(self.typecode, self)))  # ➐ ……迭代 Vector2d 实例，得到一个数组，再把数组转换成字节序列。

    def __eq__(self, other):
        return tuple(self) == tuple(other)  # ➑ 为了快速比较所有分量，在操作数中构建元组。

    def __abs__(self):
        return math.hypot(self.x, self.y)  # ➒ 模是 x 和 y 分量构成的直角三角形的斜边长。

    def __bool__(self):
        return bool(abs(self))  # ➓ __bool__ 方法使用 abs(self) 计算模，然后把结果转换成布尔值，因此，0.0 是 False，非零值是 True。

    @classmethod  # ➊ 类方法使用 classmethod 装饰器修饰。
    def frombytes(cls, octets):  # ➋ 不用传入 self 参数；相反，要通过 cls 传入类本身。

        typecode = chr(octets[0])  # ➌ 从第一个字节中读取 typecode。
        memv = memoryview(octets[1:]).cast(typecode)  # ➍ 使用传入的 octets 字节序列创建一个 memoryview，然后使用typecode 转换。
        return cls(*memv)  # ➎ 拆包转换后的 memoryview，得到构造方法所需的一对参数。

    # def __format__(self, fmt_spec=''):
    #     components = (format(c, fmt_spec) for c in self)  # ➊ 使用内置的 format 函数把 fmt_spec 应用到向量的各个分量上，构建一个可迭代的格式化字符串。
    #     return '({}, {})'.format(*components)  # ➋ 把格式化字符串代入公式 '(x, y)' 中。

    # 计算极坐标
    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):  # ➊ 如果格式代码以 'p' 结尾，使用极坐标。
            fmt_spec = fmt_spec[:-1]  # ➋ 从 fmt_spec 中删除 'p' 后缀。
            coords = (abs(self), self.angle())  # ➌ 构建一个元组，表示极坐标：(magnitude, angle)。
            outer_fmt = '<{}, {}>'  # ➍ 把外层格式设为一对尖括号。
        else:
            coords = self  # ➎ 如果不以 'p' 结尾，使用 self 的 x 和 y 分量构建直角坐标。
        outer_fmt = '({}, {})'  # ➏ 把外层格式设为一对圆括号。
        components = (format(c, fmt_spec) for c in coords)  # ➐ 使用各个分量生成可迭代的对象，构成格式化字符串。
            return outer_fmt.format(*components)  # ➑ 把格式化字符串代入外层格式。


v1 = Vector2d(3, 4)
print(v1.x, v1.y)  # ➊ Vector2d 实例的分量可以直接通过属性访问（无需调用读值方法）。
# 3.0 4.0
x, y = v1  # ➋ Vector2d 实例可以拆包成变量元组。
print(x, y)
# (3.0, 4.0)
print(format(v1, '.2f'))
# '(3.00, 4.00)'
print(format(v1, '.3e'))
# '(3.000e+00, 4.000e+00)'
print(v1)  # ➌ repr 函数调用 Vector2d 实例，得到的结果类似于构建实例的源码。
# Vector2d(3.0, 4.0)
v1_clone = eval(repr(v1))  # ➍ 这里使用 eval 函数，表明 repr 函数调用 Vector2d 实例得到的是对构造方法的准确表述。
print(v1 == v1_clone)  # ➎ Vector2d 实例支持使用 == 比较；这样便于测试。
# True
print(v1)  # ➏ print 函数会调用 str 函数，对 Vector2d 来说，输出的是一个有序对。
# (3.0, 4.0)
octets = bytes(v1)  # ➐ bytes 函数会调用 __bytes__ 方法，生成实例的二进制表示形式。
print(octets)
b'd\\x00\\x00\\x00\\x00\\x00\\x00\\x08@\\x00\\x00\\x00\\x00\\x00\\x00\\x10@'
print(abs(v1))  # ➑ abs 函数会调用 __abs__ 方法，返回 Vector2d 实例的模。
# 5.0
print(bool(v1), bool(Vector2d(0, 0)))  # ➒ bool 函数会调用 __bool__ 方法，如果 Vector2d 实例的模为零，返回 False，否则返回 True。
# 计算极坐标：
format(Vector2d(1, 1), 'p')
'<1.4142135623730951, 0.7853981633974483>'
print(format(Vector2d(1, 1), '.3ep'))
'<1.414e+00, 7.854e-01>'
print(format(Vector2d(1, 1), '0.5fp'))
'<1.41421, 0.78540>'
```

##### classmethod与staticmethod

- 定义操作类，而不是操作实例的方法。classmethod 改变了调用方法的方式，因此类方法的第一个参数是类本身，而不是实例。
- classmethod 最常见的用途是定义备选构造方法
- staticmethod 装饰器也会改变方法的调用方式，但是第一个参数不是特殊的值。其实，静态方法就是普通的函数，只是碰巧在类的定义体中，而不是在模块层定义。

```python
class Demo:
    @classmethod
    def klassmeth(*args):
        return args  # ➊ klassmeth 返回全部位置参数。

    @staticmethod
    def statmeth(*args):
        return args  # ➋ statmeth 返回全部位置参数。


print(Demo.klassmeth())  # ➌ 不管怎样调用 Demo.klassmeth，它的第一个参数始终是 Demo 类。
# (<class '__main__.Demo'>,)
print(Demo.klassmeth('spam'))
# (<class '__main__.Demo'>, 'spam')
print(Demo.statmeth())  # ➍ Demo.statmeth 的行为与普通的函数相似。
# ()
print(Demo.statmeth('spam'))
# ('spam',)
```

##### 格式化显示

> 内置的 format() 函数和 str.format() 方法把各个类型的格式化方式委托给相应的 .\__format__(format_spec) 方法。

- format_spec 是**格式说明符**，它是：
  - format(my_obj, format_spec) 的第二个参数，或者
  - str.format() 方法的格式字符串，{} 里代换字段中冒号后面的部分

```python
brl = 1 / 2.43  # BRL到USD的货币兑换比价
print(brl)
# 0.4115226337448559
print(format(brl, '0.4f'))  # ➊ 格式说明符是 '0.4f'。
# '0.4115'
print('1 BRL = {rate:0.2f} USD'.format(rate=brl))  # ➋ 格式说明符是 '0.2f'。代换字段中的 'rate' 子串是字段名称，与格式说明符无关，但是它决定把 .format() 的哪个参数传给代换字段。
'1 BRL = 0.41 USD'
```

- 格式规范微语言

  ```python
  # ，b 和 x分别表示二进制和十六进制的 int 类型，f 表示小数形式的 float 类型，而 % 表示百分数形式：
  print(format(42, 'b'))
  # '101010'
  print(format(2 / 3, '.1%'))
  # '66.7%'

  from datetime import datetime
  now = datetime.now()
  print(format(now, '%H:%M:%S'))
  '18:49:05'
  print("It's now {:%I:%M %p}".format(now))
  "It's now 06:49 PM"
  ```

- 如果类没有定义 \__format__ 方法，从 object 继承的方法会返回str(my_object)。

##### 把 x 和 y 分量设为只读特性

- 我们让这些向量不可变是有原因的，因为这样才能实现\_\_hash\_\_ 方法。这个方法应该返回一个整数，理想情况下还要考虑对象属性的散列值（\_\_eq\_\_ 方法也要使用），因为相等的对象应该具有相同的散列值

```python
class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)  # ➊ 使用两个前导下划线（尾部没有下划线，或者有一个下划线），把属性标记为私有的。
        self.__y = float(y)

    @property  # ➋ @property 装饰器把读值方法标记为特性。
    def x(self):  # ➌ 读值方法与公开属性同名，都是 x。
        return self.__x  # ➍ 直接返回 self.__x。

    @property  # ➎ 以同样的方式处理 y 特性。
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))  # ➏ 需要读取 x 和 y 分量的方法可以保持不变，通过 self.x 和 self.y读取公开特性，而不必读取私有属性，
    
v1 = Vector2d(3, 4)
v2 = Vector2d(3.1, 4.2)
print(hash(v1), hash(v2))
# (7, 384307168202284039)
print(set([v1, v2]))
# {Vector2d(3.1, 4.2), Vector2d(3.0, 4.0)}
```

##### Python的私有属性和“受保护的”属性

- 如果以 __mood 的形式（两个前导下划线，尾部没有或最多有一个下划线）命名实例属性，Python 会把属性名存入实例的\_\_dict\_\_ 属性中，而且会在前面加上一个下划线和类名。这个语言特性叫名称改写

- Python 文档的某些角落把使用一个下划线前缀标记的属性称为“受保护的”属性。 使用 self._x 这种形式保护属性的做法很常见，但是很少有人把这种属性叫作“受保护的”属性。有些人甚至将其称为“私有”属性。

##### 使用 __slots__ 类属性节省空间

- 如果要处理数百万个属性不多的实例，通过 \__slots__类属性，能节省大量内存，方法是让解释器在元组中存储实例属性，而不用字典。
- 定义 \_\_slots\_\_ 的方式是，创建一个类属性，使用 \_\_slots\_\_ 这个名字，并把它的值设为一个字符串构成的可迭代对象，其中各个元素表示各个实例属性。我喜欢使用元组，因为这样定义的 \_\_slots\_\_ 中所含的信息不会变化。

```python
"""
在类中定义 __slots__ 属性的目的是告诉解释器：“这个类中的所有实例属性都在这儿了！”这样，Python 会在各个实例中使用类似元组的结构存储实例变量，从而避免使用消耗内存的 __dict__ 属性。如果有数百万个实例同时活动，这样做能节省大量内存。
"""
class Vector2d:
    __slots__ = ('__x', '__y')
    typecode = 'd'
    # 下面是各个方法（因排版需要而省略了）
```

- 如果使用得当，\__slots__ 能显著节省内存，不过有几点要注意。
  - 每个子类都要定义\ \__slots\_\_ 属性，因为解释器会忽略继承的\_\_slots\_\_ 属性。
  - 实例只能拥有 \_\_slots\_\_ 中列出的属性，除非把 '\__dict__' 加入 \_\_slots\_\_ 中（这样做就失去了节省内存的功效）。
  - 如果不把 '\_\_weakref\_\_' 加入 \__slots__，实例就不能作为弱引用的目标。

- 如果你的程序不用处理数百万个实例，或许不值得费劲去创建不寻常的类，那就禁止它创建动态属性或者不支持弱引用。与其他优化措施一样，仅当权衡当下的需求并仔细搜集资料后证明确实有必要时，才应该使用 \__slots__ 属性。

##### 覆盖类属性

- 设定从类中继承的 typecode 属性，自定义一个实例属性

  ```python
  from vector2d_v3 import Vector2d

  v1 = Vector2d(1.1, 2.2)
  dumpd = bytes(v1)
  print(dumpd)
  # b'd\x9a\x99\x99\x99\x99\x99\xf1?\x9a\x99\x99\x99\x99\x99\x01@'
  len(dumpd)  # ➊ 默认的字节序列长度为 17 个字节。
  # 17
  v1.typecode = 'f'  # ➋ 把 v1 实例的 typecode 属性设为 'f'。
  dumpf = bytes(v1)
  print(dumpf)
  b'f\xcd\xcc\x8c?\xcd\xcc\x0c@'
  len(dumpf)  # ➌ 现在得到的字节序列是 9 个字节长。
  # 9
  print(Vector2d.typecode)  # ➍ Vector2d.typecode 属性的值不变，只有 v1 实例的 typecode 属性使用 'f'。
  'd'
  ```

- 如果想修改类属性的值，必须直接在类上修改，不能通过实例修改。如果想修改所有实例（没有 typecode 实例变量）的 typecode 属性的默认值，可以这么做：

  ```python
  Vector2d.typecode = 'f'
  ```

- ShortVector2d 是 Vector2d 的子类，只用于覆盖typecode 的默认值


##### 特殊方法

- 所有用于获取字符串和字节序列表示形式的方法：\_\_repr\_\_、\_\_str\_\_、\_\_format\_\_ 和 \_\_bytes\_\_。
- 把对象转换成数字的几个方法：\_\_abs\_\_、\_\_bool\_\_和\_\_hash\_\_。
- 用于测试字节序列转换和支持散列（连同 \_\_hash\_\_ 方法）的\_\_eq\_\_ 运算符。

### 序列的修改、散列和切片

  ```python
import functools  # ➊ 为了使用 reduce 函数，导入 functools 模块。
import numbers
import operator  # ➋ 为了使用 xor 函数，导入 operator 模块。
from array import array
import reprlib
import math


class Vector:
    typecode = 'd'
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = array(self.typecode, components)  # ➊ self._components 是“受保护的”实例属性，把 Vector 的分量保存在一个数组中。

    def __len__(self):
        return len(self._components)

    # def __getitem__(self, index):
    #     return self._components[index]
    def __getitem__(self, index):
        cls = type(self)  # ➊ 获取实例所属的类（即 Vector），供后面使用。
        if isinstance(index, slice):  # ➋ 如果 index 参数的值是 slice 对象……
            return cls(self._components[index])  # ➌ ……调用类的构造方法，使用 _components 数组的切片构建一个新Vector 实例。
        elif isinstance(index, numbers.Integral):  # ➍ 如果 index 是 int 或其他整数类型……
            return self._components[index]  # ➎ ……那就返回 _components 中相应的元素。
        else:
            msg = '{cls.__name__} indices must be integers'
        raise TypeError(msg.format(cls=cls))  # ➏ 否则，抛出异常。

    def __iter__(self):
        return iter(self._components)  # ➋ 为了迭代，我们使用 self._components 构建一个迭代器。

    def __repr__(self):
        components = reprlib.repr(
            self._components)  # ➌ 使用 reprlib.repr() 函数获取 self._components 的有限长度表示形式（如 array('d', [0.0, 1.0, 2.0, 3.0, 4.0, ...])）。
        components = components[components.find('['):-1]  # ➍ 把字符串插入 Vector 的构造方法调用之前，去掉前面的array('d' 和后面的 )。
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))  # ➎ 直接使用 self._components 构建 bytes 对象。

    # 这样做对有几千个分量的 Vector 实例来说，效率十分低下:
    # def __eq__(self, other):
    #     return tuple(self) == tuple(other)

    # 减少处理时间和内存用量:
    def __eq__(self, other):
        # if len(self) != len(other):  # ➊ 如果两个对象的长度不一样，那么它们不相等。
        #     return False
        #
        # for a, b in zip(self, other):  # ➋ zip 函数生成一个由元组构成的生成器，元组中的元素来自参数传入的各个可迭代对象。
        #     if a != b:  # ➌ 只要有两个分量不同，返回 False，退出。
        #         return False
        # return True  # ➍ 否则，对象是相等的。
        # 注意，首先要检查两个操作数的长度是否相同，因为 zip 函数会在最短的那个操作数耗尽时停止。
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))  # ➏ 不能使用 hypot 方法了，因此我们先计算各分量的平方之和，然后再使用 sqrt 方法开平方。

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)  # ➐ 我们只需在 Vector2d.frombytes 方法的基础上改动最后一行：直接把 memoryview 传给构造方法，不用像前面那样使用 * 拆包。

    def __getattr__(self, name):
        cls = type(self)  # ➊ 获取 Vector，后面待用。
        if len(name) == 1:  # ➋ 如果属性名只有一个字母，可能是 shortcut_names 中的一个。
            pos = cls.shortcut_names.find(name)  # ➌ 查找那个字母的位置；str.find 还会定位 'yz'，但是我们不需要，因此在前一行做了测试。
            if 0 <= pos < len(self._components):  # ➍ 如果位置落在范围内，返回数组中对应的元素。
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'  # ➎ 如果测试都失败了，抛出 AttributeError，并指明标准的消息文本。
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):
        cls = type(self)

        if len(name) == 1:  # ➊ 特别处理名称是单个字符的属性。
            if name in cls.shortcut_names:  # ➋ 如果 name 是 xyzt 中的一个，设置特殊的错误消息。
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():  # ➌ 如果 name 是小写字母，为所有小写字母设置一个错误消息。
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''  # ➍ 否则，把错误消息设为空字符串。
            if error:  # ➎ 如果有错误消息，抛出 AttributeError。
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)  # ➏ 默认情况：在超类上调用 __setattr__ 方法，提供标准行为。

    def __hash__(self):
        hashes = (hash(x) for x in self._components)  # ➍ 创建一个生成器表达式，惰性计算各个分量的散列值。
        # hashes = map(hash, self._components)  # ➍ 映射归约：把函数应用到各个元素上，生成一个新序列（映射，map），然后计算聚合值（归约，reduce）
        return functools.reduce(operator.xor, hashes, 0)  # ➎ 把 hashes 提供给 reduce 函数，使用 xor 函数计算聚合的散列值；第三个参数，0 是初始值


v1 = Vector(range(7))
print(v1.z)
# 2.0
print(len(v1))
# 7
print(v1[0], v1[-1])  # ➊ 单个整数索引只获取一个分量，值为浮点数。
# 0.0 6.0
v7 = Vector(range(7))
print(v7)
print(v7[1:4])  # ➋ 切片索引创建一个新 Vector 实例。
# (1.0, 2.0, 3.0)
# print(Vector[1, 2]) # Vector 不支持多维索引，因此索引元组或多个切片会抛出错误。
# Traceback (most recent call last):
# ...
# TypeError: Vector indices must be integers
  ```

##### 了解 \__getitem__ 和切片的行为

> S.indices(len) -> (start, stop, stride)
>
> 给定长度为 len 的序列，计算 S 表示的扩展切片的起始（start）和结尾（stop）索引，以及步幅（stride）。超出边界的索引会被截掉，这与常规切片的处理方式一样。
>
> 换句话说，indices 方法开放了内置序列实现的棘手逻辑，用于优雅地处理缺失索引和负数索引，以及长度超过目标序列的切片。这个方法会“整顿”元组，把 start、stop 和 stride 都变成非负数，而且都落在指定长度序列的边界内。
>
> ```python
> slice(None, 10, 2).indices(5)  # ➊ 'ABCDE'[:10:2] 等同于 'ABCDE'[0:5:2]
> (0, 5, 2)
> slice(-3, None, None).indices(5)  # ➋ ➋ 'ABCDE'[-3:] 等同于 'ABCDE'[2:5:1]
> (2, 5, 1)
> ```

```python
class MySeq:

    def __getitem__(self, index):
        return index  # ➊ 在这个示例中，__getitem__ 直接返回传给它的值。


s = MySeq()
print(s[1])  # ➋ 单个索引，没什么新奇的。
# 1
print(s[1:4])  # ➌ 1:4 表示法变成了 slice(1, 4, None)。
# slice(1, 4, None)
print(s[1:4:2])  # ➍ slice(1, 4, 2) 的意思是从 1 开始，到 4 结束，步幅为 2。
# slice(1, 4, 2)
print(s[1:4:2, 9])  # ➎ 神奇的事发生了：如果 [] 中有逗号，那么 __getitem__ 收到的是元组。
# (slice(1, 4, 2), 9)
print(s[1:4:2, 7:9])  # ➏ 元组中甚至可以有多个切片对象。
# (slice(1, 4, 2), slice(7, 9, None))

print(slice)
# <class 'slice'>  # ➊ slice 是内置的类型
print(dir(slice))  # ➋ 通过审查 slice，发现它有 start、stop 和 step 数据属性，以及indices 方法。
# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
# '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__',
# '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'indices', 'start', 'step', 'stop']
print(help(slice.indices))
# S.indices(len) -> (start, stop, stride)
```

### 定义抽象基类的子类

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):  # ➊ 为了支持洗牌，只需实现 __setitem__ 方法。
        self._cards[position] = value

    def __delitem__(self, position):  # ➋ 但是继承 MutableSequence 的类必须实现 __delitem__ 方法，这是 MutableSequence 类的一个抽象方法。
        del self._cards[position]

    def insert(self, position, value):  # ➌ 此外，还要实现 insert 方法，这是 MutableSequence 类的第三个抽象方法。
        self._cards.insert(position, value)
```

##### 定义并使用一个抽象基类

```python
import abc
from random import random


class Tombola(abc.ABC):  # ➊ 自己定义的抽象基类要继承 abc.ABC。
    @abc.abstractmethod
    def load(self, iterable):  # ➋ 抽象方法使用 @abstractmethod 装饰器标记，而且定义体中通常只有文档字符串。
        """从可迭代对象中添加元素。"""

    @abc.abstractmethod
    def pick(self):  # ➌ 根据文档字符串，如果没有元素可选，应该抛出 LookupError。
        """随机删除元素，然后将其返回。
        如果实例为空，这个方法应该抛出`LookupError`。
        """

    def loaded(self):  # ➍ 抽象基类可以包含具体方法。
        """如果至少有一个元素，返回`True`，否则返回`False`。"""
        return bool(self.inspect())  # ➎ 抽象基类中的具体方法只能依赖抽象基类定义的接口（即只能使用抽象基类中的其他具体方法、抽象方法或特性）。

    def inspect(self):
        """返回一个有序元组，由当前元素构成。"""
        items = []
        while True:  # ➏ 我们不知道具体子类如何存储元素，不过为了得到 inspect 的结果，我们可以不断调用 .pick() 方法，把 Tombola 清空……
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # ➐ ……然后再使用 .load(...) 把所有元素放回去。
        return tuple(sorted(items))


class BingoCage(Tombola):  # ➊ 明确指定 BingoCage 类扩展 Tombola 类。
    def __init__(self, items):
        self._randomizer = random.SystemRandom()  # ➋ 假设我们将在线上游戏中使用这个。random.SystemRandom 使用os.urandom(...) 函数实现 random API。
        self._items = []
        self.load(items)  # ➌ 委托 .load(...) 方法实现初始加载。

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)  # ➍ 没有使用 random.shuffle() 函数，而是使用 SystemRandom 实例的 .shuffle() 方法。

    def pick(self):  # ➎ pick 方法的实现方式与示例 5-8 一样。
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):  # ➏ __call__ 也跟示例 5-8 中的一样。它没必要满足 Tombola 接口，添加额外的方法没有问题。
        self.pick()


class LotteryBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable)  # ➊ 初始化方法接受任何可迭代对象：把参数构建成列表。

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            # ➋ 如果范围为空，random.randrange(...) 函数抛出 ValueError，为了兼容 Tombola，我们捕获它，抛出 LookupError。
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LotteryBlower')
        return self._balls.pop(position)  # ➌ 否则，从 self._balls 中取出随机选中的元素。

    def loaded(self):  # ➍ 覆盖 loaded 方法，避免调用 inspect 方法。我们可以直接处理self._balls 而不必构建整个有序元组，从而提升速度。
        return bool(self._balls)

    def inspect(self):  # ➎ 使用一行代码覆盖 inspect 方法。
        return tuple(sorted(self._balls))
```

##### TomboList 是 Tombola 的虚拟子类

```python
import abc
from random import randrange


class Tombola(abc.ABC):  # ➊ 自己定义的抽象基类要继承 abc.ABC。
    @abc.abstractmethod
    def load(self, iterable):  # ➋ 抽象方法使用 @abstractmethod 装饰器标记，而且定义体中通常只有文档字符串。
        """从可迭代对象中添加元素。"""

    @abc.abstractmethod
    def pick(self):  # ➌ 根据文档字符串，如果没有元素可选，应该抛出 LookupError。
        """随机删除元素，然后将其返回。
        如果实例为空，这个方法应该抛出`LookupError`。
        """

    def loaded(self):  # ➍ 抽象基类可以包含具体方法。
        """如果至少有一个元素，返回`True`，否则返回`False`。"""
        return bool(self.inspect())  # ➎ 抽象基类中的具体方法只能依赖抽象基类定义的接口（即只能使用抽象基类中的其他具体方法、抽象方法或特性）。

    def inspect(self):
        """返回一个有序元组，由当前元素构成。"""
        items = []
        while True:  # ➏ 我们不知道具体子类如何存储元素，不过为了得到 inspect 的结果，我们可以不断调用 .pick() 方法，把 Tombola 清空……
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # ➐ ……然后再使用 .load(...) 把所有元素放回去。
        return tuple(sorted(items))


@Tombola.register  # ➊ 把 Tombolist 注册为 Tombola 的虚拟子类。
class TomboList(list):  # ➋ Tombolist 扩展 list。
    def pick(self):
        if self:  # ➌ Tombolist 从 list 中继承 __bool__ 方法，列表不为空时返回True。
            position = randrange(len(self))
            return self.pop(position)  # ➍ pick 调用继承自 list 的 self.pop 方法，传入一个随机的元素索引。
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend  # ➎ Tombolist.load 与 list.extend 一样。

    def loaded(self):
        return bool(self)  # ➏ loaded 方法委托 bool 函数。

    def inspect(self):
        return tuple(sorted(self))
# Tombola.register(TomboList) # ➐ 如果是 Python 3.3 或之前的版本，不能把 .register 当作类装饰器使用，必须使用标准的调用句法。
```

### 继承的优缺点

##### 内置类型 dict 的 \_\_init\_\_ 和 \_\_update\_\_ 方法会忽略我们覆盖的 \_\_setitem\_\_ 方法

```python
class DoppelDict(dict):
    def __setitem__(self, key, value):
        # ➊DoppelDict.__setitem__ 方法会重复存入的值（只是为了提供易于观察的效果）。它把职责委托给超类。
        super().__setitem__(key, [value] * 2)


dd = DoppelDict(one=1)  # ➋ 继承自 dict 的 __init__ 方法显然忽略了我们覆盖的 __setitem__方法：'one' 的值没有重复。
print(dd)
# {'one': 1}
dd['two'] = 2  # ➌ [] 运算符会调用我们覆盖的 __setitem__ 方法，按预期那样工作：'two' 对应的是两个重复的值，即 [2, 2]。
print(dd)
# {'one': 1, 'two': [2, 2]}
dd.update(three=3)  # ➍ 继承自 dict 的 update 方法也不使用我们覆盖的 __setitem__ 方法：'three' 的值没有重复。
print(dd)
# {'three': 3, 'one': 1, 'two': [2, 2]}
```

##### dict.update 方法会忽略 AnswerDict.\__getitem__方法
```python
class AnswerDict(dict):
    def __getitem__(self, key):  # ➊ 不管传入什么键，AnswerDict.__getitem__ 方法始终返回 42。
        return 42


ad = AnswerDict(a='foo')  # ➋ ad = AnswerDict(a='foo')
print(ad['a'])  # ➌ ad['a'] 返回 42，这与预期相符。
# 42
d = {}
d.update(ad)  # ➍ d 是 dict 的实例，使用 ad 中的值更新 d。
print(d['a'])  # ➎ dict.update 方法忽略了 AnswerDict.__getitem__ 方法。
# 'foo'
print(d)
# {'a': 'foo'}
```

##### 不要子类化内置类型，用户自己定义的类应该继承 collections 模块中的类，例如UserDict、UserList 和 UserString，这些类做了特殊设计，因此易于扩展。

```python
import collections


class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


dd = DoppelDict2(one=1)
print(dd)
# {'one': [1, 1]}
dd['two'] = 2
print(dd)
# {'two': [2, 2], 'one': [1, 1]}
dd.update(three=3)
print(dd)
# {'two': [2, 2], 'three': [3, 3], 'one': [1, 1]}


class AnswerDict2(collections.UserDict):
    def __getitem__(self, key):
        return 42


ad = AnswerDict2(a='foo')
print(ad['a'])
# 42
d = {}
d.update(ad)
print(d['a'])
# 42
print(d)
# {'a': 42}
```

##### 多重继承和方法解析顺序

```python
class A:
    def ping(self):
        print('ping:', self)


class B(A):
    def pong(self):
        print('pong:', self)


class C(A):
    def pong(self):
        print('PONG:', self)


class D(B, C):
    def ping(self):
        super().ping()
        print('post-ping:', self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)


d = D()
d.pong()  # ➊ 直接调用 d.pong() 运行的是 B 类中的版本。
# pong: <diamond.D object at 0x10066c278>
C.pong(d)  # ➋ 超类中的方法都可以直接调用，此时要把实例作为显式参数传入。
# PONG: <diamond.D object at 0x10066c278>
print(D.__mro__)
# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
print(d.ping())  # D 类的 ping 方法做了两次调用。
# ping: <__main__.D object at 0x0000027FCC7349B0>  # 第一个调用是 super().ping()；super 函数把 ping 调用委托给 A类；这一行由 A.ping 输出。
# post-ping: <__main__.D object at 0x0000027FCC7349B0>  # 第二个调用是 print('post-ping:', self)，输出的是这一行。
print(d.pingpong())
# ping: <__main__.D object at 0x000002081CF649B0> # 第一个调用是 self.ping()，运行的是 D 类的 ping 方法，输出这一行和下一行。
# post-ping: <__main__.D object at 0x000002081CF649B0>
# ping: <__main__.D object at 0x000002081CF649B0> # 第二个调用是 super().ping()，跳过 D 类的 ping 方法，找到 A 类的 ping 方法。
# pong: <__main__.D object at 0x000002081CF649B0> # 第三个调用是 self.pong()，根据 __mro__ ，找到的是 B 类实现的pong 方法。
# pong: <__main__.D object at 0x000002081CF649B0> # 第四个调用是 super().pong()，也根据 __mro__ ，找到 B 类实现的 pong 方法。
# PONG: <__main__.D object at 0x000002081CF649B0> # 第五个调用是 C.pong(self)，忽略 mro ，找到的是 C 类实现的pong 方法。
```

- 类都有一个名为 \_\_mro\_\_ 的属性，它的值是一个元组，按照方法解析顺序列出各个超类，从当前类一直向上，直到object 类。D 类的 \_\_mro\_\_ 属性如下:

```python
D.__mro__
(<class 'diamond.D'>, <class 'diamond.B'>, <class 'diamond.C'>,<class 'diamond.A'>, <class 'object'>)
```

- 方法解析顺序不仅考虑继承图，还考虑子类声明中列出超类的顺序。也就是说，如果在 diamond.py 文件中把 D 类声明为class D(C, B):，那么 D 类的 \__mro__ 属性就会不一样：先搜索 C类，再搜索 B 类。

##### 查看几个类的 __mro__ 属性

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):  # ➊ 为了支持洗牌，只需实现 __setitem__ 方法。
        self._cards[position] = value

    def __delitem__(self, position):  # ➋ 但是继承 MutableSequence 的类必须实现 __delitem__ 方法，这是 MutableSequence 类的一个抽象方法。
        del self._cards[position]

    def insert(self, position, value):  # ➌ 此外，还要实现 insert 方法，这是 MutableSequence 类的第三个抽象方法。
        self._cards.insert(position, value)


print(bool.__mro__)  # ➊ bool 从 int 和 object 中继承方法和属性。
# (<class 'bool'>, <class 'int'>, <class 'object'>)


def print_mro(cls):  # ➋ print_mro 函数使用更紧凑的方式显示方法解析顺序。
    print(', '.join(c.__name__ for c in cls.__mro__))


print_mro(bool)
# bool, int, object

print_mro(FrenchDeck2)  # ➌ FrenchDeck2 类的祖先包含 collections.abc 模块中的几个抽象基类。
# FrenchDeck2, MutableSequence, Sequence, Reversible, Collection, Sized, Iterable, Container, object
import numbers

print_mro(numbers.Integral)  # ➍ 这些是 numbers 模块提供的几个数字抽象基类。
# Integral, Rational, Real, Complex, Number, object
import io  # ➎ io 模块中有抽象基类（名称以 ...Base 后缀结尾）和具体类，如BytesIO 和 TextIOWrapper。

print_mro(io.BytesIO)
# BytesIO, _BufferedIOBase, _IOBase, object
print_mro(io.TextIOWrapper)
# TextIOWrapper, _TextIOBase, _IOBase, object
```

### 正确重载运算符

- 运算符重载的作用是让用户定义的对象使用中缀运算符（如 + 和 |）或一元运算符（如 - 和 ~）。说得宽泛一些，在 Python 中，函数调用（()）、属性访问（.）和元素访问 / 切片（[]）也是运算符。

- 一元运算符 + 得到一个新 Counter 实例，但是没有零值和负值计数器

  ```python
  from collections import Counter

  ct = Counter('abracadabra')
  print(ct)
  Counter({'a': 5, 'r': 2, 'b': 2, 'd': 1, 'c': 1})
  ct['r'] = -3
  ct['d'] = 0
  print(ct)
  Counter({'a': 5, 'b': 2, 'c': 1, 'd': 0, 'r': -3})
  print(+ct)
  Counter({'a': 5, 'b': 2, 'c': 1})
  ```

- 重载向量加法运算符+

  ```python
  def __add__(self, other):
      # pairs 是个生成器，它会生成 (a, b) 形式的元组，其中 a 来自self，b 来自 other。如果 self 和 other 的长度不同，使用fillvalue 填充较短的那个可迭代对象。
  	pairs = itertools.zip_longest(self, other, fillvalue=0.0) # ➊
      # 构建一个新 Vector 实例，使用生成器表达式计算 pairs 中各个元素的和。
  	return Vector(a + b for a, b in pairs) # ➋
  ```

### 可迭代的对象、迭代器和生成器

##### 名称解释

- 迭代器 iterator

  > 迭代器是这样的对象：实现了无参数的 \__next__ 方法，返回序列中的下一个元素；如果没有元素了，那么抛出 StopIteration 异常。Python 中的迭代器还实现了 \__iter__ 方法，因此迭代器也可以迭代。
  >
  > 实现了无参数的 \_\_next\_\_ 方法，返回序列中的下一个元素；如果没有元素了，那么抛出 StopIteration 异常。Python 中的迭代器还实现了 \_\_iter\_\_ 方法，因此迭代器也可以迭代。

  - 迭代器应该一直可以迭代。迭代器的 \_\_iter\_\_ 方法应该返回自身。
  - 迭代器其实是生成器对象，每次调用\_\_iter\_\_方法都会自动创建，因为\__iter__方法是生成器函数。

- 生成器 

- 生成器表达式

- 生成器函数

  > 只要 Python 函数的定义体中有 yield 关键字，该函数就是生成器函数。调用生成器函数时，会返回一个生成器对象。也就是说，生成器函数是生成器工厂。

  > 生成器函数会创建一个生成器对象，包装生成器函数的定义体。把生成器传给 next(...) 函数时，生成器函数会向前，执行函数定义体中的下一个 yield 语句，返回产出的值，并在函数定义体的当前位置暂停。最终，函数的定义体返回时，外层的生成器对象会抛出StopIteration 异常——这一点与迭代器协议一致。

- 迭代器对象

- 生成器对象

- 可迭代对象 iterable

  - 使用 iter 内置函数可以获取迭代器的对象。
  - 如果对象实现了能返回迭代器的 \__iter__ 方法，那么对象就是可迭代的。
  - 序列都可以迭代；
  - 实现了 \__getitem__ 方法，而且其参数是从零开始的索引，这种对象也可以迭代。
  - 可迭代的对象和迭代器之间的关系：Python 从可迭代的对象中获取迭代器。
  - 可迭代的对象一定不能是自身的迭代器。也就是说，可迭代的对象必须实现 \_\_iter\_\_ 方法，但不能实现 \_\_next\_\_ 方法。


##### 在 Python 语言内部，迭代器用于支持：

- for 循环
- 构建和扩展集合类型
- 逐行遍历文本文件
- 列表推导、字典推导和集合推导
- 元组拆包
- 调用函数时，使用 * 拆包实参

##### Sentence类第1版：单词序列

```python
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)  # ➊ re.findall 函数返回一个字符串列表，里面的元素是正则表达式的全部非重叠匹配。

    def __getitem__(self, index):
        return self.words[index]  # ➋ self.words 中保存的是 .findall 函数返回的结果，因此直接返回指定索引位上的单词。

    def __len__(self):  # ➌ 为了完善序列协议，我们实现了 __len__ 方法；不过，为了让对象可以迭代，没必要实现这个方法。
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # ➍ reprlib.repr 这个实用函数用于生成大型数据结构的简略字符串表示形式。


s = Sentence('"The time has come," the Walrus said,')  # ➊ 传入一个字符串，创建一个 Sentence 实例。
print(s)
Sentence('"The time ha... Walrus said,')  # ➋ 注意，__repr__ 方法的输出中包含 reprlib.repr 方法生成的...。
for word in s:  # ➌ Sentence 实例可以迭代，稍后说明原因。
    print(word)
# The
# time
# has
# come
# the
# Walrus
# said
print(list(s))  # ➍ 因为可以迭代，所以 Sentence 对象可以用于构建列表和其他可迭代的类型。
# ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']
# Sentence 类是序列，可以按索引获取单词：
print(s[0])
```

##### 序列可以迭代的原因：iter函数

> 解释器需要迭代对象 x 时，会自动调用 iter(x)。

- 内置的 iter 函数有以下作用：
  - 检查对象是否实现了 \__iter__ 方法，如果实现了就调用它，获取一个迭代器。
  - 如果没有实现 \_\_iter\_\_ 方法，但是实现了 \_\_getitem\_\_ 方法，Python 会创建一个迭代器，尝试按顺序（从索引 0 开始）获取元素。
  - 如果尝试失败，Python 抛出 TypeError 异常，通常会提示“C objectis not iterable”（C 对象不可迭代），其中 C 是目标对象所属的类。

- 任何 Python 序列都可迭代的原因是，它们都实现了 \_\_getitem\_\_ 方法。其实，标准的序列也都实现了 \_\_iter\_\_ 方法

##### 可迭代的对象和迭代器之间的关系：Python 从可迭代的对象中获取迭代器。

- 一个简单的 for 循环，迭代一个字符串。这里，字符串 'ABC'是可迭代的对象。背后是有迭代器的，只不过我们看不到：

  ```python
  s = 'ABC'
  for char in s:
      print(char)
  # ABC
  ```

- 如果没有 for 语句，不得不使用 while 循环模拟：

  ```python
  s = 'ABC'
  it = iter(s)  # ➊ 使用可迭代的对象构建迭代器 it。
  while True:
      try:
          print(next(it))  # ➋ 不断在迭代器上调用 next 函数，获取下一个字符。
      except StopIteration:  # ➌ 如果没有字符了，迭代器会抛出 StopIteration 异常。
          del it  # ➍ 释放对 it 的引用，即废弃迭代器对象。
          break  # ➎ 退出循环。

  # A
  # B
  # C
  ```

- 标准的迭代器接口有两个方法。
  - \__next__ 返回下一个可用的元素，如果没有元素了，抛出 StopIteration异常。
  - \__iter__ 返回 self，以便在应该使用可迭代对象的地方使用迭代器，例如在 for 循环中。

- abc.Iterator 类

  ```python
  from abc import abstractmethod
  from collections import Iterable
  class Iterator(Iterable):
    __slots__ = ()    
    @abstractmethod
    def __next__(self):
        'Return the next item from the iterator. When exhausted, raise StopIteration'
        raise StopIteration
  
    def __iter__(self):
        return self
  
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Iterator:
            if (any("__next__" in B.__dict__ for B in C.__mro__) and
                    any("__iter__" in B.__dict__ for B in C.__mro__)):
                return True
        return NotImplemented
  ```


- 如何使用 iter(...) 函数构建迭代器，以及如何使用 next(...) 函数使用迭代器：

  > 因为迭代器只需 \_\_next\_\_ 和 \_\_iter\_\_ 两个方法，所以除了调用next() 方法，以及捕获 StopIteration 异常之外，没有办法检查是否还有遗留的元素。此外，也没有办法“还原”迭代器。如果想再次迭代，那就要调用 iter(...)，传入之前构建迭代器的可迭代对象。传入迭代器本身没用，因为前面说过 Iterator.\_\_iter\_\_ 方法的实现方式是返回实例本身，所以传入迭代器无法还原已经耗尽的迭代器。

  ```python
  import re
  import reprlib
  
  RE_WORD = re.compile('\w+')
  
  
  class Sentence:
      def __init__(self, text):
          self.text = text
          self.words = RE_WORD.findall(text)  # ➊ re.findall 函数返回一个字符串列表，里面的元素是正则表达式的全部非重叠匹配。
  
      def __getitem__(self, index):
          return self.words[index]  # ➋ self.words 中保存的是 .findall 函数返回的结果，因此直接返回指定索引位上的单词。
  
      def __len__(self):  # ➌ 为了完善序列协议，我们实现了 __len__ 方法；不过，为了让对象可以迭代，没必要实现这个方法。
          return len(self.words)
  
      def __repr__(self):
          return 'Sentence(%s)' % reprlib.repr(self.text)  # ➍ reprlib.repr 这个实用函数用于生成大型数据结构的简略字符串表示形式。
  
  s3 = Sentence('Pig and Pepper')  # ➊
  it = iter(s3)  # ➋
  print(it)  # doctest: +ELLIPSIS
  # <iterator object at 0x...>
  print(next(it))  # ➌
  'Pig'
  print(next(it))
  'and'
  print(next(it))
  'Pepper'
  # print(next(it))  # ➍
  # Traceback (most recent call last):
  # ...
  # StopIteration
  print(list(it))  # ➎
  # []
  print(list(iter(s3)))  # ➏
  # ['Pig', 'and', 'Pepper']
  ```

##### Sentence类第2版：典型的迭代器

```python
import abc
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):  # ➊ 与前一版相比，这里只多了一个 __iter__ 方法。这一版没有__getitem__ 方法，为的是明确表明这个类可以迭代，因为实现了__iter__ 方法。
        return SentenceIterator(self.words)  # ➋ 根据可迭代协议，__iter__ 方法实例化并返回一个迭代器。


class SentenceIterator:
    def __init__(self, words):
        self.words = words  # ➌ SentenceIterator 实例引用单词列表。
        self.index = 0  # ➍ self.index 用于确定下一个要获取的单词。

    def __next__(self):
        try:
            word = self.words[self.index]  # ➎ 获取 self.index 索引位上的单词。
        except IndexError:
            raise StopIteration()  # ➏ 如果 self.index 索引位上没有单词，那么抛出 StopIteration 异常。
        self.index += 1  # ➐ 递增 self.index 的值。
        return word  # ➑ 返回单词。

    def __iter__(self):  # ➒ 实现 self.__iter__ 方法。
        return self
```

##### Sentence类第3版：生成器函数

- \__iter__ 方法是生成器函数，调用时会构建一个实现了迭代器接口的生成器对象，因此不用再定义 SentenceIterator 类了。

```python
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:  # ➊ 迭代 self.words。
            yield word  # ➋ 产出当前的 word。
        return  # ➌ 这个 return 语句不是必要的；这个函数可以直接“落空”，自动返回。不管有没有 return 语句，生成器函数都不会抛出 StopIteration异常，而是在生成完全部值之后会直接退出。
# 完成！ ➍ 不用再单独定义一个迭代器类！
```

##### 生成器函数定义体的执行过程

```python
def gen_AB():  # ➊ 定义生成器函数的方式与普通的函数无异，只不过要使用 yield 关键字。
    print('start')
    yield 'A'  # ➋ 在 for 循环中第一次隐式调用 next() 函数时（序号➎），会打印'start'，然后停在第一个 yield 语句，生成值 'A'。
    print('continue')
    yield 'B'  # ➌ 在 for 循环中第二次隐式调用 next() 函数时，会打印'continue'，然后停在第二个 yield 语句，生成值 'B'。
    print('end.')  # ➍ 第三次调用 next() 函数时，会打印 'end.'，然后到达函数定义体的末尾，导致生成器对象抛出 StopIteration 异常。


a = 1
for c in gen_AB():  # ➎ 迭代时，for 机制的作用与 g = iter(gen_AB()) 一样，用于获取生成器对象，然后每次迭代时调用 next(g)。
    print('-->', c)  # ➏ 循环块打印 --> 和 next(g) 返回的值。但是，生成器函数中的 print 函数输出结果之后才会看到这个输出。

# start 'start' 是生成器函数定义体中 print('start') 输出的结果。
# --> A 生成器函数定义体中的 yield 'A' 语句会生成值 A，提供给 for 循环使用，而 A 会赋值给变量 c，最终输出 --> A。
# continue 第二次调用 next(g)，继续迭代，生成器函数定义体中的代码由yield 'A' 前进到 yield 'B'。文本 continue 是由生成器函数定义体中的第二个 print 函数输出的。
# --> B yield 'B' 语句生成值 B，提供给 for 循环使用，而 B 会赋值给变量 c，所以循环打印出 --> B。
# end. 第三次调用 next(it)，继续迭代，前进到生成器函数的末尾。文本end. 是由生成器函数定义体中的第三个 print 函数输出的。到达生成器函数定义体的末尾时，生成器对象抛出 StopIteration 异常。for机制会捕获异常，因此循环终止时没有报错。
```

##### Sentence类第4版：惰性实现

```python
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text  # ➊ 不再需要 words 列表。

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):  # ➋ finditer 函数构建一个迭代器，包含 self.text 中匹配 RE_WORD的单词，产出 MatchObject 实例。
            yield match.group()  # ➌ match.group() 方法从 MatchObject 实例中提取匹配正则表达式的具体文本。
```

##### Sentence类第5版：生成器表达式

> 生成器表达式可以理解为列表推导的惰性版本：不会迫切地构建列表，而是返回一个生成器，按需惰性生成元素。也就是说，如果列表推导是制造列表的工厂，那么生成器表达式就是制造生成器的工厂。

```python
def gen_AB():  # ➊
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')


res1 = [x * 3 for x in gen_AB()]  # ➋ 列表推导迫切地迭代 gen_AB() 函数生成的生成器对象产出的元素：'A' 和 'B'。注意，下面的输出是 start、continue 和 end.。
# start
# continue
# end.
for i in res1:  # ➌ 这个 for 循环迭代列表推导生成的 res1 列表。
    print('-->', i)
# --> AAA
# --> BBB
res2 = (x * 3 for x in gen_AB())  # ➍ 把生成器表达式返回的值赋值给 res2。只需调用 gen_AB() 函数，虽然调用时会返回一个生成器，但是这里并不使用。
print(res2)  # ➎ res2 是一个生成器对象。
# <generator object <genexpr> at 0x10063c240>
for i in res2:  # ➏ 只有 for 循环迭代 res2 时，gen_AB 函数的定义体才会真正执行。for 循环每次迭代时会隐式调用 next(res2)，前进到 gen_AB 函数中的下一个 yield 语句。注意，gen_AB 函数的输出与 for 循环中print 函数的输出夹杂在一起。
    print('-->', i)
# start
# --> AAA
# continue
# --> BBB
# end.
```

```python
import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        # __iter__ 方法，这里不是生成器函数了（没有 yield），而是使用生成器表达式构建生成器，然后将其返回。不过，最终的效果一样：调用 __iter__ 方法会得到一个生成器对象。
        return (match.group() for match in RE_WORD.finditer(self.text))
```

##### 等差数列生成器

- 内置的 range 函数用于生成有穷整数等差数列
- itertools.count 函数用于生成无穷等差数列

- ArithmeticProgression 类

  > 说明了如何使用生成器函数实现特殊的 \_\_iter\_\_方法。然而，如果一个类只是为了构建生成器而去实现 \_\_iter\_\_ 方法，那还不如使用生成器函数。毕竟，生成器函数是制造生成器的工厂。

  ```python
  class ArithmeticProgression:
      def __init__(self, begin, step, end=None):  # ➊ __init__ 方法需要两个参数：begin 和 step。end 是可选的，如果值是 None，那么生成的是无穷数列。
          self.begin = begin
          self.step = step
          self.end = end  # None -> 无穷数列

      def __iter__(self):
          result = type(self.begin + self.step)(self.begin)  # ➋ 这一行把 self.begin 赋值给 result，不过会先强制转换成前面的加法算式得到的类型。
          forever = self.end is None  # ➌ 为了提高可读性，我们创建了 forever 变量，如果 self.end 属性的值是 None，那么 forever 的值是 True，因此生成的是无穷数列。
          index = 0
          while forever or result < self.end:  # ➍ 这个循环要么一直执行下去，要么当 result 大于或等于 self.end时结束。如果循环退出了，那么这个函数也随之退出。
              yield result  # ➎ 生成当前的 result 值。
              index += 1
              result = self.begin + self.step * index  # ➏ 计算可能存在的下一个结果。这个值可能永远不会产出，因为while 循环可能会终止。
  ```

- aritprog_gen 生成器函数

  ```python
  def aritprog_gen(begin, step, end=None):
      result = type(begin + step)(begin)
      forever = end is None
      index = 0
      while forever or result < end:
          yield result
          index += 1
          result = begin + step * index
  ```

##### 使用itertools模块生成等差数列

> itertools.count 函数返回的生成器能生成多个数。如果不传入参数，itertools.count 函数会生成从零开始的整数数列。不过，我们可以提供可选的 start 和 step 值，这样实现的作用与aritprog_gen 函数十分相似。

1. tertools.count 函数

```python
import itertools
gen = itertools.count(1, .5)
print(next(gen))
# 1
next(gen)
# 1.5
next(gen)
# 2.0
next(gen)
# 2.5
```

2. itertools.takewhile 函数

> 它会生成一个使用另一个生成器的生成器，在指定的条件计算结果为 False 时停止。

```python
import itertools

gen = itertools.takewhile(lambda n: n < 3, itertools.count(1, .5))
list(gen)
# [1, 1.5, 2.0, 2.5]
```

- aritprog_gen 不是生成器函数，因为定义体中没有 yield 关键字。但是它会返回一个生成器，因此它与其他生成器函数一样，也是生成器工厂函数。

> 示例想表达的观点是，实现生成器时要知道标准库中有什么可用，否则很可能会重新发明轮子。

```python
import itertools


def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen
```

### 标准库中的生成器函数

##### 用于过滤的生成器函数

> 从输入的可迭代对象中产出元素的子集，而且不修改元素本身。

> 下列大多数函数都接受一个断言参数（predicate）。这个参数是个布尔函数，有一个参数，会应用到输入中的每个元素上，用于判断元素是否包含在输出中。

1. itertools  compress(it, selector_it) 

   > 并行处理两个可迭代的对象；如果 selector_it中的元素是真值，产出 it 中对应的元素

2. itertools  dropwhile(predicate,it)

   > 处理 it，跳过 predicate 的计算结果为真值的元素，然后产出剩下的各个元素（不再进一步检查）

3. 内置  filter(predicate, it)

   > 把 it 中的各个元素传给 predicate，如果predicate(item) 返回真值，那么产出对应的元素；如果 predicate 是 None，那么只产出真值元素

4. itertools  filterfalse(predicate,it)

   > 与 filter 函数的作用类似，不过 predicate 的逻辑是相反的：predicate 返回假值时产出对应的元素

5. itertools  islice(it, stop) 或islice(it, start,stop, step=1)

   >产出 it 的切片，作用类似于 s[:stop] 或s[start:stop:step]，不过 it 可以是任何可迭代的对象，而且这个函数实现的是惰性操作

6. itertools  takewhile(predicate,it)

   > predicate 返回真值时产出对应的元素，然后立即停止，不再继续检查

```py
>>> def vowel(c):
... return c.lower() in 'aeiou'
...
>>> list(filter(vowel, 'Aardvark'))
['A', 'a', 'a']
>>> import itertools
>>> list(itertools.filterfalse(vowel, 'Aardvark'))
['r', 'd', 'v', 'r', 'k']
>>> list(itertools.dropwhile(vowel, 'Aardvark'))
['r', 'd', 'v', 'a', 'r', 'k']
>>> list(itertools.takewhile(vowel, 'Aardvark'))
['A', 'a']
>>> list(itertools.compress('Aardvark', (1,0,1,1,0,1)))
['A', 'r', 'd', 'a']
>>> list(itertools.islice('Aardvark', 4))
['A', 'a', 'r', 'd']
>>> list(itertools.islice('Aardvark', 4, 7))
['v', 'a', 'r']
>>> list(itertools.islice('Aardvark', 1, 7, 2))
['a', 'd', 'a']
```

##### 用于映射的生成器函数

> 在输入的单个可迭代对象（map 和starmap 函数处理多个可迭代的对象）中的各个元素上做计算，然后返回结果。

1. itertools  accumulate(it,[func])

   > 产出累积的总和；如果提供了 func，那么把前两个元素传给它，然后把计算结果和下一个元素传给它，以此类推，最后产出结果

2. （内置）enumerate(iterable,start=0)

   > 产出由两个元素组成的元组，结构是 (index,item)，其中 index 从 start 开始计数，item 则从iterable 中获取

3. （内置）map(func, it1,[it2, ..., itN])

   > 把 it 中的各个元素传给func，产出结果；如果传入N 个可迭代的对象，那么 func 必须能接受 N 个参数，而且要并行处理各个可迭代的对象

4. itertools  starmap(func, it)

   > 把 it 中的各个元素传给 func，产出结果；输入的可迭代对象应该产出可迭代的元素 iit，然后以func(*iit) 这种形式调用 func

- 演示 itertools.accumulate 生成器函数

  ```python
  sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
  import itertools

  list(itertools.accumulate(sample))  # ➊ 计算总和。
  # [5, 9, 11, 19, 26, 32, 35, 35, 44, 45]
  list(itertools.accumulate(sample, min))  # ➋ 计算最小值。
  # [5, 4, 2, 2, 2, 2, 2, 0, 0, 0]
  list(itertools.accumulate(sample, max))  # ➌ 计算最大值。
  # [5, 5, 5, 8, 8, 8, 8, 8, 9, 9]
  import operator

  list(itertools.accumulate(sample, operator.mul))  # ➍ 计算乘积。
  # [5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]
  list(itertools.accumulate(range(1, 11), operator.mul))
  # [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800] # ➎ 从 1! 到 10!，计算各个数的阶乘。
  ```

- 剩余函数的演示

  ```python
  list(enumerate('albatroz', 1))  # ➊ 从 1 开始，为单词中的字母编号。
  # [(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]
  import operator
  
  print(list(map(operator.mul, range(11), range(11))))  # ➋ 从 0 到 10，计算各个整数的平方。
  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
  print(list(map(operator.mul, range(11), [2, 4, 8])))  # ➌ 计算两个可迭代对象中对应位置上的两个元素之积，元素最少的那个可迭代对象到头后就停止。
  # [0, 4, 16]
  print(list(map(lambda a, b: (a, b), range(11), [2, 4, 8])))  # ➍ 作用等同于内置的 zip 函数。
  # [(0, 2), (1, 4), (2, 8)]
  import itertools
  
  print(list(itertools.starmap(operator.mul, enumerate('albatroz', 1))))  # ➎ 从 1 开始，根据字母所在的位置，把字母重复相应的次数。
  # ['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']
  sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
  print(list(itertools.starmap(lambda a, b: b / a, enumerate(itertools.accumulate(sample), 1))))  # ➏ 计算平均值。
  # [5.0, 4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333, 5.0, 4.375, 4.888888888888889, 4.5]
  ```

##### 用于合并的生成器函数

> 这些函数都从输入的多个可迭代对象中产出元素。chain 和 chain.from_iterable 按顺序（一个接一个）处理输入的可迭代对象，而 product、zip 和 zip_longest 并行处理输入的各个可迭代对象。

1. itertools  chain(it1, ..., itN)

   > 先产出 it1 中的所有元素，然后产出 it2 中的所有元素，以此类推，无缝连接在一起

2. itertools  chain.from_iterable(it)

   > 产出 it 生成的各个可迭代对象中的元素，一个接一个，无缝连接在一起；it 应该产出可迭代的元素，例如可迭代的对象列表

3. itertools  product(it1, ..., itN,repeat=1)

   > 计算笛卡儿积：从输入的各个可迭代对象中获取元素，合并成由 N 个元素组成的元组，与嵌套的 for 循环效果一样；repeat 指明重复处理多少次输入的可迭代对象

4. （内置）zip(it1, ..., itN)

   > 并行从输入的各个可迭代对象中获取元素，产出由 N 个元素组成的元组，只要有一个可迭代的对象到头了，就默默地停止

5. itertools  zip_longest(it1, ...,itN, fillvalue=None)

   > 并行从输入的各个可迭代对象中获取元素，产出由 N 个元素组成的元组，等到最长的可迭代对象到头后才停止，空缺的值使用 fillvalue填充

- 展示 itertools.chain 和 zip 生成器函数及其同胞的用法

  ```python
  import itertools

  print(list(itertools.chain('ABC', range(2))))  # ➊ 调用 chain 函数时通常传入两个或更多个可迭代对象。
  # ['A', 'B', 'C', 0, 1]
  print(list(itertools.chain(enumerate('ABC'))))  # ➋ 如果只传入一个可迭代的对象，那么 chain 函数没什么用。
  # [(0, 'A'), (1, 'B'), (2, 'C')]
  print(list(itertools.chain.from_iterable(enumerate('ABC'))))  # ➌ 但是 chain.from_iterable 函数从可迭代的对象中获取每个元素，然后按顺序把元素连接起来，前提是各个元素本身也是可迭代的对象。
  # [0, 'A', 1, 'B', 2, 'C']
  print(list(zip('ABC', range(5))))  # ➍ zip 常用于把两个可迭代的对象合并成一系列由两个元素组成的元组。
  # [('A', 0), ('B', 1), ('C', 2)]
  print(list(zip('ABC', range(5), [10, 20, 30, 40])))  # ➎ zip 可以并行处理任意数量个可迭代的对象，不过只要有一个可迭代的对象到头了，生成器就停止。
  # [('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]
  print(list(itertools.zip_longest('ABC', range(5))))  # ➏ itertools.zip_longest 函数的作用与 zip 类似，不过输入的所有可迭代对象都会处理到头，如果需要会填充 None。
  # [('A', 0), ('B', 1), ('C', 2), (None, 3), (None, 4)]
  print(list(itertools.zip_longest('ABC', range(5), fillvalue='?')))  # ➐ fillvalue 关键字参数用于指定填充的值。
  # [('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)]
  ```

- 演示 itertools.product 生成器函数

  ```python
  import itertools
  
  print(list(itertools.product('ABC', range(2))))  # ➊ 三个字符的字符串与两个整数的值域得到的笛卡儿积是六个元组（因为 3 * 2 等于 6）。
  # [('A', 0), ('A', 1), ('B', 0), ('B', 1), ('C', 0), ('C', 1)]
  suits = 'spades hearts diamonds clubs'.split()
  print(list(itertools.product('AK', suits)))  # ➋ 两张牌（'AK'）与四种花色得到的笛卡儿积是八个元组。
  # [('A', 'spades'), ('A', 'hearts'), ('A', 'diamonds'), ('A', 'clubs'), ('K', 'spades'), ('K', 'hearts'), ('K', 'diamonds'), ('K', 'clubs')]
  print(list(itertools.product('ABC')))  # ➌ 如果传入一个可迭代的对象，product 函数产出的是一系列只有一个元素的元组，不是特别有用。
  # [('A',), ('B',), ('C',)]
  print(list(itertools.product('ABC', repeat=2)))  # ➍ repeat=N 关键字参数告诉 product 函数重复 N 次处理输入的各个可迭代对象。
  # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]
  print(list(itertools.product(range(2), repeat=3)))
  # [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
  rows = itertools.product('AB', range(2), repeat=2)
  for row in rows:
      print(row)
  # ('A', 0, 'A', 0)
  # ('A', 0, 'A', 1)
  # ('A', 0, 'B', 0)
  # ('A', 0, 'B', 1)
  # ('A', 1, 'A', 0)
  # ('A', 1, 'A', 1)
  # ('A', 1, 'B', 0)
  # ('A', 1, 'B', 1)
  # ('B', 0, 'A', 0)
  # ('B', 0, 'A', 1)
  # ('B', 0, 'B', 0)
  # ('B', 0, 'B', 1)
  # ('B', 1, 'A', 0)
  # ('B', 1, 'A', 1)
  # ('B', 1, 'B', 0)
  # ('B', 1, 'B', 1)
  ```

##### 把输入的各个元素扩展成多个输出元素的生成器函数，itertools模块：

1. combinations(it, out_len)

   > 把 it 产出的 out_len 个元素组合在一起，然后产出

2. combinations_with_replacement(it,out_len)

   > 把 it 产出的 out_len 个元素组合在一起，然后产出，包含相同元素的组合

3. count(start=0, step=1)

   > 从 start 开始不断产出数字，按step 指定的步幅增加

4. cycle(it)

   > 从 it 中产出各个元素，存储各个元素的副本，然后按顺序重复不断地产出各个元素

5. permutations(it, out_len=None)

   > 把 out_len 个 it 产出的元素排列在一起，然后产出这些排列；out_len的默认值等于 len(list(it))

6. repeat(item, [times])

   > 重复不断地产出指定的元素，除非提供 times，指定次数

- 演示 count、repeat 和 cycle 的用法

  ```python
  import itertools
  import operator

  ct = itertools.count()  # ➊ 使用 count 函数构建 ct 生成器。
  print(next(ct))  # ➋ 获取 ct 中的第一个元素。
  # 0
  print(next(ct), next(ct), next(ct))  # ➌ 不能使用 ct 构建列表，因为 ct 是无穷的，所以我获取接下来的 3个元素。
  # (1, 2, 3)
  print(list(itertools.islice(itertools.count(1, .3), 3)))  # ➍ 如果使用 islice 或 takewhile 函数做了限制，可以从 count 生成器中构建列表。
  # [1, 1.3, 1.6]
  cy = itertools.cycle('ABC')  # ➎ 使用 'ABC' 构建一个 cycle 生成器，然后获取第一个元素——'A'。
  print(next(cy))
  # 'A'
  print(list(itertools.islice(cy, 7)))  # ➏ 只有受到 islice 函数的限制，才能构建列表；这里获取接下来的 7个元素。
  # ['B', 'C', 'A', 'B', 'C', 'A', 'B']
  rp = itertools.repeat(7)  # ➐ 构建一个 repeat 生成器，始终产出数字 7。
  print(next(rp), next(rp))
  # (7, 7)
  print(list(itertools.repeat(8, 4)))  # ➑ 传入 times 参数可以限制 repeat 生成器生成的元素数量：这里会生成 4 次数字 8。
  # [8, 8, 8, 8]
  print(list(map(operator.mul, range(11), itertools.repeat(5))))  # ➒ repeat 函数的常见用途：为 map 函数提供固定参数，这里提供的是乘数 5。
  # [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
  ```

- 组合学生成器函数combinations、comb、permutations、product

  > 组合学生成器函数会从输入的各个元素中产出多个值

  ```python
  import itertools
  
  list(itertools.combinations('ABC', 2))  # ➊ 'ABC' 中每两个元素（len()==2）的各种组合；在生成的元组中，元素的顺序无关紧要（可以视作集合）。
  # [('A', 'B'), ('A', 'C'), ('B', 'C')]
  list(itertools.combinations_with_replacement('ABC', 2))  # ➋ 'ABC' 中每两个元素（len()==2）的各种组合，包括相同元素的组合。
  # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
  list(itertools.permutations('ABC', 2))  # ➌ 'ABC' 中每两个元素（len()==2）的各种排列；在生成的元组中，元素的顺序有重要意义。
  # [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
  list(itertools.product('ABC', repeat=2))  # ➍ 'ABC' 和 'ABC'（repeat=2 的效果）的笛卡儿积。
  # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]
  ```

##### 用于重新排列元素的生成器函数

1. itertools  groupby(it,key=None)

   > 产出由两个元素组成的元素，形式为 (key,group)，其中 key 是分组标准，group 是生成器，用于产出分组里的元素

2. （内置）reversed(seq)

   > 从后向前，倒序产出 seq 中的元素；seq 必须是序列，或者是实现了 \__reversed__ 特殊方法的对象

3. itertools  tee(it, n=2)

   > 产出一个由 n 个生成器组成的元组，每个生成器用于单独产出输入的可迭代对象中的元素

- itertools.groupby 函数的用法

  ```python
  import itertools

  list(itertools.groupby('LLLLAAGGG'))  # ➊ groupby 函数产出 (key, group_generator) 这种形式的元组。
  # [('L', <itertools._grouper object at 0x102227cc0>),('A', <itertools._grouper object at 0x102227b38>),('G', <itertools._grouper object at 0x102227b70>)]
  for char, group in itertools.groupby('LLLLAAAGG'):  # ➋ 处理 groupby 函数返回的生成器要嵌套迭代：这里在外层使用 for循环，内层使用列表推导。
      print(char, '->', list(group))
  ...
  # L -> ['L', 'L', 'L', 'L']
  # A -> ['A', 'A',]
  # G -> ['G', 'G', 'G']
  animals = ['duck', 'eagle', 'rat', 'giraffe', 'bear', 'bat', 'dolphin', 'shark', 'lion']
  animals.sort(key=len)  # ➌ 为了使用 groupby 函数，要排序输入；这里按照单词的长度排序。
  print(animals)
  # ['rat', 'bat', 'duck', 'bear', 'lion', 'eagle', 'shark', 'giraffe', 'dolphin']
  for length, group in itertools.groupby(animals, len):  # ➍ 再次遍历 key 和 group 值对，把 key 显示出来，并把 group 扩展成列表。
      print(length, '->', list(group))
  ...
  # 3 -> ['rat', 'bat']
  # 4 -> ['duck', 'bear', 'lion']
  # 5 -> ['eagle', 'shark']
  # 7 -> ['giraffe', 'dolphin']
  for length, group in itertools.groupby(reversed(animals), len):  # ➎ 这里使用 reverse 生成器从右向左迭代 animals。
      print(length, '->', list(group))
  ...
  # 7 -> ['dolphin', 'giraffe']
  # 5 -> ['shark', 'eagle']
  # 4 -> ['lion', 'bear', 'duck']
  # 3 -> ['bat', 'rat']
  # >>>
  ```

- iterator.tee生成器函数

  > 从输入的一个可迭代对象中产出多个生成器，每个生成器都可以产出输入的各个元素。产出的生成器可以单独使用。

  ```python
  import itertools
  print(list(itertools.tee('ABC')))
  # [<itertools._tee object at 0x10222abc8>, <itertools._tee object at 0x10222ac08>]
  g1, g2 = itertools.tee('ABC')
  print(next(g1))
  'A'
  print(next(g2))
  'A'
  print(next(g2))
  'B'
  print(list(g1))
  # ['B', 'C']
  print(next(g2))
  # ['C']
  print(list(zip(*itertools.tee('ABC'))))
  # [('A', 'A'), ('B', 'B'), ('C', 'C')]
  ```

##### 可迭代的归约函数

- 读取迭代器，返回单个值的内置函数

1. all(it)

   > it 中的所有元素都为真值时返回 True，否则返回 False；all([]) 返回 True

2. any(it)

   > 只要 it 中有元素为真值就返回 True，否则返回 False；any([]) 返回 False

3. max(it, \[key=,][default=])

   > 返回 it 中值最大的元素；*key 是排序函数，与 sorted 函数中的一样；如果可迭代的对象为空，返回 default

4. min(it, \[key=,][default=])

   > 返回 it 中值最小的元素；#key 是排序函数，与 sorted 函数中的一样；如果可迭代的对象为空，返回 default

5. reduce(func, it, [initial])

   > 把前两个元素传给 func，然后把计算结果和第三个元素传给 func，以此类推，返回最后的结果；如果提供了initial，把它当作第一个元素传入

6. sum(it, start=0)

   > it 中所有元素的总和，如果提供可选的 start，会把它加上（计算浮点数的加法时，可以使用 math.fsum 函数提高精度）

##### 深入分析iter函数

> iter 函数还有一个鲜为人知的用法：传入两个参数，使用常规的函数或任何可调用的对象创建迭代器。这样使用时，第一个参数必须是可调用的对象，用于不断调用（没有参数），产出各个值；第二个值是哨符，这是个标记值，当可调用的对象返回这个值时，触发迭代器抛出 StopIteration 异常，而不产出哨符。

- 使用 iter 函数掷骰子，直到掷出 1 点为止：

```python
from random import randint


def d6():
    return randint(1, 6)


d6_iter = iter(d6, 1)
print(d6_iter)
# <callable_iterator object at 0x00000000029BE6A0>
for roll in d6_iter:
    print(roll)
```

- 逐行读取文件，直到遇到空行或者到达文件末尾为止：

```python
with open('mydata.txt') as fp:
    for line in iter(fp.readline, '\n'):
		process_line(line)
```

- 以 iter(o) 的形式调用时返回的是迭代器；之后分析，以 iter(func, sentinel) 的形式调用时，能使用任何函数构建迭代器。

- 不使用 GeneratorType 实例实现斐波纳契数列生成器

  ```python
  class Fibonacci:
      def __iter__(self):
          return FibonacciGenerator()
      
  class FibonacciGenerator:
    def __init__(self):
        self.a = 0
        self.b = 1

    def __next__(self):
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result
  ```

- 符合 Python 风格的斐波纳契数列生成器


 ```python
def fibonacci():
	a, b = 0, 1
	while True:
		yield a
		a, b = b, a + b
 ```

### 上下文管理器

##### else 子句的行为如下：

> 在所有情况下，如果异常或者 return、break 或 continue 语句导致控制权跳到了复合语句的主块之外，else 子句也会被跳过。

- for

  > 仅当 for 循环运行完毕时（即 for 循环没有被 break 语句中止）才运行 else 块。

- while

  > 仅当 while 循环因为条件为假值而退出时（即 while 循环没有被break 语句中止）才运行 else 块。

- try

  > 仅当 try 块中没有异常抛出时才运行 else 块。

##### 上下文管理器和with块

- 上下文管理器对象存在的目的是管理wit语句。

- with 语句的目的是简化 try/finally 模式。

- 上下文管理器协议包含 \_\_enter\_\_ 和 \_\_exit\_\_ 两个方法

  > with 语句开始运行时，会在上下文管理器对象上调用 \_\_enter\_\_ 方法。with 语句运行结束后，会在上下文管理器对象上调用 \_\_exit\_\_ 方法，以此扮演 finally 子句的角色。

```python
class LookingGlass:
    """
    LookingGlass 上下文管理器类的代码
    """

    def __enter__(self):  # ➊ 除了 self 之外，Python 调用 __enter__ 方法时不传入其他参数。
        import sys
        self.original_write = sys.stdout.write  # ➋ 把原来的 sys.stdout.write 方法保存在一个实例属性中，供后面使用。
        sys.stdout.write = self.reverse_write  # ➌ 为 sys.stdout.write 打猴子补丁，替换成自己编写的方法。
        return 'JABBERWOCKY'  # ➍ 返回 'JABBERWOCKY' 字符串，这样才有内容存入目标变量 what。

    def reverse_write(self, text):  # ➎ 这是用于取代 sys.stdout.write 的方法，把 text 参数的内容反转，然后调用原来的实现。
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value,
                 traceback):  # ➏ 如果一切正常，Python 调用 __exit__ 方法时传入的参数是 None,None, None；如果抛出了异常，这三个参数是异常数据，如下所述。
        """
        :param exc_type: 异常类（例如 ZeroDivisionError）。
        :param exc_value: 异常实例。有时会有参数传给异常构造方法，例如错误消息，这些参数可以使用 exc_value.args 获取。
        :param traceback: traceback 对象。
        :return:
        """
        import sys  # ➐ 重复导入模块不会消耗很多资源，因为 Python 会缓存导入的模块。
        sys.stdout.write = self.original_write  # ➑ 还原成原来的 sys.stdout.write 方法。
        if exc_type is ZeroDivisionError:  # ➒ 如果有异常，而且是 ZeroDivisionError 类型，打印一个消息……
            print('Please DO NOT divide by zero!')
            return True  # ➓ ……然后返回 True，告诉解释器，异常已经处理了。


# ⓫ 如果 __exit__ 方法返回 None，或者 True 之外的值，with 块中的任何异常都会向上冒泡。


with LookingGlass() as what:  # ➊ 上下文管理器是 LookingGlass 类的实例；Python 在上下文管理器上调用 __enter__ 方法，把返回结果绑定到 what 上。
    print('Alice, Kitty and Snowdrop')  # ➋ 打印一个字符串，然后打印 what 变量的值。
    print(what)
# pordwonS dna yttiK ,ecilA # ➌ 打印出的内容是反向的。
# YKCOWREBBAJ
print(what)  # ➍ 现在，with 块已经执行完毕。可以看出，__enter__ 方法返回的值——即存储在 what 变量中的值——是字符串 'JABBERWOCKY'。
'JABBERWOCKY'
print('Back to normal.')  # ➎ 输出不再是反向的了。
# Back to normal.

manager = LookingGlass()  # ➊ 实例化并审查 manager 实例。
print(manager)
# <mirror.LookingGlass object at 0x2a578ac>
monster = manager.__enter__()  # ➋ 在上下文管理器上调用 __enter__() 方法，把结果存储在 monster中。
# ➌ monster 的值是字符串 'JABBERWOCKY'。打印出的 True 标识符是反向的，因为 stdout 的所有输出都经过 __enter__ 方法中打补丁的write 方法处理。
print(monster == 'JABBERWOCKY')
# eurT
print(monster)
'YKCOWREBBAJ'
print(manager)
# >ca875a2x0 ta tcejbo ssalGgnikooL.rorrim<
manager.__exit__(None, None, None)  # ➍ 调用 manager.__exit__，还原成之前的 stdout.write。
print(monster)
'JABBERWOCKY'
```

##### contextlib模块中的实用工具

1. closing

   > 如果对象提供了 close() 方法，但没有实现\_\_enter\_\_/\_\_exit\_\_ 协议，那么可以使用这个函数构建上下文管理器。

2. suppress

   > 构建临时忽略指定异常的上下文管理器。

3. @contextmanager

   > 这个装饰器把简单的生成器函数变成上下文管理器，这样就不用创建类去实现管理器协议了。

4. ContextDecorator

   > 这是个基类，用于定义基于类的上下文管理器。这种上下文管理器也能用于装饰函数，在受管理的上下文中运行整个函数。

5. ExitStack

   > 这个上下文管理器能进入多个上下文管理器。with 块结束时，ExitStack 按照后进先出的顺序调用栈中各个上下文管理器的\__exit__ 方法。如果事先不知道 with 块要进入多少个上下文管理器，可以使用这个类。例如，同时打开任意一个文件列表中的所有文件。

##### 使用@contextmanager

> @contextmanager 装饰器能减少创建上下文管理器的样板代码量，因为不用编写一个完整的类，定义 \_\_enter\_\_ 和 \_\_exit\_\_ 方法，而只需实现有一个 yield 语句的生成器，生成想让 \_\_enter\_\_ 方法返回的值。

- 在使用 @contextmanager 装饰的生成器中，yield 语句的作用是把函数的定义体分成两部分：yield 语句前面的所有代码在 with 块开始时（即解释器调用 \_\_enter\_\_ 方法时）执行， yield 语句后面的代码在with 块结束时（即调用 \_\_exit\_\_ 方法时）执行。
- contextlib.contextmanager 装饰器会把函数包装成实现\_\_enter\_\_ 和 \_\_exit\_\_ 方法的类。这个类的 \_\_enter\_\_ 方法有如下作用:
  - 调用生成器函数，保存生成器对象（这里把它称为 gen）。
  - 调用 next(gen)，执行到 yield 关键字所在的位置。
  - 返回 next(gen) 产出的值，以便把产出的值绑定到 with/as 语句中的目标变量上。
- with 块终止时，\_\_exit\_\_ 方法会做以下几件事:
  - 检查有没有把异常传给 exc_type；如果有，调用gen.throw(exception)，在生成器函数定义体中包含 yield 关键字的那一行抛出异常。
  - 否则，调用 next(gen)，继续执行生成器函数定义体中 yield 语句之后的代码。

- 使用生成器实现的上下文管理器

  ```python
  import contextlib
  
  
    @contextlib.contextmanager  # ➊ 应用 contextmanager 装饰器。
    def looking_glass():
        import sys
        original_write = sys.stdout.write  # ➋ 贮存原来的 sys.stdout.write 方法。
  
        def reverse_write(text):  # ➌ 定义自定义的 reverse_write 函数；在闭包中可以访问original_write。
            original_write(text[::-1])
        sys.stdout.write = reverse_write  # ➍ 把 sys.stdout.write 替换成 reverse_write。
        yield 'JABBERWOCKY'  # ➎ 产出一个值，这个值会绑定到 with 语句中 as 子句的目标变量上。执行 with 块中的代码时，这个函数会在这一点暂停。
        sys.stdout.write = original_write  # ➏ 控制权一旦跳出 with 块，继续执行 yield 语句之后的代码；这里是恢复成原来的 sys. stdout.write 方法。
  
    with looking_glass() as what:  # ➊
           print('Alice, Kitty and Snowdrop')
           print(what)
  ```


 ```python
import contextlib


@contextlib.contextmanager
def looking_glass():
  import sys
  original_write = sys.stdout.write

  def reverse_write(text):
    original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''  # ➊ 创建一个变量，用于保存可能出现的错误消息；与示例 15-5 相比，这是第一处改动。
    try:
      yield 'JABBERWOCKY'
      except ZeroDivisionError:  # ➋ 处理 ZeroDivisionError 异常，设置一个错误消息。
        msg = 'Please DO NOT divide by zero!'
        finally:
          sys.stdout.write = original_write  # ➌ 撤销对 sys.stdout.write 方法所做的猴子补丁。
          if msg:
            print(msg)  # ➍ 如果设置了错误消息，把它打印出来。
 ```

### 协程

> yield 关键字可以在表达式中使用，而且生成器 API 中增加了 .send(value) 方法。生成器的调用方可以使用 .send(...) 方法发送数据，发送的数据会成为生成器函数中 yield 表达式的值。

- 协程是指一个过程，这个过程与调用方协作，产出由调用方提供的值。
- 在协程中，yield 通常出现在表达式的右边（例如，datum = yield），可以产出值，也可以不产出——如果 yield关键字后面没有表达式，那么生成器产出 None。
- 协程可能会从调用方接收数据，不过调用方把数据提供给协程使用的是 .send(datum) 方法，而不是 next(...) 函数。通常，调用方会把值推送给协程。
- yield 关键字甚至还可以不接收或传出数据。不管数据如何流动，yield 都是一种流程控制工具，使用它可以实现协作式多任务：协程可以把控制器让步给中心调度程序，从而激活其他的协程。
- .send(...) :生成器的调用方可以使用 .send(...) 方法发送数据，发送的数据会成为生成器函数中 yield 表达式的值。
  - 因为 send 方法的参数会成为暂停的 yield 表达式的值，所以，仅当协程处于暂停状态时才能调用 send 方法。
- .throw(...)的作用是让调用方抛出异常，在生成器中处理。
- .close()方法的作用是终止生成器。

##### 用作协程的生成器的基本行为

```python
def simple_coroutine():  # ➊ 协程使用生成器函数定义：定义体中有 yield 关键字。
    print('-> coroutine started')
    x = yield  # ➋ yield 在表达式中使用；如果协程只需从客户那里接收数据，那么产出的值是 None——这个值是隐式指定的，因为 yield 关键字右边没有表达式。
    print('-> coroutine received:', x)


my_coro = simple_coroutine()
print(my_coro)  # ➌ 与创建生成器的方式一样，调用函数得到生成器对象。
# <generator object simple_coroutine at 0x100c2be10>
print(next(my_coro))  # ➍ 首先要调用 next(...) 函数，因为生成器还没启动，没在 yield 语句处暂停，所以一开始无法发送数据。
# -> coroutine started
# None
print(my_coro.send(42))  # ➎ 调用这个方法后，协程定义体中的 yield 表达式会计算出 42；现在，协程会恢复，一直运行到下一个 yield 表达式，或者终止。
# -> coroutine received: 42
# Traceback (most recent call last): # ➏ 这里，控制权流动到协程定义体的末尾，导致生成器像往常一样抛出 StopIteration 异常。
# ...
# StopIteration
```

- 当前状态可以使用inspect.getgeneratorstate(...) 函数确定，该函数会返回下述字符串中的一个。

  - 'GEN_CREATED'

    > 等待开始执行。

  - 'GEN_RUNNING'

    > 解释器正在执行。

  - 'GEN_SUSPENDED'

    > 在 yield 表达式处暂停。

    > 因为 send 方法的参数会成为暂停的 yield 表达式的值，所以，仅当协程处于暂停状态时才能调用 send 方法。不过，如果协程还没激活（即，状态是 'GEN_CREATED'），情况就不同了。因此，始终要调用 next(my_coro) 激活协程——也可以调用my_coro.send(None)，效果一样。

  - 'GEN_CLOSED'

    > 执行结束。

- 最先调用 next(my_coro) 函数这一步通常称为“预激”（prime）协程（即，让协程向前执行到第一个 yield 表达式，准备好作为活跃的协程使用）。

##### 产出两个值的协程

> 关键的一点是，协程在 yield 关键字所在的位置暂停执行。前面说过，在赋值语句中，= 右边的代码在赋值之前执行。因此，对于 b =yield a 这行代码来说，等到客户端代码再激活协程时才会设定 b 的值。

```python
def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b =', b)
    c = yield a + b
    print('-> Received: c =', c)


my_coro2 = simple_coro2(14)
from inspect import getgeneratorstate

getgeneratorstate(my_coro2)  # ➊ inspect.getgeneratorstate 函数指明，处于 GEN_CREATED 状态（即协程未启动）。
'GEN_CREATED'
print(next(my_coro2))  # ➋ 向前执行协程到第一个 yield 表达式，打印 -> Started: a = 14消息，然后产出 a 的值，并且暂停，等待为 b 赋值。
# -> Started: a = 14
# 14
getgeneratorstate(my_coro2)  # ➌ getgeneratorstate 函数指明，处于 GEN_SUSPENDED 状态（即协程在 yield 表达式处暂停）。
'GEN_SUSPENDED'
print(my_coro2.send(
    28))  # ➍ 把数字 28 发给暂停的协程；计算 yield 表达式，得到 28，然后把那个数绑定给 b。打印 -> Received: b = 28 消息，产出 a + b 的值（42），然后协程暂停，等待为 c 赋值。
# -> Received: b = 28
# 42
print(my_coro2.send(99))  # ➎把数字 99 发给暂停的协程；计算 yield 表达式，得到 99，然后把那个数绑定给 c。打印 -> Received: c = 99 消息，然后协程终止，导致生成器对象抛出 StopIteration 异常。
# -> Received: c = 99
# Traceback (most recent call last):
# File "<stdin>", line 1, in <module>
# StopIteration
getgeneratorstate(my_coro2)  # ➏ getgeneratorstate 函数指明，处于 GEN_CLOSED 状态（即协程执行结束）。
'GEN_CLOSED'
```

- simple_coro2 协程的执行过程分为 3 个阶段
  - 调用 next(my_coro2)，打印第一个消息，然后执行 yield a，产出数字 14。
  - 调用 my_coro2.send(28)，把 28 赋值给 b，打印第二个消息，然后执行 yield a + b，产出数字 42。
  - 调用 my_coro2.send(99)，把 99 赋值给 c，打印第三个消息，协程终止。

##### 使用协程计算移动平均值

- 定义一个计算移动平均值的协程

  > 使用协程的好处是，total 和 count 声明为局部变量即可，无需使用实例属性或闭包在多次调用之间保持上下文。

  ```python
  def averager():
      total = 0.0
      count = 0
      average = None
      while True:  # ➊ 这个无限循环表明，只要调用方不断把值发给这个协程，它就会一直接收值，然后生成结果。仅当调用方在协程上调用 .close() 方法，或者没有对协程的引用而被垃圾回收程序回收时，这个协程才会终止。
          term = yield average  # ➋ 这里的 yield 表达式用于暂停执行协程，把结果发给调用方；还用于接收调用方后面发给协程的值，恢复无限循环。
          total += term
          count += 1
          average = total / count
  
  """
  调用 next(coro_avg) 函数后，协程会向前执行到 yield 表达式，产出 average 变量的初始值——None，因此不会出现在控制台中。此时，协程在 yield 表达式处暂停，等到调用方发送值。coro_avg.send(10) 那一行发送一个值，激活协程，把发送的值赋给 term，并更新 total、count 和 average 三个变量的值，然后开始 while 循环的下一次迭代，产出 average 变量的值，等待下一次为 term 变量赋值。
  """
  coro_avg = averager()  # ➊ 创建协程对象。
  # 调用 next(coro_avg) 函数后，协程会向前执行到 yield 表达式，产出 average 变量的初始值——None
  print(next(coro_avg))  # ➋ 调用 next 函数，预激协程。
  # None
  print(coro_avg.send(10))  # ➌ 计算移动平均值：多次调用 .send(...) 方法，产出当前的平均值。
  # 10.0
  print(coro_avg.send(30))
  # 20.0
  print(coro_avg.send(5))
  # 15.0
  ```

##### 预激协程的装饰器

> 如果不预激，那么协程没什么用。调用 my_coro.send(x) 之前，记住一定要调用 next(my_coro)。为了简化协程的用法，有时会使用一个预激装饰器。

- 使用@coroutine 装饰器定义并测试计算移动平均值的协程

  ```python
  from functools import wraps
  
  
    def coroutine(func):
        """装饰器：向前执行到第一个`yield`表达式，预激`func`"""
  
        @wraps(func)
        def primer(*args, **kwargs):  # ➊ 把被装饰的生成器函数替换成这里的 primer 函数；调用 primer 函数时，返回预激后的生成器。
            gen = func(*args, **kwargs)  # ➋ 调用被装饰的函数，获取生成器对象。
            next(gen)  # ➌ 预激生成器。
            return gen  # ➍ 返回生成器。
      
        return primer
  
  
    @coroutine  # ➎ 把装饰器应用到 averager 函数上。
    def averager():
        total = 0.0
        count = 0
        average = None
        while True:  # ➊ 这个无限循环表明，只要调用方不断把值发给这个协程，它就会一直接收值，然后生成结果。仅当调用方在协程上调用 .close() 方法，或者没有对协程的引用而被垃圾回收程序回收时，这个协程才会终止。
            term = yield average  # ➋ 这里的 yield 表达式用于暂停执行协程，把结果发给调用方；还用于接收调用方后面发给协程的值，恢复无限循环。
            total += term
            count += 1
            average = total / count
  
  
    coro_avg = averager()  # ➊ 调用 averager() 函数创建一个生成器对象，在 coroutine 装饰器的 primer 函数中已经预激了这个生成器。
  
    from inspect import getgeneratorstate
  
    print(getgeneratorstate(coro_avg))  # ➋ getgeneratorstate 函数指明，处于 GEN_SUSPENDED 状态，因此这个协程已经准备好，可以接收值了。
  
    'GEN_SUSPENDED'
  
    print(coro_avg.send(10))  # ➌ 可以立即开始把值发给 coro_avg——这正是 coroutine 装饰器的目的。
    # 10.0
    print(coro_avg.send(30))
    # 20.0
    print(coro_avg.send(5))
    # 15.0
  ```


- 使用 yield from 句法调用协程时，会自动预激，因此与 @coroutine 等装饰器不兼容。

- Python 3.4 标准库里的 asyncio.coroutine 装饰器不会预激协程，因此能兼容 yield from 句法。

##### 未处理的异常会导致协程终止

- 终止协程的一种方式：发送某个哨符值，让协程退出。
- 内置的 None 和 Ellipsis 等常量经常用作哨符值。
- Ellipsis 的优点是，数据流中不太常有这个值。

 ```python
from functools import wraps


def coroutine(func):
    """装饰器：向前执行到第一个`yield`表达式，预激`func`"""

    @wraps(func)
    def primer(*args, **kwargs):  # ➊ 把被装饰的生成器函数替换成这里的 primer 函数；调用 primer 函数时，返回预激后的生成器。
        gen = func(*args, **kwargs)  # ➋ 调用被装饰的函数，获取生成器对象。
        next(gen)  # ➌ 预激生成器。
        return gen  # ➍ 返回生成器。

    return primer


@coroutine  # ➎ 把装饰器应用到 averager 函数上。
def averager():
    total = 0.0
    count = 0
    average = None
    while True:  # ➊ 这个无限循环表明，只要调用方不断把值发给这个协程，它就会一直接收值，然后生成结果。仅当调用方在协程上调用 .close() 方法，或者没有对协程的引用而被垃圾回收程序回收时，这个协程才会终止。
        term = yield average  # ➋ 这里的 yield 表达式用于暂停执行协程，把结果发给调用方；还用于接收调用方后面发给协程的值，恢复无限循环。
        total += term
        count += 1
        average = total / count


coro_avg = averager()
print(coro_avg.send(40))  # ➊ 使用 @coroutine 装饰器装饰的 averager 协程，可以立即开始发送值。
# 40.0
print(coro_avg.send(50))
# 45.0
print(coro_avg.send('spam'))  # ➋ 发送的值不是数字，导致协程内部有异常抛出。
# Traceback (most recent call last):
# ...
# TypeError: unsupported operand type(s) for +=: 'float' and 'str'
print(coro_avg.send(60))  # ➌ 由于在协程内没有处理异常，协程会终止。如果试图重新激活协程，会抛出 StopIteration 异常。
# Traceback (most recent call last):
# File "<stdin>", line 1, in <module>
# StopIteration
 ```

- generator.throw(exc_type[, exc_value[, traceback]])

  > 致使生成器在暂停的 yield 表达式处抛出指定的异常。如果生成器处理了抛出的异常，代码会向前执行到下一个 yield 表达式，而产出的值会成为调用 generator.throw 方法得到的返回值。如果生成器没有处理抛出的异常，异常会向上冒泡，传到调用方的上下文中。

- generator.close()

  > 致使生成器在暂停的 yield 表达式处抛出 GeneratorExit 异常。如果生成器没有处理这个异常，或者抛出了 StopIteration 异常（通常是指运行到结尾），调用方不会报错。如果收到 GeneratorExit 异常，生成器一定不能产出值，否则解释器会抛出 RuntimeError 异常。生成器抛出的其他异常会向上冒泡，传给调用方。

##### 激活和关闭 demo_exc_handling，没有异常

```python
class DemoException(Exception):
    """为这次演示定义的异常类型。"""


def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:  # ➊ 特别处理 DemoException 异常。
            print('*** DemoException handled. Continuing...')
        else:  # ➋ 如果没有异常，那么显示接收到的值。
            print('-> coroutine received: {!r}'.format(x))
    # raise RuntimeError('This line should never run.')  # ➌ 这一行永远不会执行。


exc_coro = demo_exc_handling()
print(next(exc_coro))
# -> coroutine started
print(exc_coro.send(11))
# -> coroutine received: 11
print(exc_coro.send(22))
# -> coroutine received: 22
exc_coro.close()
from inspect import getgeneratorstate

print(getgeneratorstate(exc_coro))
'GEN_CLOSED'
```

- 把 DemoException 异常传入 demo_exc_handling 不会导致协程中止

  ```python
  from inspect import getgeneratorstate

  exc_coro = demo_exc_handling()
  next(exc_coro)
  # -> coroutine started
  exc_coro.send(11)
  # -> coroutine received: 11
  exc_coro.throw(DemoException)
  # *** DemoException handled. Continuing...
  getgeneratorstate(exc_coro)
  'GEN_SUSPENDED'
  ```

- 如果无法处理传入的异常，协程会终止

  ```python
  from inspect import getgeneratorstate

  exc_coro = demo_exc_handling()
  print(next(exc_coro))
  # -> coroutine started
  print(exc_coro.send(11))
  # -> coroutine received: 11
  print(exc_coro.throw(ZeroDivisionError))
  # Traceback (most recent call last):
  # ...
  # ZeroDivisionError
  print(getgeneratorstate(exc_coro))
  'GEN_CLOSED'
  ```

- 如果不管协程如何结束都想做些清理工作，要把协程定义体中相关的代码放入 try/finally 块中，

  ```python
  class DemoException(Exception):
        """为这次演示定义的异常类型。"""
  
  
    def demo_finally():
        # 使用 try/finally 块在协程终止时执行操作
        print('-> coroutine started')
        try:
            while True:
                try:
                    x = yield
                except DemoException:
                    print('*** DemoException handled. Continuing...')
                else:
                    print('-> coroutine received: {!r}'.format(x))
        finally:
            print('-> coroutine ending')
  ```


##### 让协程返回值

  ```python
from collections import namedtuple

Result = namedtuple('Result', 'count average')


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break  # ➊ 为了返回值，协程必须正常终止；因此，这一版 averager 中有个条件判断，以便退出累计循环。
        total += term
        count += 1
        average = total / count
    return Result(count, average)  # ➋ 返回一个 namedtuple，包含 count 和 average 两个字段。


coro_avg = averager()
print(next(coro_avg))
print(coro_avg.send(10))  # ➊ 这一版不产出值。
print(coro_avg.send(30))
print(coro_avg.send(6.5))
print(coro_avg.send(None))  # ➋
# Traceback (most recent call last):
# ...
# StopIteration: Result(count=3, average=15.5)
  ```

- 捕获 StopIteration 异常，获取 averager 返回的值

  ```python
  coro_avg = averager()
  print(next(coro_avg))
  print(coro_avg.send(10))  # ➊ 这一版不产出值。
  print(coro_avg.send(30))
  print(coro_avg.send(6.5))
  try:
      coro_avg.send(None)
  except StopIteration as exc:
      result = exc.value
  	print(result)
  # Result(count=3, average=15.5)
  ```

##### 使用yield from

> yield from 结构会在内部自动捕获StopIteration 异常。这种处理方式与 for 循环处理 StopIteration异常的方式一样：循环机制使用用户易于理解的方式处理异常。对yield from 结构来说，解释器不仅会捕获 StopIteration 异常，还会把 value 属性的值变成 yield from 表达式的值。
>
> yield from x表达式对x对象所做的第一件事是，调用iter(x)，从中获取迭代器。因此，x可以是任何可迭代的对象。

> yield from 的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连接起来，这样二者可以直接发送和产出值，还可以直接传入异常，而不用在位于中间的协程中添加大量处理异常的样板代码。有了这个结构，协程可以通过以前不可能的方式委托职责。
>
> Python 3.3 引入 yield from 结构的主要原因之一与把异常传入嵌套的协程有关。另一个原因是让协程更方便地返回值。
>
> 引入 yield from 结构的目的是为了支持实现了\__next__、send、close 和 throw 方法的生成器。

- yield from 可用于简化 for 循环中的 yield 表达式。

  > yield from x 表达式对 x 对象所做的第一件事是，调用 iter(x)，从中获取迭代器。因此，x 可以是任何可迭代的对象。

```python
def gen():
  for c in 'AB':
      yield c
  for i in range(1, 3):
      yield i


print(list(gen()))


# ['A', 'B', 1, 2]

def gen_for():
  yield from 'AB'
  yield from range(1, 3)


print(list(gen_for()))
# ['A', 'B', 1, 2]

def chain(*iterables):
  for it in iterables:
  yield from it

  s = 'ABC'
  t = tuple(range(3))
  print(list(chain(s, t)))
  # ['A', 'B', 'C', 0, 1, 2]
```




- 委派生成器

  > 　　包含 yield from <iterable> 表达式的生成器函数。

- 子生成器

  > 从 yield from 表达式中 <iterable> 部分获取的生成器。

- 调用方

  > PEP 380 使用“调用方”这个术语指代调用委派生成器的客户端代码。

- 委派生成器在 yield from 表达式处暂停时，调用方可以直接把数据发给子生成器，子生成器再把产出的值发给调用方。子生成器返回之后，解释器会抛出 StopIteration 异常，并把返回值附加到异常对象上，此时委派生成器会恢复。

##### 使用 yield from 计算平均值并输出统计报告
```python
from collections import namedtuple

Result = namedtuple('Result', 'count average')


# 子生成器
def averager():  # ➊ 与示例 16-13 中的 averager 协程一样。这里作为子生成器使用。
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield  # ➋ main 函数中的客户代码发送的各个值绑定到这里的 term 变量上。
        if term is None:  # ➌ 至关重要的终止条件。如果不这么做，使用 yield from 调用这个协程的生成器会永远阻塞。
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)  # ➍ 返回的 Result 会成为 grouper 函数中 yield from 表达式的值。


# 委派生成器
def grouper(results, key):  # ➎ grouper 是委派生成器。
    while True:  # ➏ 这个循环每次迭代时会新建一个 averager 实例；每个实例都是作为协程使用的生成器对象。
        # ➐ grouper 发送的每个值都会经由 yield from 处理，通过管道传给
        # averager 实例。grouper 会在 yield from 表达式处暂停，等待
        # averager 实例处理客户端发来的值。averager 实例运行完毕后，返
        # 回的值绑定到 results[key] 上。while 循环会不断创建 averager 实
        # 例，处理更多的值。
        results[key] = yield from averager()


# 客户端代码，即调用方
def main(data):  # ➑ main 函数是客户端代码，用 PEP 380 定义的术语来说，是“调用方”。这是驱动一切的函数。
    results = {}
    for key, values in data.items():
        group = grouper(results, key)  # ➒ group 是调用 grouper 函数得到的生成器对象，传给 grouper 函数的第一个参数是 results，用于收集结果；第二个参数是某个键。group 作为协程使用。
        next(group)  # ➓ 预激 group 协程。
        for value in values:
            group.send(value)  # ⓫ 把各个 value 传给 grouper。传入的值最终到达 averager 函数中term = yield 那一行；grouper 永远不知道传入的值是什么。
        group.send(None)  # 重要！ ⓬ 把 None 传入 grouper，导致当前的 averager 实例终止，也让grouper 继续运行，再创建一个 averager 实例，处理下一组值。
        # print(results) # 如果要调试，去掉注释
        report(results)


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}
if __name__ == '__main__':
    main(data)

# 10 girls averaging 42.04kg
# 10 girls averaging 42.04kg
# 10 girls averaging 1.43m
#  9 boys  averaging 40.42kg
# 10 girls averaging 42.04kg
# 10 girls averaging 1.43m
#  9 boys  averaging 40.42kg
#  9 boys  averaging 1.39m
# 10 girls averaging 42.04kg
# 10 girls averaging 1.43m
```

**简要说明示例的运作方式：**

- 外层 for 循环每次迭代会新建一个 grouper 实例，赋值给 group变量；group 是委派生成器。
- 调用 next(group)，预激委派生成器 grouper，此时进入 whileTrue 循环，调用子生成器 averager 后，在 yield from 表达式处暂停。
- 内层 for 循环调用 group.send(value)，直接把值传给子生成器averager。同时，当前的 grouper 实例（group）在 yieldfrom 表达式处暂停。
- 内层循环结束后，group 实例依旧在 yield from 表达式处暂停，因此，grouper 函数定义体中为 results[key] 赋值的语句还没有执行。
- 如果外层 for 循环的末尾没有 group.send(None)，那么averager 子生成器永远不会终止，委派生成器 group 永远不会再次激活，因此永远不会为 results[key] 赋值。
- 外层 for 循环重新迭代时会新建一个 grouper 实例，然后绑定到group 变量上。前一个 grouper 实例（以及它创建的尚未终止的averager 子生成器实例）被垃圾回收程序回收。

##### yield from 的行为

- 子生成器产出的值都直接传给委派生成器的调用方（即客户端代码）。
- 使用 send() 方法发给委派生成器的值都直接传给子生成器。如果发送的值是 None，那么会调用子生成器的 \__next__() 方法。如果发送的值不是 None，那么会调用子生成器的 send() 方法。如果调用的方法抛出 StopIteration 异常，那么委派生成器恢复运行。任何其他异常都会向上冒泡，传给委派生成器。
- 生成器退出时，生成器（或子生成器）中的 return expr 表达式会触发 StopIteration(expr) 异常抛出。
- yield from 表达式的值是子生成器终止时传给 StopIteration异常的第一个参数。
- 传入委派生成器的异常，除了 GeneratorExit 之外都传给子生成器的 throw() 方法。如果调用 throw() 方法时抛出StopIteration 异常，委派生成器恢复运行。StopIteration 之外的异常会向上冒泡，传给委派生成器。
- 如果把 GeneratorExit 异常传入委派生成器，或者在委派生成器上调用 close() 方法，那么在子生成器上调用 close() 方法，如果它有的话。如果调用 close() 方法导致异常抛出，那么异常会向上冒泡，传给委派生成器；否则，委派生成器抛出GeneratorExit 异常。





### 使用期物处理并发

- 期物指一种对象，表示异步执行的操作。这个概念的作用很大，是 concurrent.futures 模块和asyncio 包的基础。

- 依序下载的脚本

 ```python

 ```


##### 使用concurrent.futures模块下载

- 使用futures.ThreadPoolExecutor 类实现多线程下载的脚本：

 ```python
import os
import time
import sys
from concurrent import futures
import requests  # ➊ 导入 requests 库。这个库不在标准库中，因此依照惯例，在导入标准库中的模块（os、time 和 sys）之后导入，而且使用一个空行分隔开。

MAX_WORKERS = 20  # ➋ 设定 ThreadPoolExecutor 类最多使用几个线程。

# ➋ 列出人口最多的 20 个国家的 ISO 3166 国家代码，按照人口数量降序排列。
POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'  # ➌ 获取国旗图像的网站。
DEST_DIR = '../downloads/'  # ➍ 保存图像的本地目录。


def save_flag(img, filename):  # ➎ 把 img（字节序列）保存到 DEST_DIR 目录中，命名为 filename。
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):  # ➏ 指定国家代码，构建 URL，然后下载图像，返回响应中的二进制内容。
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):  # ➐ 显示一个字符串，然后刷新 sys.stdout，这样能在一行消息中看到进度。在 Python 中得这么做，因为正常情况下，遇到换行才会刷新stdout 缓冲。
    print(text, end=' ')
    sys.stdout.flush()


def download_one(cc):  # ➌ 下载一个图像的函数；这是在各个线程中执行的函数。
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))  # ➍ 设定工作的线程数量：使用允许的最大值（MAX_WORKERS）与要处理的数量之间较小的那个值，以免创建多余的线程。
    # ➎ 使用工作的线程数实例化 ThreadPoolExecutor类；executor.__exit__ 方法会调用executor.shutdown(wait=True) 方法，它会在所有线程都执行完毕前阻塞线程。
    with futures.ThreadPoolExecutor(workers) as executor:
        # ➏ map 方法的作用与内置的 map 函数类似，不过 download_one 函数会在多个线程中并发调用；map 方法返回一个生成器，因此可以迭代，获取各个函数返回的值。
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))  # ➐返回获取的结果数量；如果有线程抛出异常，异常会在这里抛出，这与隐式调用 next() 函数从迭代器中获取相应的返回值一样。


def main(download_many):  # ➓ main 函数记录并报告运行 download_many 函数之后的耗时。
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)  # 调用 flags 模块中的 main 函数，传入 download_many 函数的增强版。
 ```

- 把download_many 函数中的executor.map 方法换成 executor.submit 方法和futures.as_completed 函数

  > executor.submit 和futures.as_completed这个组合比executor.map更灵活，因为submit方法能处理不同的可调用对象和参数，而executor.map只能处理参数不同的同一个可调用对象。此外，传给futures.as_completed函数的期物集合可以来自多个Executor实例，例如一些由ThreadPoolExecutor实例创建，另一些由ProcessPoolExecutor实例创建。

  ```python
  def download_many(cc_list):
      cc_list = cc_list[:5] # ➊ 这次演示只使用人口最多的 5 个国家。
      with futures.ThreadPoolExecutor(max_workers=3) as executor: # ➋ 把 max_workers 硬编码为 3，以便在输出中观察待完成的期物。
          to_do = []
          for cc in sorted(cc_list): # ➌ 按照字母表顺序迭代国家代码，明确表明输出的顺序与输入一致。
              future = executor.submit(download_one, cc) # ➍ executor.submit 方法排定可调用对象的执行时间，然后返回一个期物，表示这个待执行的操作。
              to_do.append(future) # ➎ 存储各个期物，后面传给 as_completed 函数。
              msg = 'Scheduled for {}: {}'
              print(msg.format(cc, future)) # ➏ 显示一个消息，包含国家代码和对应的期物。
              
          results = []
          for future in futures.as_completed(to_do): # ➐ as_completed 函数在期物运行结束后产出期物。
              res = future.result() # ➑ 获取该期物的结果。
              msg = '{} result: {!r}'
              print(msg.format(future, res)) # ➒ 显示期物及其结果。
              results.append(res)
              
      return len(results)
  ```

- GIL（Global InterpreterLock，全局解释器锁）
  - CPython 解释器本身就不是线程安全的，因此有全局解释器锁（GIL），一次只允许使用一个线程执行 Python 字节码。
  - Python 标准库中的所有阻塞型 I/O 函数都会释放 GIL，允许其他线程运行。
  - time.sleep() 函数也会释放 GIL。
  - 尽管有GIL，Python 线程还是能在 I/O 密集型应用中发挥作用。

- 对I/O 密集型处理来说，可以在一个 ThreadPoolExecutor 实例中使用 10个、100 个或 1000 个线程；最佳线程数取决于做的是什么事，以及可用内存有多少，因此要仔细测试才能找到最佳的线程数。

##### 使用concurrent.futures模块启动进程

> 这个模块实现的是真正的并行计算，因为它使用 ProcessPoolExecutor 类把工作分配给多个Python 进程处理。因此，如果需要做 CPU 密集型处理，使用这个模块能绕开 GIL，利用所有可用的 CPU 核心。

```python
def download_many(cc_list):
    with futures.ProcessPoolExecutor() as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))
```

##### 简单演示ThreadPoolExecutor 类的 map 方法

```python
from time import sleep, strftime
from concurrent import futures


def display(*args):  # ➊ 这个函数的作用很简单，把传入的参数打印出来，并在前面加上[HH:MM:SS] 格式的时间戳。
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):  # ➋ loiter 函数什么也没做，只是在开始时显示一个消息，然后休眠 n秒，最后在结束时再显示一个消息；消息使用制表符缩进，缩进的量由n 的值确定。
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))
    return n * 10  # ➌ loiter 函数返回 n * 10，以便让我们了解收集结果的方式。


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)  # ➍ 创建 ThreadPoolExecutor 实例，有 3 个线程。
    # ➎ 把五个任务提交给 executor（因为只有 3 个线程，所以只有 3 个任务会立即开始：loiter(0)、loiter(1) 和 loiter(2)）；这是非阻塞调用。
    results = executor.map(loiter, range(5))
    display('results:', results)  # ➏ 立即显示调用 executor.map 方法的结果：一个生成器，如示例 17-7 中的输出所示。
    display('Waiting for individual results:')
    # ➐ for 循环中的 enumerate 函数会隐式调用 next(results)，这个函数又会在（内部）表示第一个任务（loiter(0)）的 _f 期物上调用_f.result() 方法。
    # result 方法会阻塞，直到期物运行结束，因此这个循环每次迭代时都要等待下一个结果做好准备。
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


main()

# [15:56:50] Script starting. ➊ 这次运行从 15:56:50 开始。
# [15:56:50] loiter(0): doing nothing for 0s... ➋ 第一个线程执行 loiter(0)，因此休眠 0 秒，甚至会在第二个线程开始之前就结束，不过具体情况因人而异。
# [15:56:50] loiter(0): done.
# [15:56:50] loiter(1): doing nothing for 1s... ➌ loiter(1) 和 loiter(2) 立即开始（因为线程池中有三个职程，可以并发运行三个函数）。
# [15:56:50] loiter(2): doing nothing for 2s...
# [15:56:50] results: <generator object result_iterator at 0x106517168> ➍ 这一行表明，executor.map 方法返回的结果（results）是生成器；不管有多少任务，也不管 max_workers 的值是多少，目前不会阻塞。
# [15:56:50] loiter(3): doing nothing for 3s... ➎ loiter(0) 运行结束了，第一个职程可以启动第四个线程，运行loiter(3)。
# [15:56:50] Waiting for individual results:
# [15:56:50] result 0: 0 ➏ 此时执行过程可能阻塞，具体情况取决于传给 loiter 函数的参数：results 生成器的 __next__ 方法必须等到第一个期物运行结束。此时不会阻塞，因为 loiter(0) 在循环开始前结束。注意，这一点之前的所有事件都在同一刻发生——15:56:50。
# [15:56:51] loiter(1): done. ➐ 一秒钟后，即 15:56:51，loiter(1) 运行完毕。这个线程闲置，可以开始运行 loiter(4)。
# [15:56:51] loiter(4): doing nothing for 4s...
# [15:56:51] result 1: 10 ➑ 显示 loiter(1) 的结果：10。现在，for 循环会阻塞，等待loiter(2) 的结果。
# [15:56:52] loiter(2): done. ➒ 同上：loiter(2) 运行结束，显示结果；loiter(3) 也一样。
# [15:56:52] result 2: 20
# [15:56:53] loiter(3): done.
# [15:56:53] result 3: 30
# [15:56:55] loiter(4): done. ➓ 2 秒钟后 loiter(4) 运行结束，因为 loiter(4) 在 15:56:51 时开始，休眠了 4 秒。
# [15:56:55] result 4: 40
```

### 使用 asyncio 包处理并发

##### 通过线程以动画形式显示文本式旋转指针

```python
import threading
import itertools
import time
import sys


class Signal:  # ➊ 这个类定义一个简单的可变对象；其中有个 go 属性，用于从外部控制线程。
    go = True


def spin(msg, signal):  # ➋ 这个函数会在单独的线程中运行。signal 参数是前面定义的Signal 类的实例。
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-+~!?*'):  # ➌ 这其实是个无限循环，因为 itertools.cycle 函数会从指定的序列中反复不断地生成元素。
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  # ➍ 这是显示文本式动画的诀窍所在：使用退格符（\x08）把光标移回来。
        time.sleep(.9)
        if not signal.go:  # ➎ 如果 go 属性的值不是 True 了，那就退出循环。
            break
    write(' ' * len(status) + '\x08' * len(status))  # ➏ 使用空格清除状态消息，把光标移回开头。


def slow_function():  # ➐ 假设这是耗时的计算。
    # 假装等待I/O一段时间
    time.sleep(10)  # ➑ 调用 sleep 函数会阻塞主线程，不过一定要这么做，以便释放GIL，创建从属线程。
    return 42


def supervisor():  # ➒ 这个函数设置从属线程，显示线程对象，运行耗时的计算，最后杀死线程。
    signal = Signal()
    spinner = threading.Thread(target=spin, args=('thinking!', signal))
    print('spinner object:', spinner)  # ➓ 显示从属线程对象。输出类似于 <Thread(Thread-1,initial)>。
    spinner.start()  # ⓫ 启动从属线程。
    result = slow_function()  # ⓬ 运行 slow_function 函数，阻塞主线程。同时，从属线程以动画形式显示旋转指针。
    signal.go = False  # ⓭ 改变 signal 的状态；这会终止 spin 函数中的那个 for 循环。
    spinner.join()  # ⓮ 等待 spinner 线程结束。
    return result


def main():
    result = supervisor()  # ⓯ 运行 supervisor 函数。
    print('Answer:', result)


if __name__ == '__main__':
    main()
```

##### 通过协程以动画形式显示文本式旋转指针
```python
"""
使用 @asyncio.coroutine 装饰器不是强制要求，但是强烈建议这么做，因为这样能在一众普通的函数中把协程凸显出来，也有助于调试：如果还没从中产出值，协程就被垃圾回收了（意味着有操作未完成，因此有可能是个缺陷），那就可以发出警告。这个装饰器不会预激协程。
"""

import asyncio
import itertools
import sys


@asyncio.coroutine  # ➊ 打算交给 asyncio 处理的协程要使用 @asyncio.coroutine 装饰。这不是强制要求，但是强烈建议这么做。原因在本列表后面。
def spin(msg):  # ➋ 这里不需要示例 18-1 中 spin 函数中用来关闭线程的 signal 参数。
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\+*-~!@#$%'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(.8)  # ➌ 使用 yield from asyncio.sleep(.1) 代替 time.sleep(.1)，这样的休眠不会阻塞事件循环。
        except asyncio.CancelledError:  # ➍ 如果 spin 函数苏醒后抛出 asyncio.CancelledError 异常，其原因是发出了取消请求，因此退出循环。
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():  # ➎ 现在，slow_function 函数是协程，在用休眠假装进行 I/O 操作时，使用 yield from 继续执行事件循环。
    # 假装等待I/O一段时间
    yield from asyncio.sleep(10)  # ➏ yield from asyncio.sleep(10) 表达式把控制权交给主循环，在休眠结束后恢复这个协程。
    return 42


@asyncio.coroutine
def supervisor():  # ➐ 现在，supervisor 函数也是协程，因此可以使用 yield from 驱动slow_function 函数。
    spinner = asyncio.async(spin('thinking!'))  # ➑ asyncio.async(...) 函数排定 spin 协程的运行时间，使用一个Task 对象包装 spin 协程，并立即返回。
    print('spinner object:', spinner)  # ➒ 显示 Task 对象。输出类似于 <Task pending coro=<spin()running at spinner_ asyncio.py:12>>。
    # ➓ 驱动 slow_function() 函数。结束后，获取返回值。同时，事件循环继续运行，因为 slow_function 函数最后使用 yield fromasyncio.sleep(3) 表达式把控制权交回给了主循环。
    result = yield from slow_function()
    spinner.cancel()  # ⓫ Task 对象可以取消；取消后会在协程当前暂停的 yield 处抛出asyncio.CancelledError 异常。协程可以捕获这个异常，也可以延迟取消，甚至拒绝取消。
    return result


def main():
    loop = asyncio.get_event_loop()  # ⓬ 获取事件循环的引用。
    result = loop.run_until_complete(supervisor())  # ⓭ 驱动 supervisor 协程，让它运行完毕；这个协程的返回值是这次调用的返回值。
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
```

##### 线程版 supervisor 函数和异步版 supervisor 协程实现之间的主要区别：

> 线程与协程之间的比较还有最后一点要说明：如果使用线程做过重要的编程，你就知道写出程序有多么困难，因为调度程序任何时候都能中断线程。必须记住保留锁，去保护程序中的重要部分，防止多步操作在执行的过程中中断，防止数据处于无效状态。而协程默认会做好全方位保护，以防止中断。我们必须显式产出才能让程序的余下部分运行。对协程来说，无需保留锁，在多个线程之间同步操作，协程自身就会同步，因为在任意时刻只有一个协程运行。想交出控制权时，可以使用 yield 或 yield from 把控制权交还调度程序。这就是能够安全地取消协程的原因：按照定义，协程只能在暂停的yield 处取消，因此可以处理 CancelledError 异常，执行清理操作。

- asyncio.Task 对象差不多与 threading.Thread 对象等效。Victor Stinner（本章的特约技术审校）指出，“Task 对象像是实现协作式多任务的库（例如 gevent）中的绿色线程（greenthread）”。
- Task 对象用于驱动协程，Thread 对象用于调用可调用的对象。
- Task 对象不由自己动手实例化，而是通过把协程传给asyncio.async(...) 函数或 loop.create_task(...) 方法获取。
- 获取的 Task 对象已经排定了运行时间（例如，由 asyncio.async函数排定）；Thread 实例则必须调用 start 方法，明确告知让它运行。
- 在线程版 supervisor 函数中，slow_function 函数是普通的函数，直接由线程调用。在异步版 supervisor 函数中，slow_function 函数是协程，由 yield from 驱动。
- 没有 API 能从外部终止线程，因为线程随时可能被中断，导致系统处于无效状态。如果想终止任务，可以使用 Task.cancel() 实例方法，在协程内部抛出 CancelledError 异常。协程可以在暂停的yield 处捕获这个异常，处理终止请求。
- supervisor 协程必须在 main 函数中由loop.run_until_complete 方法执行。