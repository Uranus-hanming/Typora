[toc]

##### 1. int

1. \_\_xx\_\_: 
2. \_\_delattr\_\_: del xxx
3. \_\_dir\_\_: dir()
4. \_\_eq\_\_: ==
5. \_\_ge\_\_: >=
6. \_\_gt\_\_: >
7. \_\_hash\_\_: hash()
8. \_\_le\_\_: <=
9. \_\_lt\_\_: <
10. \_\_ne\_\_: !=
11. \_\_repr\_\_: 
12. \_\_setattr\_\_:  =
13. \_\_str\_\_: str()
14. \_\_abs\_\_: |n|
15. \_\_add\_\_: + add
16. \_\_sub\_\_: - subtract
17. \_\_mul\_\_: * multiply
18. \_\_truediv\_\_:  / divide
19. \_\_mod\_\_: %
20. \_\_radd\_\_: +=
21. \_\_rmul\_\_: *=
22. \_\_rmod\_\_: %=
23. \_\_rfloordiv\_\_: //=
24. \_\_xor\_\_: m^n
25. \_\_float\_\_: float()
26. \_\_floordiv\_\_: // 地板除
27. \_\_neg\_\_: -n 取反
28. \_\_ne\_\_: !=
29. \_\_and\_\_: &
30. \_\_or\_\_: |
31. \_\_index\_\_: index()
32. \_\_int\_\_: int()
33. \_\_pow\_\_: pow(m, n) = m^n
34. \_\_str\_\_: print()



##### 2. str

1. center(width, fillchar=None)

   > Python的字符串center()方法会对原字符串进行排版，通过指定一个长度值，将原字符串在该长度内居中。可以指定字符为填充字符。

   | 名称     | 说明                       | 备注                                 |
   | -------- | -------------------------- | ------------------------------------ |
   | width    | 字符串排版总宽度，整型参数 | 不可省略的参数                       |
   | fillchar | 填充字符，字符串参数       | 可省略的参数，省略时填充字符为空格符 |

2. ljust(width, fillchar=None)

   > Python的字符串center()方法会对原字符串进行排版，通过指定一个长度值，将原字符串在该长度内靠左对齐。可以指定字符为填充字符。

3. rjust(width, fillchar=None)

   > Python的字符串center()方法会对原字符串进行排版，通过指定一个长度值，将原字符串在该长度内靠右对齐。可以指定字符为填充字符。

4. string.count(sub_string, start, end)

   > count()方法返回出现在范围内串子数range [start, end]

   | 名称       | 备注                                                         | 说明                 |
   | ---------- | ------------------------------------------------------------ | -------------------- |
   | string     | 待统计的字符串                                               |                      |
   | sub_string | 希望检测的字符串。即希望检测出sub_string在string中出现的次数 | 不可省略的字符串参数 |
   | start      | string字符串开始搜索的位置                                   | 整型数字，可省略     |
   | end        | string字符串结束搜索的位置                                   | 整型数字，可省略     |

5. str.encode(encoding='UTF-8',errors='strict')

   > encode方法返回字符串编码后的数据，默认的编码是当前的字符串编码。errors为给定的不同错误处理方法。

6. endswith(suffix, start=None, end=None)

   - str：字符串，待判断字符串
   - suffix：后缀，判断字符串后缀是否是这几个后缀，可为单字符也可为多字符。
   - start：索引字符串开始序号，可选，默认为0，从第一个位置开始。
   - end：索引字符串结束序号，可选，默认为字符串长度len(str)，从最后位置结束。若填写则开始字符串也要填，start填，end可选填。

7. startswith(prefix, start=None, end=None)

8. str.expandtabs(tabsize= 8)

   - 创建一个字符串，把原字符串中的 制表符（tab 符号（'\t'））转为空格，tab 符号默认的空格数是 8。
   - 如果字符为制表符（'\t'），则会在结果中插入一个或多个空格符，直到当前列等于下一个制表位。（制表符本身不会被复制）
   - 如果字符为换行符（'\n'）或回车符（'\r'），它会被复制并将当前列重设为零。 任何其他字符会被不加修改地复制并将当前列加一，不论该字符在被打印时会如何显示。
   - tabsize —— 指定转换字符串中的制表符转为空格的字符数。

9. find(sub, start=None, end=None)

   > 用于判断查询字符串是否含有目标字符串，有则返回第一个查询到的位置序号，否则返回-1

   - str：被索引的字符串，定义某串字符串或者获取str。
   - string：目标检索的字符或者字符串。是指整个str中查找某个或者某几个字符string。
   - begin：可选择，开始遍历的序号，默认为0，即第一个值。
   - end：可选，结束的位置序号，默认为最后的位置。但是有end必须要有begin，否则会报错。

10. index(sub, start=None, end=None)

    > index()方法确定字符串str，如果起始索引beg和结束索引end在末尾给出了找到字符串或字符串的一个子串。这个方法与find()方法一样，只是如果没有找到子符趾会抛出一个异常。

11. format(*args, **kwargs)

    > format() 方法格式化指定的值，并将其插入字符串的占位符内。

12. format_map(mapping)

    > 该方法类似于 str.format(**mapping) 都可以进行字符串格式化，不同之处在于 format( ) 方法是一种所有情况都能使用的格式化方法，而 str.format_map(mapping) 方法仅适用于字符串格式中可变数据参数来源于字典等映射关系数据时。mapping 会被直接使用而不是复制到一个 dict。

    ```
    >>> a = '{who}爱{how_many}条{what}'
    >>> dict_x = {'how_many': '一', 'who': '你', 'what': 'chai'}
    >>> a.format_map(dict_x)
    '你爱一条chai'
    ```

13. s.isalnum()

    > 如果s中的字符都只含数字和字母，则返回True，否则返回False

14. str.join(sequence)

    > 将序列（列表或元组）中的元素以指定的字符连接成一个新的字符串。
    >
    > 其中，str：指定的字符
    > sequence：待连接的元素序列
    > 返回值为通过指定字符连接序列中的元素后生成的新字符串

    ```
    >>> str = '-'
    >>> seq = ('b','o','o','k')
    >>> print str.join(seq)
    >>> b-o-o-k # 输出结果
    ```

15. lower()：转小写

16. upper()：转大写

17. title()：每个单词开头大写

18. swapcase()：大小写互换

19. lstrip():删除字符串左侧空白字符

20. rstrip():删除字符串右侧空白字符

21. strip():删除字符串两侧空白字符

22. str.maketrans(intab, outtab)

    > maketrans() 方法用于创建字符映射的转换表，对于接受两个参数的最简单的调用方式，第一个参数intab是字符串，表示需要转换的字符；第二个参数outtab是字符串表示转换的目标。
    >
    > 两个字符串的长度必须相同，为一一对应的关系。

    ```python
    intab = "aeiou"
    outtab = "12345"
    trantab = str.maketrans(intab, outtab)
    str = "this is string example....wow!!!"
    print (str.translate(trantab))
    # th3s 3s str3ng 2x1mpl2....w4w!!!
    ```

23. str.partition(sign)

    > partition() 方法用来根据指定的分隔符将字符串进行分割，返回一个3元的元组，第一个为分隔符左边的子串，第二个为分隔符本身，第三个为分隔符右边的子串。

24. str.rpartition(sign)

    ```python
    str = "http://www.w3cschool.cc/"
    print(str.rpartition("ww")) # ('http://w', 'ww', '.w3cschool.cc/')
    print(str.partition("ww")) # ('http://', 'ww', 'w.w3cschool.cc/')
    ```

25. S.replace(old, new[, count])

    > 指定新的字符串替换旧的字符串，如果给出参数count数量，则按指定的数量进行替换

26. S.rfind(sub, start=None, end=None)

    > 返回sub在S中出现的最右边的索引值

27. S.rindex(sub, start=None, end=None)

28. S.split(sep=None, maxsplit=-1)

    > **sep**：        分割字符
    >                当sep为None，将以**换行符、空格符、制表符等空字符**作为分割字符，当包含多个时，多个空字符整体作为分割符
    >
    > **maxsplit**：分割次数，返回值最多包含maxsplit+1个字符
    >                当maxsplit为-1时，返回值包含（分割字符个数+1）个字符

29. str.zfill(width)

    > zfill()方法返回指定长度的字符串，原字符串右对齐，前面填充0

30. \_\_add\_\_: self+value

31. \_\_contains\_\_: key in self.

32. \_\_eq\_\_: ==

33. \_\_format\_\_: 

34. \_\_getitem\_\_: self[key]

35. \_\_ge\_\_: self>=value

36. \_\_gt\_\_: self>value

37. \_\_hash\_\_: hash(self)

38. \_\_len\_\_: len()

39. \_\_le\_\_: <=

40. \_\_lt\_\_: <

41. \_\_mod\_\_:  self%value

42. \_\_mul\_\_: self*value

43. \_\_str\_\_: str(self)



##### 3. list

1. L.append(object)：在列表后面添加一个对象

2. L.clear()：清空列表

3. L.copy()：shallow copy 浅拷贝

4. L.count(value)：返回列表中value出现的次数

5. L.extend(iterable)

   > 通过追加可迭代对象中的元素来达到扩展列表的作用

   ```python
   li = [1, 2, 3, 4, 5, 6, 7, 8, 9]
   s = 'abcd'
   print(li.extend(s))
   # [1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd']

   l2 = [1, 2, 3]
   print(li.extend(l2))
   # [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
   ```

6. L.index(value, start=None, stop=None)

   > 返回value在列表中第一次出现的索引值，如果不存在则返回错误

7. L.insert(index, object)：在index前插入object

8. L.pop(index=None)：

   > 移除列表中index对应的值，默认是最后一个；如果列表是空，或index超出范围，则抛出错误

9. L.remove(value)：移除第一个出现value的值，如果不存在则抛出错误

10. L.reverse()：反转列表

11. L.sort(key=None, reverse=False)：对列表进行排序，默认升序

12. \_\_add\_\_: +

13. \_\_contains\_\_: key in self

14. \_\_delitem\_\_: delete self[key]

15. \_\_eq\_\_: ==

16. \_\_getitem\_\_: x[y]

17. \_\_ge\_\_: >=

18. \_\_gt\_\_: >

19. \_\_iadd\_\_: +=

20. \_\_imul\_\_: *=

21. \_\_iter\_\_: 

22. \_\_len\_\_: len()

23. \_\_le\_\_: <=

24. \_\_lt\_\_: <

25. \_\_mul\_\_: *

26. \_\_ne\_\_: !=

27. \_\_repr\_\_: 

28. \_\_reversed\_\_: 

29. \_\_rmul\_\_: 

30. \_\_setitem\_\_: =

31. \_\_sezeof\_\_: 



##### 4. dict

1. D.clear()：清空字典

2. D.copy()：浅拷贝

3. dict.fromkeys(iterable, value)：将可迭代对象iterable中的元素作为key，value作为键值，返回新的字典

4. D.get(k, d)

   > 根据k获取值，如果k不存在，则返回d，d默认是None

   ```python
   d = {'a': 1, 'b': 2, 'c': 3}
   print(d.get('e', 0)) # 0
   ```

5. D.items()：以列表的形式返回可遍历的元素数组

   ```python
   d = {'a': 1, 'b': 2, 'c': 3}
   dict_items([('a', 1), ('b', 2), ('c', 3)])
   ```

6. D.keys()：返回列表中所有的键

   ```python
   d = {'a': 1, 'b': 2, 'c': 3}
   dict_keys(['a', 'b', 'c'])
   ```

7. D.values()：以列表返回字典中的所有值

   ```python
   d = {'a': 1, 'b': 2, 'c': 3}
   dict_values([1, 2, 3])
   ```

8. D.pop(k[, d])

   > 移除对应的k和值，如果k不存在则返回d，没有d则返回keyError

9. D.popitem()：不需要传入参数，随机删除一个键值对，一般删除最后一个

10. D.setdefault(k[,d])

    > 如果k在字典中则返回该键对应的值，如果不存在，则添加键值对k=d到字典D中

11. D.update()：使用另一个字典对象或可迭代的键值对中的元素更新字典

    ```python
    d = {'a': 1, 'b': 2, 'c': 3}
    du = {'a': 4, 'e': 5, 'c': 6, 'f': 7}

    print(d.update(du))
    # {'a': 4, 'b': 2, 'c': 6, 'e': 5, 'f': 7}
    d.update(b=0, c=0)
    # {'a': 4, 'b': 0, 'c': 0, 'e': 5, 'f': 7}
    ```

12. \_\_contains\_\_: in

13. \_\_delitem\_\_: delete

14. \_\_eq\_\_: ==

15. \_\_getattribute\_\_: 

16. \_\_getitem\_\_: x[y]

17. \_\_ge\_\_: >=

18. \_\_gt\_\_: >

19. \_\_iter\_\_: 

20. \_\_len\_\_: len()

21. \_\_le\_\_: <=

22. \_\_lt\_\_: <

23. \_\_ne\_\_: !=

24. \_\_repr\_\_: 

25. \_\_setitem\_\_: =

26. \_\_sizeof\_\_: 



##### 5. tuple

1. T.count(value)：返回value在元祖中的个数
2. T.index(value, start=None, stop=None)：返回第一个出现value的索引值
3. \_\_add\_\_: +
4. \_\_contains\_\_: in
5. \_\_eq\_\_: ==
6. \_\_getattribute\_\_: 
7. \_\_getitem\_\_: self[key]
8. \_\_ge\_\_: >=
9. \_\_gt\_\_: >
10. \_\_hash\_\_: hash()
11. \_\_iter\_\_: 
12. \_\_len\_\_: len()
13. \_\_le\_\_: <=
14. \_\_lt\_\_: <
15. \_\_mul\_\_: *
16. \_\_ne\_\_: !=
17. \_\_repr\_\_: 



##### 6. set

1. add(*args, **kwargs)：添加元素

2. clear()：清空集合

3. copy()：浅拷贝

4. difference()：返回两个或多个集合中不同的集合，并生成新的集合

   ```python
   A = {2, 3, 4, 5}
   B = {3, 4}
   C = {2}
   n = A.difference(B, C)
   print(n)
   # {5}
   ```

5. difference_update()：将当前集合中包含的其他集合的元素都移除掉

   ```python
   A = {2, 3, 4, 5}
   B = {3, 4}
   A.difference_update(B)
   print(A)
   # {2, 5}
   ```

6. discard(value)：将value从集合中移除掉

7. intersection()：返回交集

8. intersection_update()：将集合更新为交集

   ```python
   A = {2, 3, 4, 5}
   B = {3, 4, 6, 8}
   A.intersection_update(B)
   print(A)
   # {3, 4}
   ```

9. A.isdisjoint(B)：判断A和B的交集是否为空

10. A.issubset(B)：判断A是否为B的子集

11. A.isuperset(B)：判断集合A是否包含集合B

12. pop()：从集合中删除一个元素

13. remove(element)：从集合中移除指定的元素

14. A.symmetric_difference(B)：返回集合A和集合B的差集

15. A.symmetric_difference_update(B)：将集合A和集合B的差集，更新到集合A

16. union()：并集，返回新的集合

17. A.update(B)：将并集更新到集合A

18. \_\_and\_\_: &

19. \_\_contains\_\_: y in x

20. \_\_eq\_\_: ==

21. \_\_getattribute\_\_: 

22. \_\_ge\_\_: >=

23. \_\_gt\_\_: >

24. \_\_iand\_\_: 

25. \_\_ior\_\_: 

26. \_\_iter\_\_: 

27. \_\_ixor\_\_: 

28. \_\_len\_\_: len()

29. \_\_le\_\_: <=

30. \_\_lt\_\_: <

31. \_\_ne\_\_: !=

32. \_\_or\_\_: |

33. \_\_rand\_\_: 

34. \_\_reduce\_\_: 

35. \_\_repr\_\_: 

36. \_\_ror\_\_: 

37. \_\_rsub\_\_: 

38. \_\_rxor\_\_: 

39. \_\_sizeof\_\_: 

40. \_\_sub\_\_: 