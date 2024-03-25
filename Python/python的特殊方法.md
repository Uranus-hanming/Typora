[toc]

##### python的特殊方法

###### \_\_repr__（print()）

> 能把一个对象用字符串的形式表达出来以便辨认，这就是“字符串表示形式”。
>
> \__repr__所返回的字符串应该准确、无歧义，并且尽可能表达出如何用代码创建出这个被打印的对象。

```python
class Test():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '这个类的名字是: % s' % self.name


str = Test('科學')
print(str)  # 这个类的名字是: 科学
```

###### \__str__（print()、str()）

> 当使用print输出对象的时候，若定义了__str__(self)方法，打印对象时就会从这个方法中打印出return的z字符串数据。

- __str__()用于显示给用户，而__repr__()用于显示给开发人员
- \__str__是在 str() 函数被使用，或是在用 print 函数打印一个对象的时候才被调用的，并且它返回的字符串对终端用户更友好。
- 如果一个对象没有_\_str__函数，而python又需要调用它的时候，解释器会用\_\_repr\_\_作为替代

###### \__len__（len()）

###### \__bool__（bool()）
> bool(x)的背后是调用x.\__bool__()的结果；如果不存在\__bool__方法，那么bool(x)会尝试调用x.\__len__()。

###### \__format__（format()）

```python
_formats = {'ymd': '{d.year}-{d.month}-{d.day}', 'mdy': '{d.month}/{d.day}/{d.year}'}


class Date:
    def __init__(self, year, month, day):
        self.year = year

        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'

        fmt = _formats[code]
        return fmt.format(d=self)


d = Date(2018, 8, 8)
r = format(d)
```

###### \__getitem__

> 这个方法返回所给键对应的值。当对象是序列时，键是整数。当对象是映射时（字典），键是任意值。

```python
class Fib():                  #定义类Fib
    def __init__(self,start=0,step=1):
        self.step=step
    def __getitem__(self, key): #定性__getitem__函数，key为类Fib的键
            a = key+self.step
            return a          #当按照键取值时，返回的值为a

s=Fib()
s[1]  #返回2 ，因为类有 __getitem__方法，所以可以直接通过键来取对应的值
```

###### \__setitem__

> __setitem__(self,key,value)方法应该以与键相关联的方式存储值，以便之后能够使用__setitem__来获取。当然，这个对象可变时才需要实现这个方法。

```python
class Tag:
    def __init__(self):
        self.change={'python':'This is python',
                     'php':'PHP is a good language'}
 
    def __getitem__(self, item):
        print('调用getitem')
        return self.change[item]
 
    def __setitem__(self, key, value):
        print('调用setitem')
        self.change[key]=value
 
a=Tag()
print(a['php'])
a['php']='PHP is not a good language'
print(a['php'])

"""
输出：

调用getitem
PHP is a good language
调用setitem
调用getitem
PHP is not a good language
"""
```

###### \__delitem__

> 这个方法在对对象的组成部分使用__del__语句的时候被调用，应删除与key相关联的值。同样，仅当对象可变的时候，才需要实现这个方法。

```python
class Tag:
    def __init__(self):
        self.change={'python':'This is python',
                     'php':'PHP is a good language'}
 
    def __getitem__(self, item):
        print('调用getitem')
        return self.change[item]
 
    def __setitem__(self, key, value):
        print('调用setitem')
        self.change[key]=value
 
    def __delitem__(self, key):
        print('调用delitem')
        del self.change[key]
 
a=Tag()
print(a['php'])
del a['php']
print(a.change)

"""
输出：

调用getitem
PHP is a good language
调用delitem
{'python': 'This is python'}
"""
```

###### \__contians__

> 判断元素是否在序列中

```python
class BeiMenChuiXue:
    def __init__(self, name):
        self.name = name
 
    def __contains__(self, item):
        return item in self.name
 
 
if __name__ == '__main__':
    name = BeiMenChuiXue("beimenchuixue")
    print('bei' in name)
```

###### \__ iter\__函数和\_\_next\_\_函数

- 在python中实现了\__iter__方法的对象是可迭代的，实现了next()方法的对象是迭代器
- \__iter__()方法返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的next()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环。
- 容器是用来储存元素的一种数据结构，容器将所有数据保存在**内存**中

```python
"""
	for … in… 这个语句其实做了两件事:
	1. 第一件事是获得一个可迭代器，即调用了__iter__()函数。 
	2. 第二件事是循环的过程，循环调用__next__()函数。
	
	对于test这个类来说，它定义了__iter__和__next__函数，所以是一个可迭代的类，也可以说是一个可迭代的对象（Python中一切皆对象）。
"""
class test():
    def __init__(self,data=1):
        self.data = data

    def __iter__(self):
        return self
    def __next__(self):
        if self.data > 5:
            raise StopIteration
        else:
            self.data+=1
            return self.data

for item in test(3):
    print(item)
```

- 含有__next__()函数的对象都是一个迭代器，所以test也可以说是一个迭代器。如果去掉__itet__()函数，test这个类也不会报错。

```python
class test():
    def __init__(self,data=1):
        self.data = data

    def __next__(self):
        if self.data > 5:
            raise StopIteration
        else:
            self.data+=1
            return self.data

t = test(3)   
for i in range(3):
    print(t.__next__())
```

- 生成器是一种特殊的迭代器。当调用fib()函数时，生成器实例化并返回，这时并不会执行任何代码，生成器处于空闲状态，注意这里prev, curr = 0, 1并未执行。然后这个生成器被包含在list()中，list会根据传进来的参数生成一个列表，所以它对fib()对象(一切皆对象，函数也是对象)调用__next__方法。

```python
def fib(end = 1000):
    prev,curr=0,1
    while curr < end:
        yield curr
        prev,curr=curr,curr+prev

print(list(fib()))
```

###### \__init__

> __init__()方法，在创建一个对象时默认被调用，不需要手动调用
> __init__(self)中的self参数，不需要开发者传递，python解释器会自动把当前的对象引用传递过去
>
> 在类内部获取 属性 和 实例方法，通过self获取；
> 在类外部获取 属性 和 实例方法，通过对象名获取。
>
> 如果一个类有多个对象，每个对象的属性是各自保存的，都有各自独立的地址；
> 但是实例方法是所有对象共享的，只占用一份内存空间。类会通过self来判断是哪个对象调用了实例方法。

> 在实例 (通过 [`__new__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__)) 被创建之后，返回调用者之前调用。其参数与传递给类构造器表达式的参数相同。一个基类如果有 [`__init__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__init__) 方法，则其所派生的类如果也有 [`__init__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__init__) 方法，就必须显式地调用它以确保实例基类部分的正确初始化；例如: `super().__init__([args...])`.
>
> 因为对象是由 [`__new__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__) 和 [`__init__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__init__) 协作构造完成的 (由 [`__new__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__) 创建，并由 [`__init__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__init__) 定制)，所以 [`__init__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__init__) 返回的值只能是 `None`，否则会在运行时引发 [`TypeError`](https://docs.python.org/zh-cn/3/library/exceptions.html#TypeError)。

```python
class Cat:
    - 创建init方法      参数
    def __init__(self, name, age):
        self.name = name（增加实例）
        self.age = age

    def __str__(self):   - 对init方法调用
        return "%s的年龄%d" % (self.name, self.age)
        
    def sing(self):  - 创建方法
        print("猫在唱歌")
    def dance(self):
        print("猫在跳舞")

tom = Cat("老王的猫", 40)  - 创建对象
tom.sing()   - 调用对象中的方法
tom.dance()
print(tom)
```

###### \__new__

> 调用以创建一个 *cls* 类的新实例。[`__new__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__) 是一个静态方法 (因为是特例所以你不需要显式地声明)，它会将所请求实例所属的类作为第一个参数。其余的参数会被传递给对象构造器表达式 (对类的调用)。[`__new__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__) 的返回值应为新对象实例 (通常是 *cls* 的实例)。
>
> 典型的实现会附带适宜的参数使用 `super().__new__(cls[, ...])`，通过超类的 [`__new__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__) 方法来创建一个类的新实例，然后根据需要修改新创建的实例再将其返回。
>
> 如果 [`__new__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__) 未返回一个 *cls* 的实例，则新实例的 [`__init__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__init__) 方法就不会被执行。
>
> [`__new__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__) 的目的主要是允许不可变类型的子类 (例如 int, str 或 tuple) 定制实例创建过程。它也常会在自定义元类中被重载以便定制类创建过程。

###### \_\_enter\_\_、\_\_exit\_\_

```python
#上下文管理协议；
#之前说过文件的open，可以使用  with  open()  as f  :
#其实，这个就是利用了上下文管理协议；上下文管理协议的本质，就是__enter__()、__exit__()两个方法的触发；
class Foo:
    def __init__(self,filename):
        self.filename=filename
 
    def __enter__(self):
        print("执行__enter__()")
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("执行__exit__()")
        print(exc_type)
        print(exc_val)
        print(exc_tb)#上面三个参数的打印只是为了看参数的值；
                    # 当with ...  as...代码块没有异常时，这三个参数为None;
                    #当with ...  as...代码块有异常时，这三个参数分别有对应的值（可运行代码查看值的详情）
        return True  #返回值True,会吞掉with ...  as...代码块的异常，并且结束代码块运行，但是代码块之外的代码要继续运行
                        #若，没有返回值、或者返回值不为True,一遇到with ...  as...代码块的异常，
                        # 会立即抛出异常，结束所有代码的运行，包括代码块之外的代码
 
 
 
if __name__ == '__main__':
    with  Foo("test.txt")  as  f:
        print("1")
        print(b)
        print("3")
    print("4")
```

###### \__getattr__

> 兜底函数\__getattr__，当我们访问一个不存在的属性的时候，会抛出异常，提示我们不存在这个属性。访问一个不存在的属性的最后落脚点，作为异常抛出的地方提示出错。

```python
class A(object):
    def __init__(self, value):
        self.value = value
 
    def __getattr__(self, item):
        print "into __getattr__"
        return  "can not find"
 
a = A(10)
print a.value
# 10
print a.name
# into __getattr__
# can not find
```

###### \__setattr__

> 在对一个属性设置值的时候，会调用到这个函数，每个设置值的方式都会进入这个方法。

```python
class A(object):
    def __init__(self, value):
        print("into __init__")
        self.value = value

    def __setattr__(self, name, value):
        print("into __setattr__")
        if value == 10:
            print("from __init__")
        object.__setattr__(self, name, value)


a = A(10)
print(a.value)
# into __init__
# into __setattr__
# from __init__
# 10

a.value = 100
print(a.value)
# into __setattr__
# 100
```

- 重写\__setattr__避开循环。

```python
class A(object):
    def __init__(self, value):
        self.value = value
 
    def __setattr__(self, name, value):
        self.__dict__[name] = value
 
 
a = A(10)
print a.value
# 10
```

- 重写\__setattr__方法的时候千万不要重复调用造成死循环。

```python
class A(object):
    def __init__(self, value):
        self.value = value
 
    def __setattr__(self, name, value):
        self.name = value
```

###### \__delattr__

> \__delattr__是个删除属性的方法

```python
class A(object):
    def __init__(self, value):
        self.value = value
 
    def __delattr__(self, item):
        object.__delattr__(self, item)
 
    def __getattr__(self, item):
        return "when can not find attribute into __getattr__"
 
 
 
a = A(10)
print a.value
# 10
del a.value
print a.value
# when can not find attribute into __getattr__
```

###### \__dict__

> __dict__ 是类的内置属性，用于以字典的形式存储类里的属性，也就是存储那些 self.xxx 的属性

```python
class People(object):
    def __init__(self):
        self.name = 'Tom'
        self.age = 23

obj = People()
print obj.__dict__

# {'age': 23, 'name': 'Tom'}
```

###### \__iadd__（+=）

> += 背后的特殊方法是 \__iadd__ （用于“就地加法”）。但是如果一个类没有实现这个方法的话，Python 会退一步调用 \_\_add__

###### \__doc__

> 将文档写在程序里，是LISP中的一个特色，Python也借鉴过。每个函数都是一个对象，每个函数对象都是有一个\_\_doc\_\_的属性，函数语句中，如果第一个表达式是一个string，这个函数的\_\_doc\_\_就是这个string，否则\_\_doc\_\_是None。

###### \__call__

> 允许一个类的实例像函数一样被调用。实质上说，这意味着 x() 与 x.\_\_call\_\_() 是相同的。注意 \_\_call\_\_ 参数可变。这意味着你可以定义 \_\_call\_\_ 为其他你想要的函数，无论有多少个参数。

###### \__code__

###### \__closure__

###### \__name__

###### \__defaults__

###### \__bytes__

> bytes() 函数调用它获取对象的字节序列表示形式

###### \__slots__

###### \__mro__

###### \__subclasshook__

> 作用是让抽象基类识别没有注册为子类的类，你可以根据需要做简单的或者复杂的测试——标准库的做法只是检查方法名称。

###### \__missing__

###### \__next__

> 返回下一个可用的元素

###### \__dir__

###### \__all__

> 定义列表\_\_all\_\_，只有在\_\_all\_\_中的名称才能通过*导入





###### reversed()

> 实现反向迭代序列中的元素(字符串、列表、元组序列)

- 对象实现了`__reversed__()`特殊方法

###### len()

> 返回容器中元素的个数

- 背后是调用的object.\__len__方法的结果

###### bool()

> 判断对象（object）的真假，并返回True或False

- 背后是调用的object.\__bool__方法的结果
- 如果不存在 \_\_bool\_\_ 方法，那么 bool(x) 会尝试调用 x.\__len__()。若返回 0，则 bool 会返回 False；否则返回True。

###### abs()

> abs()函数可返回一个数的绝对值，()中参数可以是整数或浮点数，如果参数是复数，则返回这个复数的模

- 背后是调用的object.\__abs__方法的结果

##### dir()

> 内置的 dir() 函数能够返回由对象所定义的名称列表。

- 如果这一对象是一个模块，则该列表会包括函数内所定义的函数、类与变量。该函数接受参数。
- 如果参数是模块名称，函数将返回这一指定模块的名称列表。
- 如果没有提供参数，函数将返回当前模块的名称列表。

```python
# operator 模块中定义的部分函数（省略了以 _ 开头的名称，因为它们基本上是实现细节）
[name for name in dir(operator) if not name.startswith('_')]

"""
['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains','countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt','iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imod', 'imul','index', 'indexOf', 'inv', 'invert', 'ior', 'ipow', 'irshift','is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le','length_hint', 'lshift', 'lt', 'methodcaller', 'mod', 'mul', 'ne','neg', 'not_', 'or_', 'pos', 'pow', 'rshift', 'setitem', 'sub','truediv', 'truth', 'xor']
"""
```

##### type()

> `type()`函数用于获取对象的类型。

##### isinstance() 

> 用来判断一个函数是否是一个已知的类型

- isinstance(object,classinfo)
  - object : 实例对象。
  - classinfo : 可以是直接或者间接类名、基本类型或者由它们组成的元组。
  - 返回值：如果对象的类型与参数二的类型（classinfo）相同则返回 True，否则返回 False。
- isinstance()与type()的区别
  - isinstance() 会认为子类是一种父类类型，考虑继承关系。
  - type() 不会认为子类是一种父类类型，不考虑继承关系。

##### sample(序列a, n)

> 从序列a中随机抽取n个元素，并将n个元素生以list形式返回。

##### shuffle()

> 打乱序列里面的元素，并随机排列

```python
import random
random.shuffle(alist)
```

##### enumerate()

> 用来遍历一个集合对象，它在遍历的同时还可以得到当前元素的索引位置。

- enumerate()函数中接受一个可选参数，该参数允许你为本次循环中的计数器变量设置初始值

##### nametuple()

> 用以构建只有少数属性但是没有方法的对象

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])
ranks = [str(n) for n in range(2, 11)] + list('JQKA')
suits = 'spades diamonds clubs hearts'.split()
cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
```

##### bisect

- 在有序序列中用 bisect 查找某个元素的插入位置

```python
import bisect
import sys

HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]
ROW_FMT = '{0:2d} @ {1:2d} {2}{0:<2d}'


def demo(bisect_fn):
    for needle in reversed(NEEDLES):
        position = bisect_fn(HAYSTACK, needle)
        offset = position * ' |'
        print(ROW_FMT.format(needle, position, offset))


if __name__ == '__main__':
    if sys.argv[-1] == 'left':
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect
        print('DEMO:', bisect_fn.__name__)
        print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
        demo(bisect_fn)
        
"""
DEMO: bisect
haystack ->  1  4  5  6  8 12 15 20 21 23 23 26 29 30
31 @ 14  | | | | | | | | | | | | | |31
30 @ 14  | | | | | | | | | | | | | |30
29 @ 13  | | | | | | | | | | | | |29
23 @ 11  | | | | | | | | | | |23
22 @  9  | | | | | | | | |22
10 @  5  | | | | |10
 8 @  5  | | | | |8 
 5 @  3  | | |5 
 2 @  1  |2 
 1 @  1  |1 
 0 @  0 0 
"""
```

##### MappingProxyType

> 如果给这个类一个映射，它会返回一个只读的映射视图。虽然是个只读视图，但是它是动态的。这意味着如果对原映射做出了改动，我们通过这个视图可以观察到，但是无法通过这个视图对原映射做出修改。

```python
from types import MappingProxyType

d = {1:'A'}
d_proxy = MappingProxyType(d)
d_proxy	# mappingproxy({1: 'A'})
d_proxy[1] # 'A'
d[2] = 'B'
d_proxy # mappingproxy({1: 'A', 2: 'B'})
d_proxy[2] # 'B'
```

##### all()

> all(iterable) 如果 iterable 的每个元素都是真值，返回 True；all([]) 返回True。

##### any()

> any(iterable) 只要 iterable 中有元素是真值，就返回 True；any([]) 返回False。

##### callable()

> callable() 函数用于检查一个对象是否是可调用的。如果返回True，object仍然可能调用失败；但如果返回False，调用对象ojbect绝对不会成功.对于函数, 方法, lambda 函式, 类, 以及实现了 **call** 方法的类实例, 它都返回 True。

```python
[callable(obj) for obj in (abs, str, 13)]
# [True, True, False]
```

##### itemgetter

> 根据元组的某个字段给元组列表排序

- 使用 itemgetter 排序一个元组列表

  ```
  >>> metro_data = [
  ... ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
  ... ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
  ... ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
  ... ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
  ... ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
  ... ]
  >>>
  >>> from operator import itemgetter
  >>> for city in sorted(metro_data, key=itemgetter(1)):
  ... print(city)
  ...
  ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833))
  ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889))
  ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
  ('Mexico City', 'MX', 20.142, (19.433333, -99.133333))
  ('New York-Newark', 'US', 20.104, (40.808611, -74.020386))
  ```

- 把多个参数传给 itemgetter，它构建的函数会返回提取的值构成的元组：

  ```
  >>> cc_name = itemgetter(1, 0)
  >>> for city in metro_data:
  ... print(cc_name(city))
  ...
  ('JP', 'Tokyo')
  ('IN', 'Delhi NCR')
  ('MX', 'Mexico City')
  ('US', 'New York-Newark')
  ('BR', 'Sao Paulo')
  ```

- itemgetter 使用 [] 运算符，因此它不仅支持序列，还支持映射和任何实现 \__getitem__ 方法的类。

##### attrgetter

- 它创建的函数根据名称提取对象的属性
- 如果把多个属性名传给 attrgetter，它也会返回提取的值构成的元组

##### dis

> dis 模块为反汇编 Python 函数字节码提供了简单的方式

##### zip

```python
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

#### object

- ```python
  def __delattr__(self, *args, **kwargs):
  ```

- ```python
  def __dir__(self):
  ```

- ```python
  def __eq__(self, *args, **kwargs):
  ```

- ```python
  def __format__(self, *args, **kwargs):
  ```

- ```python
  def __getattribute__(self, *args, **kwargs):
  ```

- ```python
  def __ge__(self, *args, **kwargs):
  ```

- ```python
  def __gt__(self, *args, **kwargs):
  ```

- ```python
  def __hash__(self, *args, **kwargs):
  ```

- ```python
  def __init_subclass__(self, *args, **kwargs):
  ```

- ```python
  def __init__(self):
  ```

- ```python
  def __le__(self, *args, **kwargs):
  ```

- ```python
  def __lt__(self, *args, **kwargs):
  ```

- ```python
  def __new__(cls, *more):
  ```

- ```python
  def __ne__(self, *args, **kwargs):
  ```

- ```python
  def __reduce_ex__(self, *args, **kwargs):
  ```

- ```python
  def __reduce__(self, *args, **kwargs):
  ```

- ```python
  def __repr__(self, *args, **kwargs):
  ```

- ```python
  def __setattr__(self, *args, **kwargs):
  ```

- ```python
  def __sizeof__(self):
  ```

- ```python
  def __str__(self, *args, **kwargs):
  ```

- ```python
  def __subclasshook__(cls, subclass):
  ```

#### int

- ```python
  def bit_length(self):
  ```

- ```python
  def conjugate(self, *args, **kwargs):
  ```

- ```python
  def from_bytes(cls, bytes, byteorder, *args, **kwargs):
  ```

- ```python
  def to_bytes(self, length, byteorder, *args, **kwargs):
  ```

- ```python
  def __abs__(self, *args, **kwargs):
  ```

- ```python
  def __add__(self, *args, **kwargs):
  ```

- ```python
  def __and__(self, *args, **kwargs):
  ```

- ```python
  def __bool__(self, *args, **kwargs):
  ```

- ```python
  def __ceil__(self, *args, **kwargs):
  ```

- ```python
  def __divmod__(self, *args, **kwargs):
  ```

- ```python
  def __eq__(self, *args, **kwargs):
  ```

- ```python
  def __float__(self, *args, **kwargs):
  ```

- ```python
  def __floordiv__(self, *args, **kwargs):
  ```

- ```python
  def __floor__(self, *args, **kwargs):
  ```

- ```python
  def __format__(self, *args, **kwargs):
  ```

- ```python
  def __getattribute__(self, *args, **kwargs):
  ```

- ```python
  def __getnewargs__(self, *args, **kwargs):
  ```

- ```python
  def __ge__(self, *args, **kwargs):
  ```

- ```python
  def __gt__(self, *args, **kwargs):
  ```

- ```python
  def __hash__(self, *args, **kwargs):
  ```

- ```python
  def __index__(self, *args, **kwargs):
  ```

- ```python
  def __init__(self, x, base=10):
  ```

- ```python
  def __int__(self, *args, **kwargs):
  ```

- ```python
  def __invert__(self, *args, **kwargs):
  ```

- ```python
  def __le__(self, *args, **kwargs):
  ```

- ```python
  def __lshift__(self, *args, **kwargs):
  ```

- ```python
  def __lt__(self, *args, **kwargs):
  ```

- ```python
  def __mod__(self, *args, **kwargs):
  ```

- ```python
  def __mul__(self, *args, **kwargs):
  ```

- ```python
  def __neg__(self, *args, **kwargs):
  ```

- ```python
  def __new__(*args, **kwargs):
  ```

- ```python
  def __ne__(self, *args, **kwargs):
  ```

- ```python
  def __or__(self, *args, **kwargs):
  ```

- ```python
  def __pos__(self, *args, **kwargs):
  ```

- ```python
  def __pow__(self, *args, **kwargs):
  ```

- ```python
  def __radd__(self, *args, **kwargs):
  ```

- ```python
  def __rand__(self, *args, **kwargs):
  ```

- ```python
  def __rand__(self, *args, **kwargs):
  ```

- ```python
  def __rdivmod__(self, *args, **kwargs):
  ```

- ```python
  def __repr__(self, *args, **kwargs):
  ```

- ```python
  def __rfloordiv__(self, *args, **kwargs):
  ```

- ```python
  def __rlshift__(self, *args, **kwargs):
  ```

- ```python
  def __rmod__(self, *args, **kwargs):
  ```

- ```python
  def __rmul__(self, *args, **kwargs):
  ```

- ```python
  def __ror__(self, *args, **kwargs):
  ```

- ```python
  def __round__(self, *args, **kwargs):
  ```

- ```python
  def __rpow__(self, *args, **kwargs):
  ```

- ```python
  def __rrshift__(self, *args, **kwargs):
  ```

- ```python
  def __rshift__(self, *args, **kwargs):
  ```

- ```python
  def __rsub__(self, *args, **kwargs):
  ```

- ```python
  def __rtruediv__(self, *args, **kwargs):
  ```

- ```python
  def __rxor__(self, *args, **kwargs):
  ```

- ```python
  def __sizeof__(self, *args, **kwargs):
  ```

- ```python
  def __str__(self, *args, **kwargs):
  ```

- ```python
  def __sub__(self, *args, **kwargs):
  ```

- ```python
  def __truediv__(self, *args, **kwargs):
  ```

- ```python
  def __trunc__(self, *args, **kwargs):
  ```

- ```python
  def __xor__(self, *args, **kwargs):
  ```

#### str

- ```python
  def capitalize(self):
  ```

- ```python
  def casefold(self):
  ```

- ```python
  def center(self, width, fillchar=None):
  ```

- ```python
  def count(self, sub, start=None, end=None):
  ```

- ```python
  def encode(self, encoding='utf-8', errors='strict'):
  ```

- ```python
  def endswith(self, suffix, start=None, end=None):
  ```

- ```python
  def expandtabs(self, tabsize=8):
  ```

- ```python
  def find(self, sub, start=None, end=None):
  ```

- ```python
  def format(self, *args, **kwargs):
  ```

- ```python
  def format_map(self, mapping):
  ```

- ```python
  def index(self, sub, start=None, end=None):
  ```

- ```python
  def isalnum(self):
  ```

- ```python
  def isalpha(self):
  ```

- ```python
  def isdecimal(self):
  ```

- ```python
  def isdigit(self):
  ```

- ```python
  def isidentifier(self):
  ```

- ```python
  def islower(self):
  ```

- ```python
  def isnumeric(self):
  ```

- ```python
  def isprintable(self):
  ```

- ```python
  def isspace(self):
  ```

- ```python
  def istitle(self):
  ```

- ```python
  def isupper(self):
  ```

- ```python
  def join(self, iterable):
  ```

- ```python
  def ljust(self, width, fillchar=None):
  ```

- ```python
  def lower(self):
  ```

- ```python
  def lstrip(self, chars=None):
  ```

- ```python
  def maketrans(self, *args, **kwargs):
  ```

- ```python
  def partition(self, sep):
  ```

- ```python
  def replace(self, old, new, count=None):
  ```

- ```python
  def rfind(self, sub, start=None, end=None):
  ```

- ```python
  def rindex(self, sub, start=None, end=None):
  ```

- ```python
  def rjust(self, width, fillchar=None):
  ```

- ```python
  def rpartition(self, sep):
  ```

- ```python
  def rsplit(self, sep=None, maxsplit=-1):
  ```

- ```python
  def rstrip(self, chars=None):
  ```

- ```python
  def split(self, sep=None, maxsplit=-1):
  ```

- ```python
  def splitlines(self, keepends=None):
  ```

- ```python
  def startswith(self, prefix, start=None, end=None):
  ```

- ```python
  def strip(self, chars=None):
  ```

- ```python
  def swapcase(self):
  ```

- ```python
  def title(self):
  ```

- ```python
  def translate(self, table):
  ```

- ```python
  def upper(self):
  ```

- ```python
  def zfill(self, width):
  ```

- ```python
  def __add__(self, *args, **kwargs):
  ```

- ```python
  def __contains__(self, *args, **kwargs):
  ```

- ```python
  def __eq__(self, *args, **kwargs):
  ```

- ```python
  def __format__(self, format_spec):
  ```

- ```python
  def __getattribute__(self, *args, **kwargs):
  ```

- ```python
  def __getitem__(self, *args, **kwargs):
  ```

- ```python
  def __getnewargs__(self, *args, **kwargs):
  ```

- ```python
  def __ge__(self, *args, **kwargs):
  ```

- ```python
  def __gt__(self, *args, **kwargs):
  ```

- ```python
  def __hash__(self, *args, **kwargs):
  ```

- ```python
  def __init__(self, value='', encoding=None, errors='strict'):
  ```

- ```python
  def __iter__(self, *args, **kwargs):
  ```

- ```python
  def __len__(self, *args, **kwargs):
  ```

- ```python
  def __le__(self, *args, **kwargs):
  ```

- ```python
  def __lt__(self, *args, **kwargs):
  ```

- ```python
  def __mod__(self, *args, **kwargs):
  ```

- ```python
  def __mul__(self, *args, **kwargs):
  ```

- ```python
  def __new__(*args, **kwargs):
  ```

- ```python
  def __ne__(self, *args, **kwargs):
  ```

- ```python
  def __repr__(self, *args, **kwargs):
  ```

- ```python
  def __rmod__(self, *args, **kwargs):
  ```

- ```python
  def __rmul__(self, *args, **kwargs):
  ```

- ```python
  def __sizeof__(self):
  ```

- ```python
  def __str__(self, *args, **kwargs):
  ```

#### list

- ```python
  def append(self, p_object):
  ```

- ```python
  def clear(self):
  ```

- ```python
  def copy(self):
  ```

- ```python
  def count(self, value):
  ```

- ```python
  def extend(self, iterable):
  ```

- ```python
  def index(self, value, start=None, stop=None):
  ```

- ```python
  def insert(self, index, p_object):
  ```

- ```python
  def pop(self, index=None):
  ```

- ```python
  def remove(self, value):
  ```

- ```python
  def reverse(self):
  ```

- ```python
  def sort(self, key=None, reverse=False):
  ```

- ```python
  def __add__(self, *args, **kwargs):
  ```

- ```python
  def __contains__(self, *args, **kwargs):
  ```

- ```python
  def __delitem__(self, *args, **kwargs):
  ```

- ```python
  def __eq__(self, *args, **kwargs):
  ```

- ```python
  def __getattribute__(self, *args, **kwargs):
  ```

- ```python
  def __getitem__(self, y):
  ```

- ```python
  def __ge__(self, *args, **kwargs):
  ```

- ```python
  def __gt__(self, *args, **kwargs):
  ```

- ```python
  def __iadd__(self, *args, **kwargs):
  ```

- ```python
  def __imul__(self, *args, **kwargs):
  ```

- ```python
  def __init__(self, seq=()):
  ```

- ```python
  def __iter__(self, *args, **kwargs):
  ```

- ```python
  def __len__(self, *args, **kwargs):
  ```

- ```python
  def __le__(self, *args, **kwargs):
  ```

- ```python
  def __lt__(self, *args, **kwargs):
  ```

- ```python
  def __mul__(self, *args, **kwargs):
  ```

- ```python
  def __new__(*args, **kwargs):
  ```

- ```python
  def __ne__(self, *args, **kwargs):
  ```

- ```python
  def __repr__(self, *args, **kwargs):
  ```

- ```python
  def __reversed__(self):
  ```

- ```python
  def __rmul__(self, *args, **kwargs):
  ```

- ```python
  def __setitem__(self, *args, **kwargs):
  ```

- ```python
  def __sizeof__(self):
  ```

#### dict

- ```python
  def clear(self):
  ```

- ```python
  def copy(self):
  ```

- ```python
  def fromkeys(*args, **kwargs):
  ```

- ```python
  def get(self, k, d=None):
  ```

- ```python
  def items(self):
  ```

- ```python
  def keys(self):
  ```

- ```python
  def pop(self, k, d=None):
  ```

- ```python
  def popitem(self):
  ```

- ```python
  def setdefault(self, k, d=None):
  ```

- ```python
  def update(self, E=None, **F):
  ```

- ```python
  def values(self):
  ```

- ```python
  def __contains__(self, *args, **kwargs):
  ```

- ```python
  def __delitem__(self, *args, **kwargs):
  ```

- ```python
  def __eq__(self, *args, **kwargs):
  ```

- ```python
  def __getattribute__(self, *args, **kwargs):
  ```

- ```python
  def __getitem__(self, y):
  ```

- ```python
  def __ge__(self, *args, **kwargs):
  ```

- ```python
  def __gt__(self, *args, **kwargs):
  ```

- ```python
  def __init__(self, seq=None, **kwargs):
  ```

- ```python
  def __iter__(self, *args, **kwargs):
  ```

- ```python
  def __len__(self, *args, **kwargs):
  ```

- ```python
  def __le__(self, *args, **kwargs):
  ```

- ```python
  def __lt__(self, *args, **kwargs):
  ```

- ```python
  def __new__(*args, **kwargs):
  ```

- ```python
  def __ne__(self, *args, **kwargs):
  ```

- ```python
  def __repr__(self, *args, **kwargs):
  ```

- ```python
  def __setitem__(self, *args, **kwargs):
  ```

- ```python
  def __sizeof__(self):
  ```

#### tuple

- ```python
  def count(self, value):
  ```

- ```python
  def index(self, value, start=None, stop=None):
  ```

- ```python
  def __add__(self, *args, **kwargs):
  ```

- ```python
  def __contains__(self, *args, **kwargs):
  ```

- ```python
  def __eq__(self, *args, **kwargs):
  ```

- ```python
  def __getattribute__(self, *args, **kwargs):
  ```

- ```python
  def __getitem__(self, *args, **kwargs):
  ```

- ```python
  def __getnewargs__(self, *args, **kwargs):
  ```

- ```python
  def __ge__(self, *args, **kwargs):
  ```

- ```python
  def __gt__(self, *args, **kwargs):
  ```

- ```python
  def __hash__(self, *args, **kwargs):
  ```

- ```python
  def __init__(self, seq=()):
  ```

- ```python
  def __iter__(self, *args, **kwargs):
  ```

- ```python
  def __len__(self, *args, **kwargs):
  ```

- ```python
  def __le__(self, *args, **kwargs):
  ```

- ```python
  def __lt__(self, *args, **kwargs):
  ```

- ```python
  def __mul__(self, *args, **kwargs):
  ```

- ```python
  def __new__(*args, **kwargs):
  ```

- ```python
  def __ne__(self, *args, **kwargs):
  ```

- ```python
  def __repr__(self, *args, **kwargs):
  ```

- ```python
  def __rmul__(self, *args, **kwargs):
  ```

#### set

- ```python
  def add(self, *args, **kwargs):
  ```

- ```python
  def clear(self, *args, **kwargs):
  ```

- ```python
  def copy(self, *args, **kwargs):
  ```

- ```python
  def difference(self, *args, **kwargs):
  ```

- ```python
  def difference_update(self, *args, **kwargs):
  ```

- ```python
  def discard(self, *args, **kwargs):
  ```

- ```python
  def intersection(self, *args, **kwargs):
  ```

- ```python
  def intersection_update(self, *args, **kwargs):
  ```

- ```python
  def isdisjoint(self, *args, **kwargs):
  ```

- ```python
  def issubset(self, *args, **kwargs):
  ```

- ```python
  def issuperset(self, *args, **kwargs):
  ```

- ```python
  def pop(self, *args, **kwargs):
  ```

- ```python
  def remove(self, *args, **kwargs):
  ```

- ```python
  def symmetric_difference(self, *args, **kwargs):
  ```

- ```python
  def symmetric_difference_update(self, *args, **kwargs):
  ```

- ```python
  def union(self, *args, **kwargs):
  ```

- ```python
  def update(self, *args, **kwargs):
  ```

- ```python
  def __and__(self, *args, **kwargs):
  ```

- ```python
  def __contains__(self, y):
  ```

- ```python
  def __eq__(self, *args, **kwargs):
  ```

- ```python
  def __getattribute__(self, *args, **kwargs):
  ```

- ```python
  def __ge__(self, *args, **kwargs):
  ```

- ```python
  def __gt__(self, *args, **kwargs):
  ```

- ```python
  def __iand__(self, *args, **kwargs):
  ```

- ```python
  def __init__(self, seq=()):
  ```

- ```python
  def __ior__(self, *args, **kwargs):
  ```

- ```python
  def __isub__(self, *args, **kwargs):
  ```

- ```python
  def __iter__(self, *args, **kwargs):
  ```

- ```python
  def __ixor__(self, *args, **kwargs):
  ```

- ```python
  def __len__(self, *args, **kwargs):
  ```

- ```python
  def __le__(self, *args, **kwargs):
  ```

- ```python
  def __lt__(self, *args, **kwargs):
  ```

- ```python
  def __new__(*args, **kwargs):
  ```

- ```python
  def __ne__(self, *args, **kwargs):
  ```

- ```python
  def __or__(self, *args, **kwargs):
  ```

- ```python
  def __rand__(self, *args, **kwargs):
  ```

- ```python
  def __reduce__(self, *args, **kwargs):
  ```

- ```python
  def __repr__(self, *args, **kwargs):
  ```

- ```python
  def __ror__(self, *args, **kwargs):
  ```

- ```python
  def __rsub__(self, *args, **kwargs):
  ```

- ```python
  def __rxor__(self, *args, **kwargs):
  ```

- ```python
  def __sizeof__(self):
  ```

- ```python
  def __sub__(self, *args, **kwargs):
  ```

- ```python
  def __xor__(self, *args, **kwargs):
  ```

#### builtins

- ```python
  def abs(*args, **kwargs):
  ```

- ```python
  def all(*args, **kwargs):
  ```

- ```python
  def any(*args, **kwargs):
  ```

- ```python
  def ascii(*args, **kwargs):
  ```

- ```python
  def bin(*args, **kwargs):
  ```

- ```python
  def callable(i_e_, some_kind_of_function):
  ```

- ```python
  def chr(*args, **kwargs):
  ```

- ```python
  def compile(*args, **kwargs):
  ```

- ```python
  def copyright(*args, **kwargs):
  ```

- ```python
  def credits(*args, **kwargs):
  ```

- ```python
  def delattr(x, y):
  ```

- ```python
  def dir(p_object=None):
  ```

- ```python
  def divmod(x, y):
  ```

- ```python
  def eval(*args, **kwargs):
  ```

- ```python
  def exec(*args, **kwargs):
  ```

- ```python
  def exit(*args, **kwargs):
  ```

- ```python
  def format(*args, **kwargs):
  ```

- ```python
  def getattr(object, name, default=None):
  ```

- ```python
  def globals(*args, **kwargs):
  ```

- ```python
  def hasattr(*args, **kwargs):
  ```

- ```python
  def hash(*args, **kwargs):
  ```

- ```python
  def help():
  ```

- ```python
  def hex(*args, **kwargs):
  ```

- ```python
  def id(*args, **kwargs):
  ```

- ```python
  def input(*args, **kwargs):
  ```

- ```python
  def isinstance(x, A_tuple):
  ```

- ```python
  def issubclass(x, A_tuple):
  ```

- ```python
  def iter(source, sentinel=None):
  ```

- ```python
  def len(*args, **kwargs):
  ```

- ```python
  def license(*args, **kwargs):
  ```

- ```python
  def locals(*args, **kwargs):
  ```

- ```python
  def max(*args, key=None):
  ```

- ```python
  def min(*args, key=None):
  ```

- ```python
  def next(iterator, default=None):
  ```

- ```python
  def oct(*args, **kwargs):
  ```

- ```python
  def open(file, mode='r', buffering=None, encoding=None, errors=None, newline=None, closefd=True):
  ```

- ```python
  def ord(*args, **kwargs):
  ```

- ```python
  def pow(*args, **kwargs):
  ```

- ```python
  def print(self, *args, sep=' ', end='\n', file=None):
  ```

- ```python
  def quit(*args, **kwargs):
  ```

- ```python
  def repr(obj):
  ```

- ```python
  def round(number, ndigits=None):
  ```

- ```python
  def setattr(x, y, v):
  ```

- ```python
  def sorted(*args, **kwargs):
  ```

- ```python
  def sum(*args, **kwargs):
  ```

- ```python
  def vars(p_object=None):
  ```

- ```python
  class object:
  ```

- ```python
  class BaseException(object):
  ```

- ```python
  class Exception(BaseException):
  ```

- ```python
  class ArithmeticError(Exception):
  ```

- ```python
  class AssertionError(Exception):
  ```

- ```python
  class AttributeError(Exception):
  ```

- ```python
  class WindowsError(Exception):
  ```

- ```python
  class BlockingIOError(OSError):
  ```

- ```python
  class int(object):
  ```

- ```python
  class bool(int):
  ```

- ```python
  class ConnectionError(OSError):
  ```

- ```python
  class BrokenPipeError(ConnectionError):
  ```

- ```python
  class BufferError(Exception):
  ```

- ```python
  class bytearray(object):
  ```

- ```python
  class bytes(object):
  ```

- ```python
  class Warning(Exception):
  ```

- ```python
  class BytesWarning(Warning):
  ```

- ```python
  class ChildProcessError(OSError):
  ```

- ```python
  class classmethod(object):
  ```

- ```python
  class complex(object):
  ```

- ```python
  class ConnectionAbortedError(ConnectionError):
  ```

- ```python
  class ConnectionRefusedError(ConnectionError):
  ```

- ```python
  class ConnectionResetError(ConnectionError):
  ```

- ```python
  class DeprecationWarning(Warning):
  ```

- ```python
  class dict(object):
  ```

- ```python
  class enumerate(object):
  ```

- ```python
  class EOFError(Exception):
  ```

- ```python
  class FileExistsError(OSError):
  ```

- ```python
  class FileNotFoundError(OSError):
  ```

- ```python
  class filter(object):
  ```

- ```python
  class float(object):
  ```

- ```python
  class FloatingPointError(ArithmeticError):
  ```

- ```python
  class frozenset(object):
  ```

- ```python
  class FutureWarning(Warning):
  ```

- ```python
  class GeneratorExit(BaseException):
  ```

- ```python
  class ImportError(Exception):
  ```

- ```python
  class ImportWarning(Warning):
  ```

- ```python
  class SyntaxError(Exception):
  ```

- ```python
  class IndentationError(SyntaxError):
  ```

- ```python
  class LookupError(Exception):
  ```

- ```python
  class IndexError(LookupError):
  ```

- ```python
  class InterruptedError(OSError):
  ```

- ```python
  class IsADirectoryError(OSError):
  ```

- ```python
  class KeyboardInterrupt(BaseException):
  ```

- ```python
  class KeyError(LookupError):
  ```

- ```python
  class list(object):
  ```

- ```python
  class map(object):
  ```

- ```python
  class MemoryError(Exception):
  ```

- ```python
  class memoryview(object):
  ```

- ```python
  class ModuleNotFoundError(ImportError):
  ```

- ```python
  class NameError(Exception):
  ```

- ```python
  class NotADirectoryError(OSError):
  ```

- ```python
  class RuntimeError(Exception):
  ```

- ```python
  class NotImplementedError(RuntimeError):
  ```

- ```python
  class OverflowError(ArithmeticError):
  ```

- ```python
  class PendingDeprecationWarning(Warning):
  ```

- ```python
  class PermissionError(OSError):
  ```

- ```python
  class ProcessLookupError(OSError):
  ```

- ```python
  class property(object):
  ```

- ```python
  class range(object):
  ```

- ```python
  class RecursionError(RuntimeError):
  ```

- ```python
  class ReferenceError(Exception):
  ```

- ```python
  class ResourceWarning(Warning):
  ```

- ```python
  class reversed(object):
  ```

- ```python
  class RuntimeWarning(Warning):
  ```

- ```python
  class set(object):
  ```

- ```python
  class slice(object):
  ```

- ```python
  class staticmethod(object):
  ```

- ```python
  class StopAsyncIteration(Exception):
  ```

- ```python
  class StopIteration(Exception):
  ```

- ```python
  class str(object):
  ```

- ```python
  class super(object):
  ```

- ```python
  class SyntaxWarning(Warning):
  ```

- ```python
  class SystemError(Exception):
  ```

- ```python
  class SystemExit(BaseException):
  ```

- ```python
  class TabError(IndentationError):
  ```

- ```python
  class TimeoutError(OSError):
  ```

- ```python
  class tuple(object):
  ```

- ```python
  class type(object):
  ```

- ```python
  class TypeError(Exception):
  ```

- ```python
  class UnboundLocalError(NameError):
  ```

- ```python
  class ValueError(Exception):
  ```

- ```python
  class UnicodeError(ValueError):
  ```

- ```python
  class UnicodeDecodeError(UnicodeError):
  ```

- ```python
  class UnicodeEncodeError(UnicodeError):
  ```

- ```python
  class UnicodeTranslateError(UnicodeError):
  ```

- ```python
  class UnicodeWarning(Warning):
  ```

- ```python
  class UserWarning(Warning):
  ```

- ```python
  class ZeroDivisionError(ArithmeticError):
  ```

- ```python
  class zip(object):
  ```

#### collections

- ```python
  class deque(object):
  ```

- ```python
  class defaultdict(dict):
  ```

- ```python
  def namedtuple(typename, field_names, *, verbose=False, rename=False, module=None):
  ```

- ```python
  class UserDict(MutableMapping):
  ```

- ```python
  class UserList(MutableSequence):
  ```

- ```python
  class UserString(Sequence):
  ```

- ```python
  class Counter(dict):
  ```

- ```python
  class OrderedDict(dict):
  ```

- ```python
  class ChainMap(MutableMapping):
  ```

#### functools

- ```python
  def update_wrapper(wrapper,
                     wrapped,
                     assigned = WRAPPER_ASSIGNMENTS,
                     updated = WRAPPER_UPDATES):
  ```

- ```python
  def wraps(wrapped,
            assigned = WRAPPER_ASSIGNMENTS,
            updated = WRAPPER_UPDATES):
  ```

- ```python
  def total_ordering(cls):
  ```

- ```python
  def cmp_to_key(mycmp):
  def cmp_to_key(*args, **kwargs):
  ```

- ```python
  def lru_cache(maxsize=128, typed=False):
  ```

- ```python
  def reduce(function, sequence, initial=None):
  ```

- ```python
  class partial:
  ```

- ```python
  class partialmethod(object):
  ```

- ```python
  def singledispatch(func):
  ```

#### itertools

- ```python
  class accumulate(object):
  ```

- ```python
  class chain(object):
  ```

- ```python
  class combinations(object):
  ```

- ```python
  class combinations_with_replacement(object):
  ```

- ```python
  class compress(object):
  ```

- ```python
  class count(object):
  ```

- ```python
  class cycle(object):
  ```

- ```python
  class dropwhile(object):
  ```

- ```python
  class filterfalse(object):
  ```

- ```python
  class groupby(object):
  ```

- ```python
  class islice(object):
  ```

- ```python
  class permutations(object):
  ```

- ```python
  class product(object):
  ```

- ```python
  class repeat(object):
  ```

- ```python
  class starmap(object):
  ```

- ```python
  class takewhile(object):
  ```

- ```python
  class zip_longest(object):
  ```

#### Python中带下划线_的变量和函数命名

###### 前后均带有双下划线__的命名

> 一般用于特殊方法的命名，用来实现对象的一些行为或者功能。

###### 仅开头带双下划线__的命名

> 用于对象的数据封装，以此命名的属性或者方法为类的私有属性或者私有方法。
>
> Python 管理这些名称，它用于避免名称与子类定义的名称冲突。
>
> 所有以双下划线开头的名称\_\_name都会自动变为"_类名__name"的新名称。

- 私有函数不可以从它们的模块外面被调用
- 私有类方法不能够从它们的类外面被调用
- 私有属性不能够从它们的类外面被访问

###### 以单下划线_开头的命名

> 一般用于模块中的"私有"定义的命名。
>
> 名称前的单个下划线用于指定程序员将名称视为“私有”。这可以视为一种约定，方便阅读代码的人知道以 _ 开头的名称供内部使用。
>
> 带有下划线的名称(例如 _spam)应被视为 API 的非公开部分(无论是函数、方法还是数据成员)。

- from module import * 语句用于加载模块中的所有名称，要控制导入的名称，一种方法是定义列表\_\_all\_\_，只有在\_\_all\_\_中的名称才能通过*导入;
- 另一种方法就是以单下划线开头命名定义了，这种定义不会被*导入。

- 如果是模块的私有类，还可能有一个前缀下划线(主要目的是防止可能与祖先类的类成员发生名称冲突。)

###### 单下划线

- _ 用作一次性的名称。这为了让阅读代码的人知道，这里分配了某个名称，但是不打算使用

  ```python
  for _ in range(10)
  ```

###### 名称后的单下划线(例如 total_)

> 名称后面的单个下划线用于避免名称遮盖另一个名称，当然是惯例。例如，如果你想命名某种格式，为了避免掩盖 Python 的内置格式，你可以将其命名为format_。

#### @staticmethod（静态方法）和@classmethod（类方法）使用

> 一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。
> 而使用@staticmethod或@classmethod，就可以不需要实例化，直接通过类名就可以实现调用。
> 使用：**直接类名.方法名()**来调用。
>
> 这有利于组织代码，把某些应该属于某个类的函数给放到那个类里去，同时有利于命名空间的整洁。

- @staticmethod不需要表示自身对象的self和自身类的cls参数（这两个参数都不需要添加），就跟使用函数一样。使用：**直接类名.属性名**或**直接类名.方法名**。直接类名，也可以直接类名( )

  ```python
  #直接定义一个test()函数
  def test():
      print "i am a normal method!"

  #定义一个类，其中包括一个类方法，采用@staticmethod修饰    
  class T:

      @staticmethod
      def static_test():   #没有self参数
          print "i am a static method!"

  if __name__ == "__main__":
      test()				# 1
      T.static_test()		# 2
      T().static_test()	# 3

  output:
  i am a normal method!
  i am a static method!
  i am a static method!
  ```

- @classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。使用：**直接类名.属性名**或**直接类名.方法名**，直接类名，也可以直接类名( )

  ```python
  class T:
      @classmethod
      def class_test(cls):     #必须有cls参数     #这里第一个参数是cls， 表示调用当前的类名
          print "i am a class method"
  
  if __name__ == "__main__":
      T.class_test()
      T().class_test()
  
  output:
  i am a class method
  i am a class method
  ```

####  property（特性）

- 用访问类属性的方式，直接调用类方法

  ```python
  import math
  class Circle:
      def __init__(self,radius): #圆的半径radius
          self.radius=radius

      @property
      def area(self):
          return math.pi * self.radius**2 #计算面积

      @property
      def perimeter(self):
          return 2*math.pi*self.radius #计算周长

  c=Circle(10)
  print(c.radius)
  print(c.area) #可以向访问数据属性一样去访问area,会触发一个函数的执行,动态计算出一个值
  print(c.perimeter) #同上
  '''
  输出结果:
  314.1592653589793
  62.83185307179586
  '''
  ```

- 设置属性值：

  - 被 `@property`装饰的方法是获取属性值的方法，被装饰方法的名字会被用做属性名。
  - 被 `@属性名.setter` 装饰的方法是设置属性值的方法。
  - 被 `@属性名.deleter`装饰的方法是删除属性值的方法。

  ```python
  class Student:
  
      def __init__(self):
          self._score = ''
  
      @property
      def score(self):
          return self._score
  
      @score.setter
      def score(self, value):
          if not isinstance(value, int):
              raise ValueError('分数必须是数字')
          if value > 100 or value < 0:
              raise ValueError('分数不符实际')
          self._score = value
  
      @score.deleter
      def score(self):
          del self._score
  ```


  s = Student()
  s.score = 100
  print(s.score)  # 100
  s.score = 150
  print(s.score)  # 报错
  del s.score
  print(s.score)  # 报错
  ```

- 面向对象的封装有三种方式:
  - public: 这种其实就是不封装,是对外公开的
  - protected: 这种封装方式对外不公开,但对子类公开。
  - private: 这种封装对谁都不公开

```python
class Foo:
    def __init__(self, val):
        self.__NAME = val  # 将所有的数据属性都隐藏起来

    @property
    def name(self):
        return self.__NAME  # obj.name访问的是self.__NAME(这也是真实值的存放位置)

    @name.setter
    def name(self, value):
        if not isinstance(value, str):  # 在设定值之前进行类型检查
            raise TypeError('%s must be str' % value)
        self.__NAME = value  # 通过类型检查后,将值value存放到真实的位置self.__NAME

    @name.deleter
    def name(self):
        raise TypeError('Can not delete')


f = Foo('tom')
print(f.name)
f.name = 10  # 抛出异常'TypeError: 10 must be str'
# del f.name  # 抛出异常'TypeError: Can not delete'
  ```

#### 可以直接import的模块和包(python/Lib/)

- asyncio
- collections
- concurrent
- ctypes
- curses
- dbm
- distutils
- email
- encodings
- ensurepip
- html
- http
- idlelib
- importlib
- json
- lib2to3
- logging
- msilib
- multiprocessing
- pydoc_data
- site-packages
- sqlite3
- test
- tkinter
- turtledemo
- unittest
- urllib
- venv
- wsgiref
- xml
- xmlrpc
- \__future__
- _bootlocale
- _collections_abc
- _compat_pickle
- _compression
- _dummy_thread
- _markupbase
- _osx_support
- _pydecimal
- _pyio
- _sitebuiltins
- _strptime
- _threading_local
- _weakrefset
- abc
- aifc
- antigravity
- argparse
- ast
- asynchat
- asyncore
- base64
- bdb
- binhex
- bisect
- bz2
- calendar
- cgi
- cgitb
- chunk
- cmd
- code
- codecs
- codeop
- colorsys
- compileall
- configparser
- contextlib
- copy
- copyreg
- cProfile
- crypt
- csv
- datetime
- decimal
- difflib
- dis
- doctest
- dummy_threading
- enum
- filecmp
- fileinput
- fnmatch
- formatter
- fractions
- ftplib
- functools
- genericpath
- getopt
- getpass
- gettext
- glob
- gzip
- hashlib
- heapq
- hmac
- imaplib
- imghdr
- imp
- inspect
- io
- ipaddress
- keyword
- linecache
- locale
- lzma
- macpath
- macurl2path
- mailbox
- mailcap
- mimetypes
- modulefinder
- netrc
- nntplib
- ntpath
- nturl2path
- numbers
- opcode
- operator
- optparse
- os
- pathlib
- pdb
- pickle
- pickletools
- pipes
- pkgutil
- platform
- plistlib
- poplib
- posixpath
- pprint
- profile
- pstats
- pty
- py_compile
- pyclbr
- pydoc
- queue
- quopri
- random
- re
- reprlib
- rlcompleter
- runpy
- sched
- secrets
- selectors
- shelve
- shlex
- shutil
- signal
- site
- smtpd
- smtplib
- sndhdr
- socket
- socketserver
- sre_compile
- sre_constants
- sre_parse
- ssl
- stat
- statistics
- string
- stringprep
- struct
- subprocess
- sunau
- symbol
- symtable
- sysconfig
- tabnanny
- tarfile
- telnetlib
- tempfile
- textwrap
- this
- threading
- timeit
- token
- tokenize
- trace
- traceback
- tracemalloc
- tty
- turtle
- types
- typing
- uu
- uuid
- warnings
- wave
- weakref
- webbrowser
- xdrlib
- zipapp
- zipfile