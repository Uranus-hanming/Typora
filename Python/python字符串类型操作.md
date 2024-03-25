[toc]
###### 1. 如何拆分含有多種分隔符的字符串？

```python
"""
    split
    map
    lambda
    list
    sum
    functools,reduce
    re
"""
# 方法1：連續使用str.split() 方法，每次處理一種分隔符號。
s = "dsa,alsdk;dkjfkla\tdk;lsadjjqwek.ldkfqoweal;jasd;jfk-sldfjqwekj,lasdfjk/dla."
s.split(',')
[ss.split(';') for ss in s.split(',')]
list(map(lambda ss: ss.split(';'), s.split(',')))

t = []
list(map(t.extend, [ss.split(',') for ss in s.split(';' )]))
sum([ss.split(',') for ss in s.split(';')], [])


def my_split(s, seps):
    res = [s]
    for sep in seps:
        t = []
        list(map(lambda ss: t.extend(ss.split(sep)), res))
        res = t
    return res


result = my_split(s, ',;\t/')
print(result)

# 方法2：使用正則表達式的re.split()方法
from functools import reduce

q = reduce(lambda l, sep: sum(map(lambda ss: ss.split(sep), l), []), ',;/\t', [s])

my_split2 = lambda s, seps: reduce(lambda l, sep: sum(map(lambda ss: ss.split(sep), l), []), seps, [s])
print(my_split2(s, ',;\t/'))

# 方法3：使用正則表達式的re.split()方法
import re

p = re.split('[,;/\t]+', s)
print(p)
```

###### 2. 如何判斷字符串a是否以字符串b開頭或結尾？

```python
"""
    os-listdir,stat,chmod
    st_mode
    oct
    stat,S_IXUSR
    startswith,endswith

    某問價系統目錄下有一系列文件：
    ald.c
    ljef.py
    nfwe.java
    elekn.sh
    idnlw.cpp
    ...
    編寫程序給其中所有.sh文件和.py文件加上用戶可執行權限。
"""

# 使用str.startswith()和str.endswith()方法（注意：多個匹配時參數使用元祖。）
import os

d = os.listdir('.')
s = os.stat('b.py')
r = s.st_mode
oct(s.st_mode)
oct(s.st_mode | 0o100)  # 修改可執行權限
os.chmod('b.py', s.st_mode | 0o100)

import stat

a = stat.S_IXUSR

for fn in os.listdir():
    if fn.endswith(('.py', '.sh')):  # 找到文件夾中所有的.py和.sh文件
        fs = os.stat(fn)  # 讀取文件狀態
        os.chmod(fn, fs.st_mode | stat.S_IXUSR)  # 給文件加上可執行權限
```

###### 3. 如何調整字符串中文本的格式？

```python
"""
    open
    re.sub
"""

# 使用正則表達式re.sub()方法做字符串替換，利用正則表達式的捕獲組，捕獲每個部分內容，再替換字符串中調整各個補貨組的順序。
f = open('/var/log/dpkg.log.1')
log = f.read()
import re

re.sub('(\d{4})-(\d{2})-(\d{2})', r'\2/\3/\1', log)
re.sub('(?P<d>\d{4})-(?P<m>\d{2})-(?P<y>\d{2})', r'\g<m>/\g<d>/\g<y>', log)  # 命名分組
```

###### 4. 如何將多個小字符串拼接成一個大字符串？

```python
"""
    reduce
    str.join()
"""

# 方法1：迭代列表，連續用‘+’操作依次拼接每一個字符串。
l = ["dls", "alsdjf", "sfa", "qowe", "oqadfj", "ldfjwe", "dfwhbe"]
s = ''
for x in l:
    s += x

from functools import reduce
r = reduce(str.__add__, l)

# 方法2：使用str.join()方法，更加快速的拼接列表中所有字符串。
q = ''.join(l)

import timeit
```

###### 5. 如何對字符串進行左，右，居中對齊？

```python
"""
    ljust,rjust,center
    format
    map
    max
"""

# 方法1：使用字符串的str.ljust(),str.rjust(),str.center()進行左，右，居中對齊。
# 方法2：使用format()方法，傳遞類似'<20','>20','^20'參數完成同樣任務。
s = 'abc'
s.ljust(10)
s.rjust(10)
s.center(10)
format(s, '<10')
format(s, '>10')
format(s, '^10')

d = {'ljfkl': 100.0, 'jkqwejwejfwe': 200.0, 'sdfqehqweh': 0.004, 'dshf': 40, 'woehfew': 500, 'dskaafdd': 404}
w = max(map(len, d.keys()))
for k, v in d.items():
    print(k.ljust(w), ':', v)
```

###### 6. 如何去掉字符串中不需要的字符？

```python
"""
    strip
    replace
    re.sub
    str.translate
    str.maketrans
    unicodedata.combining()
    dict
    ord
"""

"""
    實際案例
    1.過濾掉用戶輸入中前後多餘的空白字符：' ofqwejkfsd@gmail.com '
    2.過濾某windows下編輯文本中的'/r': 'hello world\r\n'
    3.去掉文本中的unicode組合符號（音調）
"""
# 方法一：字符串strip(),lstrip(),rstrip()方法去掉字符串兩端字符。
s = '   hanmingqin@gmail.com    '
s1 = '\t   hanmingqin@gmail.com    \t'
s2 = '===+-   hanmingqin@gmail.com   ==-+='
print(s2.strip('+-= '))

# 方法二：刪除單個固定位置的字符，可以使用切片 + 拼接的方式。
s3 = 'abc:1234'
print(s3[:3] + s3[4:])

# 方法3；字符串的replace()方法或正則表達式re.sub()刪除任意子串。
s4 = '   abc    def   '
s5 = '\t\n   abc    def   \t'
print(s4.replace(' ', ''))
import re

r1 = re.sub('[ \t\n]', '', s4)
r2 = re.sub('\s+', '', s4)
print(r2)

# 方法4：字符串的translate()方法，可以同時刪除多種不同字符。
s6 = 'abcdef123zy'
s6.translate({ord('a'): 'X', ord('b'): 'Y'})
q = s6.translate(s6.maketrans('abcef', 'EFABC'))

s6.translate({ord('a'): None})  # 刪除a

import unicodedata

unicodedata.combining()  # 判斷一個字符是否是一個組合符號
dict.fromkeys([ord(c) for c in s if unicodedata.combining(c)], None)
s.translate(dict.fromkeys([ord(c) for c in s if unicodedata.combining(c)], None))  # 去掉所有的聲調符號
```