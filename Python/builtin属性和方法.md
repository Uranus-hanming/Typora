1. abs()：返回参数的绝对值

2. all(iterable)

   > 可迭代对象中的每一项的布尔值都为真时，返回True

3. any(iterable)

   > 可迭代对象中只要有一个是真时，返回True

4. bin(number)：返回整数的二进制表示形式

5. callable(object)

   > 用于检查一个对象是否是可调用的；函数、方法、lambda函数、类以及实现了\_\_call\_\_方法的类实例

6. chr(number)：返回一个字符串，该字符串表示Unicode代码点是整数的字符

7. ord(str)：返回Unicode代码点

8. compile()

   > compile()函数允许程序员在运行时刻迅速生成代码对象，然后就可以用exec 语句或者内建函数eval()来执行这些对象或者对它们进行求值。
   >
   > 一个很重要的观点是：exec 和eval()都可以执行字符串格式的Python 代码。当执行字符串形式的代码时，每次都必须对这些代码进行字节编译处理。compile()函数提供了一次性字节代码预编译，以后每次调用的时候，都不用编译了。
   > compile(source, filename, mode[, flags[, dont_inherit]])
   >
   > 第一参数代表了要编译的python 代码。
   > 第二个字符串，虽然是必需的，但通常被置为空串。mode参数是个字符串，它用来表明代码对象的类型。有三个可能值：
   > 'eval' 可求值的表达式[和eval()一起使用]
   > 'single' 单一可执行语句[和exec或eval()一起使用]
   > 'exec' 可执行语句组[和exec一起使用]

   ```python
   >>> eval_code = compile ( '100 + 200' , '' , 'eval' )
   >>> eval ( eval_code )
   300
   ```

9. delattr(object, name)

   > 用于删除对象属性。参数是一个对象和一个字符串。delattr(x, 'foo')等同于 del x.foo

   ```python
   class Dog:
     age = 1
     name = 'tom'
     sex = 'man'
     	
   dog = Dog()
   delattr(dog, 'sex')
   del dog.sex
   ```

10. setattr(x, y, x)：设置属性的值

    > setattr(x, y, v)等同于 x.y = v

11. dir(object)：返回任何对象的属性和方法的里列表

12. divmod(x, y)：返回元祖(x//y, x%y)

13. eval(expression, globals=None, locals=None)

    > eval()函数用于执行一个字符串表达式，并且返回该表达式的值。

    - **expression**：表达式，上面提到eval函数用于执行一个字符串表达式，表达式的内容就放在此处。当表达式涉及到
    - **globals**：**该部分必须是字典！必须是字典！必须是字典！**否则程序会出错。当定义了globals 参数之后eval函数的作用域会被限定在globals中。
    - **locals**：该参数掌控局部的命名空间，功能和globals类型，不过当参数冲突时，会执行locals处的参数。

    ```python
    a=10
    b=20
    c=30
    g={'a':6,'b':8}
    t={'b':100,'c':10}
    print(eval('a+b+c',g,t))
    # 116
    # 当有globals和locals时作用的范围域是在globals和locals中，所以a=10,b=20,c=30不会被应用。a和c的值分别去字典g和字典t中的值，当globals和locals中都有相同参数时取locals中的值。
    ```

14. exec(object[, globals[, locals]])

    > 与eval()主要的区别是，exec() 的第一个参数不是表达式，而是代码块，这意味着两点：一是它不能做表达式求值并返回出去，二是它可以执行复杂的代码逻辑，相对而言功能更加强大

    ```python
    x = 1
    exec('x = 1 + 1')
    print(x) # 2

    >>> a = "[[1,2], [3,4], [5,6], [7,8], [9,0]]"
    >>> print(eval(a))
    [[1, 2], [3, 4], [5, 6], [7, 8], [9, 0]]
    >>> a = "{'name': 'Python猫', 'age': 18}"
    >>> print(eval(a))
    {'name': 'Python猫', 'age': 18}
     
    # 与 eval 略有不同
    >>> a = "my_dict = {'name': 'Python猫', 'age': 18}"
    >>> exec(a)
    >>> print(my_dict)
    {'name': 'Python猫', 'age': 18}
    ```

15. format()

16. getattr(object, name, default=None)

17. globals()

18. hasattr(object, name)：判断对象是否有该属性

19. hash(object)：返回对象的哈希值

20. help()：获取指定模块，类，函数，变量等的说明文档

21. hex()：返回整数的十六进制表达式

22. id(object)：返回对象的身份identity（内存地址）

23. input()

24. isinstance()：判断一个对象是否是一个类或其子类中的实例

25. iter(iterable)：从可迭代对象中获取迭代器，然后可以使用next()获取迭代器中的元素，直至被耗尽

26. locals()

27. max(arg1, arg1,.., key=xxx)：返回最大值

28. min(arg1, arg1,.., key=xxx)：返回最小值

29. next(iterator, default)

    > 返回迭代器中的下一项，如果迭代器耗尽了，则返回默认值default

30. oct()：返回整数的八进制表达式

31. open()：打开文件并返回字节流

32. pow(base, exp, mod)

    1. pow(x, y)两个参数等同于：x ** y
    2. pow(x, y, z)三个参数等同于：x ** y % z

33. sorted(iterable, key, reverse)

34. sum(iterable)：默认从0开始累加可迭代对象中的数字

35. print()

36. round(number, x)：四舍五入，x表示保留小数点后几位

37. vars(object)：返回对象的dict属性

38. enumerate(iterable[, start])

39. map(function, iterable)

40. filter(function, iterable)

41. reduce(function, sequence)

42. float(object)

43. frozenset()：返回一个冻结的集合，冻结后集合不能再添加或删除任何元素

44. property

    ```python
    class C(object):
            @property
            def x(self):
                "I am the 'x' property."
                return self._x
            @x.setter
            def x(self, value):
                self._x = value
            @x.deleter
            def x(self):
                del self._x
    ```

45. range(start, stop[, step])

46. reversed(sequence)

47. classmethod(object)

48. staticmethod(object)

49. type(object)

50. zip(object)

    ```python
    >>> pairs = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
    >>> numbers, letters = zip(*pairs)
    >>> numbers
    (1, 2, 3, 4)
    >>> letters
    ('a', 'b', 'c', 'd')
    ```