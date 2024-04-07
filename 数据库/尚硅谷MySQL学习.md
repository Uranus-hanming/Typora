[toc]
### MySQL基础篇

##### 数据库相关概念

1. DB: 数据库(Database)

   > 即存储数据的“仓库”，其本质是一个**文件系统**。它保存了一系列有组织的数据。

2. DBMS：数据库管理系统（Database Management System）

   > 是一种操纵和管理数据库的大型软件，用于建立、使用和维护数据库，对数据库进行统一管理和控
   > 制。用户通过数据库管理系统访问数据库中表内的数据。

3. SQL：结构化查询语言（Structured Query Language）

   > 专门用来与数据库通信的语言。

##### 数据库类型的分类

###### 关系型数据库

- 以***行(row) 和列(column)*** 的形式存储数据
- 可以用***SQL语句***方便的在一个表以及多个表之间做非常复杂的数据查询

###### 非关系型数据库

> 基于**键值对**存储数据；
>
> 不需要经过SQL层的解析；

- 键值型数据库

  > 通过 **Key-Value 键值的方式**来存储数据，其中 Key 和 Value 可以是简单的对象，也可以是复杂的对象。
  >
  > 查找速度快，应用于内存缓存 -- Redis

- 文档型数据库

  > 可存放并获取文档，可以是XML、JSON等格式；
  >
  > ***文档***作为处理信息的基本单位，一个文档就相当于一条记录。
  >
  > MongoDB

- 搜索引擎数据库

  > 应用在搜索引擎领域的数据存储形式
  >
  > Elasticsearch

- 列式数据库

  > 将数据**按照列存储**到数据库中，这样做的好处是可以大量降低系统的I/O，适合于分布式文件系统，不足在于功能相对有限。典型产品：HBase

- 图形数据库

  > 是一种**存储图形关系**的数据库。它利用了图这种数据结构存储了实体（对象）之间的关系。

##### 表的关联关系

1. 一对一关联

2. 一对多关联

3. 多对多关联

   > 要表示多对多关系，**必须创建第三个表**，该表通常称为**联接表**，它将多对多关系划分为两个一对多关系。将这两个表的主键都插入到第三个表中。

4. 自我引用

##### SQL分类

###### DDL（Data Definition Languages、数据定义语言）

> 这些语句定义了不同的数据库、表、视图、索引等数据库对象，还可以用来创建、删除、修改数据库和数据表的结构。
>
> **CREATE、DROP、DELETE、ALTER** 等

###### DML（Data Manipulation Language、数据操作语言）

> 用于添加、删除、更新和查询数据库记录，并检查数据完整性。
>
> 主要的语句关键字包括**INSERT 、DELETE 、UPDATE 、SELECT** 等。

###### DCL（Data Control Language、数据控制语言）

> 用于定义数据库、表、字段、用户的访问权限和安全级别。
>
> 主要的语句关键字包括**GRANT 、REVOKE 、COMMIT 、ROLLBACK 、SAVEPOINT** 等。

##### MySQL基本操作指令

- 数据导出到本地 - mysqldump

  ```mysql
  mysqldump --default-character-set=utf8 --hex-blob -h localhost -uroot -p123456 gitea > gitea.sql
  //注意是在命令行，而不是在进入mysql中输入这个命令，导出后，对应的sql，在MySQL的bin目录下 。
   
   mysqldump --default-character-set=utf8 --hex-blob -hlocalhost -uroot -p123456 gitea > gitea.sql

  //也可以
   mysqldump -hlocalhost -uroot -p123456 gitea(db) > /xx/xx/gitea.sql(导出的文件路径)
  ```

- 数据导入 - source

  ```mysql
  source d:\mysqldb.sql
  ```

- SELECT 语句

  1. SELECT ...
  2. SELECT ... FROM

- 列的别名（As 可以省略）

- 去除重复行

  ```mysql
  SELECT DISTINCT
  ```

- 着重号``

  > 我们需要保证表中的字段、表名等没有和保留字、数据库系统或常用方法冲突。如果真的相同，请在SQL语句中使用一对``（着重号）引起来。

- 显示表结构 - DESC

- 排序

  ```MySQL
  ORDER BY
  ASC (ascend)：升序
  DESC：降序
  ```

- 分页 - LIMIT

  ```
  LIMIT [位置偏移量，] 行数
  ```


##### 运算符

###### 算术运算符

> 算术运算符主要用于数学运算，其可以连接运算符前后的两个数值或表达式，对数值或表达式进行加（+）、减（-）、乘（*）、除（/）和取模（%）运算。

| 运算符 | 名称               | 作用                     | 示例                             |
| ------ | ------------------ | ------------------------ | -------------------------------- |
| +      | 加法运算符         | 计算两个值或表达式的和   | SELECT A + B                     |
| -      | 减法运算符         | 计算两个值或表达式的差   | SELECT A - B                     |
| *      | 乘法运算符         | 计算两个值或表达式的乘积 | SELECT A * B                     |
| /或DIV | 除法运算符         | 计算两个值或表达式的商   | SELECT A / B<br />SELECT A DIV B |
| %或MOD | 求模（求余）运算符 | 计算两个值或表达式的余数 | SELECT A % B<br />SELECT A MOD B |

###### 比较运算符

> 比较运算符用来对表达式左边的操作数和右边的操作数进行比较，比较的结果为真则返回1，比较的结果为假则返回0，其他情况则返回NULL。

| =    | <=>      | <>(!=) | <    | <=       | >    | \>=      |
| ---- | -------- | ------ | ---- | -------- | ---- | -------- |
| 等于 | 安全等于 | 不等于 | 小于 | 小于等于 | 大于 | 大于等于 |

###### 非符号类型运算符

1. 空运算符 

   > 空运算符（**IS NULL或者ISNULL**）判断一个值是否为NULL，如果为NULL则返回1，否则返回0。

2. 非空运算符 

   > 非空运算符（**IS NOT NULL**）判断一个值是否不为NULL，如果不为NULL则返回1，否则返回0。

3. 最小值运算符 

   > 语法格式为：**LEAST(值1，值2，...，值n)**。其中，“值n”表示参数列表中有n个值。在有两个或多个参数的情况下，返回最小值。

4. 最大值运算符 

   > 语法格式为：**GREATEST(值1，值2，...，值n)**。其中，n表示参数列表中有n个值。当有两个或多个参数时，返回值为最大值。假如任意一个自变量为NULL，则GREATEST()的返回值为NULL。

5. BETWEEN AND运算符 

   > BETWEEN运算符使用的格式通常为**SELECT D FROM TABLE WHERE C BETWEEN AAND B**，此时，当C大于或等于A，并且C小于或等于B时，结果为1，否则结果为0。

6. IN运算符 

   > IN运算符用于判断给定的值是否是IN列表中的一个值，如果是则返回1，否则返回0。如果给定的值为NULL，或者IN列表中存在NULL，则结果为NULL。

7. NOT IN运算符 

   > NOT IN运算符用于判断给定的值是否不是IN列表中的一个值，如果不是IN列表中的一个值，则返回1，否则返回0。

8. LIKE运算符 

   > LIKE运算符主要用来匹配字符串，通常用于模糊匹配，如果满足条件则返回1，否则返回0。如果给定的值或者匹配条件为NULL，则返回结果为NULL。
   >
   > “%”：匹配0个或多个字符。
   > “_”：只能匹配一个字符。

9. REGEXP运算符

   > REGEXP运算符用来匹配字符串，语法格式为： **expr REGEXP 匹配条件**。

   （1）‘^’匹配以该字符后面的字符开头的字符串。
   （2）‘$’匹配以该字符前面的字符结尾的字符串。
   （3）‘.’匹配任何一个单字符。
   （4）“[...]”匹配在方括号内的任何字符。例如，“[abc]”匹配“a”或“b”或“c”。为了命名字符的范围，使用一
   个‘-’。“[a-z]”匹配任何字母，而“[0-9]”匹配任何数字。
   （5）‘*’匹配零个或多个在它前面的字符。例如，“x*”匹配任何数量的‘x’字符，“[0-9]*”匹配任何数量的数字，而“*”匹配任何数量的任何字符。

###### 逻辑运算符 

> 逻辑运算符主要用来判断表达式的真假，在MySQL中，逻辑运算符的返回结果为1、0或者NULL。

1. 逻辑非运算符 逻辑非（NOT或!）运算符表示当给定的值为0时返回1；当给定的值为非0值时返回0；
   当给定的值为NULL时，返回NULL。
2. 逻辑与运算符 逻辑与（AND或&&）运算符是当给定的所有值均为非0值，并且都不为NULL时，返回
   1；当给定的一个值或者多个值为0时则返回0；否则返回NULL。
3. 逻辑或运算符 逻辑或（OR或||）运算符是当给定的值都不为NULL，并且任何一个值为非0值时，则返
   回1，否则返回0；当一个值为NULL，并且另一个值为非0值时，返回1，否则返回NULL；当两个值都为
   NULL时，返回NULL。
4. 逻辑异或运算符 逻辑异或（XOR）运算符是当给定的值中任意一个值为NULL时，则返回NULL；如果
   两个非NULL的值都是0或者都不等于0时，则返回0；如果一个值为0，另一个值不为0时，则返回1。

###### 位运算符 

> 位运算符是在二进制数上进行计算的运算符。位运算符会先将操作数变成二进制数，然后进行位运算，最后将计算结果从二进制变回十进制数。

1. 按位与运算符 按位与（&）运算符将给定值对应的二进制数逐位进行逻辑与运算。当给定值对应的二

进制位的数值都为1时，则该位返回1，否则返回0。

2. 按位或运算符 按位或（|）运算符将给定的值对应的二进制数逐位进行逻辑或运算。当给定值对应的
    二进制位的数值有一个或两个为1时，则该位返回1，否则返回0。
3. 按位取反运算符 按位取反（~）运算符将给定的值的二进制数逐位进行取反操作，即将1变为0，将0变
    为1。
4. 按位右移运算符 按位右移（>>）运算符将给定的值的二进制数的所有位右移指定的位数。右移指定的
    位数后，右边低位的数值被移出并丢弃，左边高位空出的位置用0补齐。
5. 按位左移运算符 按位左移（<<）运算符将给定的值的二进制数的所有位左移指定的位数。左移指定的
    位数后，左边高位的数值被移出并丢弃，右边低位空出的位置用0补齐。

##### 多表查询

- 多个表中有相同列时，必须在列名之前加上表名前缀。

- 使用别名可以简化查询。

  > ，如果我们使用了表的别名，在查询字段中、过滤条件中就只能使用别名进行代替，不能使用原有的表名，否则就会报错。

- 连接 n个表,至少需要n-1个连接条件。

- 当table1和table2本质上是同一张表，只是**用取别名的方式虚拟成两张表**以代表不同的意义。然后两个表再进行内连接，外连接等查询。

###### 1. 等值连接 vs 非等值连接

###### 2. 自连接 vs 非自连接

###### 3. 内连接 vs 外连接

- 内连接: 合并具有同一列的两个以上的表的行, 结果集中不包含一个表与另一个表不匹配的行。

  ```mysql
  SELECT 字段列表
  FROM A表 INNER JOIN B表
  ON 关联条件
  WHERE 等其他子句;
  ```

- 外连接: 两个表在连接过程中除了返回满足连接条件的行以外还返回左（或右）表中不满足条件的
  行 ，这种连接称为左（或右） 外连接。没有匹配的行时, 结果表中相应的列为空(NULL)。

  - 如果是左外连接，则连接条件中左边的表也称为主表，右边的表称为从表。

    ```mysql
    #实现查询结果是A
    SELECT 字段列表
    FROM A表 LEFT JOIN B表
    ON 关联条件
    WHERE 等其他子句;
    ```

  - 如果是右外连接，则连接条件中右边的表也称为主表，左边的表称为从表。

    ```mysql
    #实现查询结果是B
    SELECT 字段列表
    FROM A表 RIGHT JOIN B表
    ON 关联条件
    WHERE 等其他子句;
    ```

###### 7种SQL JOINS的实现

1. 内连接 A∩B

   ```mysql
   select 字段列表
   from A表 join B表
   on 关联条件
   ```

2. 左外连接

   ```mysql
   select 字段列表
   from A表 left join B表
   on 关联条件
   ```

3. 右外连接

   ```mysql
   select 字段列表
   from A表 right join B表
   on 关联条件
   ```

4. A - A∩B

   ```mysql
   select 字段列表
   from A表 left join B表
   on 关联条件
   where 从表关联字段 is null and 等其他子句;
   ```

5. B - A∩B

   ```mysql
   select 字段列表
   from A表 right join B表
   on 关联条件
   where 从表关联字段 is null and 等其他子句;
   ```

6. 满外连接

   ```mysql
   select 字段列表
   from A表 left join B表
   on 关联条件
   where 等其他子句
   union
   select 字段列表
   from A表 right join B表
   on 关联条件
   where 等其他子句;
   ```

7. A ∪B- A∩B 或者 (A - A∩B) ∪ （B - A∩B）

   ```mysql
   select 字段列表
   from A表 left join B表
   on 关联条件
   where 从表关联字段 is null and 等其他子句
   union
   select 字段列表
   from A表 right join B表
   on 关联条件
   where 从表关联字段 is null and 等其他子句
   ```

##### 单行函数

###### 1. 数值函数

- 基本函数

| 函数                | 用法                                                         |
| ------------------- | ------------------------------------------------------------ |
| ABS(x)              | 返回x的绝对值                                                |
| SIGN(X)             | 返回X的符号。正数返回1，负数返回-1，0返回0                   |
| PI()                | 返回圆周率的值                                               |
| CEIL(x)，CEILING(x) | 返回大于或等于某个值的最小整数                               |
| FLOOR(x)            | 返回小于或等于某个值的最大整数                               |
| LEAST(e1,e2,e3…)    | 返回列表中的最小值                                           |
| GREATEST(e1,e2,e3…) | 返回列表中的最大值                                           |
| MOD(x,y)            | 返回X除以Y后的余数                                           |
| RAND()              | 返回0~1的随机值                                              |
| RAND(x)             | 返回0~1的随机值，其中x的值用作种子值，相同的X值会产生相同的随机 |
| ROUND(x)            | 返回一个对x的值进行四舍五入后，最接近于X的整数               |
| ROUND(x,y)          | 返回一个对x的值进行四舍五入后最接近X的值，并保留到小数点后面Y位 |
| TRUNCATE(x,y)       | 返回数字x截断为y位小数的结果                                 |
| SQRT(x)             | 返回x的平方根。当X的值为负数时，返回NULL                     |

- 角度与弧度互换函数

| 函数       | 用法                                  |
| ---------- | ------------------------------------- |
| RADIANS(x) | 将角度转化为弧度，其中，参数x为角度值 |
| DEGREES(x) | 将弧度转化为角度，其中，参数x为弧度值 |

- 三角函数

| 函数       | 用法                                                         |
| ---------- | ------------------------------------------------------------ |
| SIN(x)     | 返回x的正弦值，其中，参数x为弧度值                           |
| ASIN(x)    | 返回x的反正弦值，即获取正弦为x的值。如果x的值不在-1到1之间，则返回NULL |
| COS(x)     | 返回x的余弦值，其中，参数x为弧度值                           |
| ACOS(x)    | 返回x的反余弦值，即获取余弦为x的值。如果x的值不在-1到1之间，则返回NULL |
| TAN(x)     | 返回x的正切值，其中，参数x为弧度值                           |
| ATAN(x)    | 返回x的反正切值，即返回正切值为x的值                         |
| ATAN2(m,n) | 返回两个参数的反正切值                                       |
| COT(x)     | 返回x的余切值，其中，X为弧度值                               |

- 指数与对数

| 函数                 | 用法                                                 |
| -------------------- | ---------------------------------------------------- |
| POW(x,y)，POWER(X,Y) | 返回x的y次方                                         |
| EXP(X)               | 返回e的X次方，其中e是一个常数，2.718281828459045     |
| LN(X)，LOG(X)        | 返回以e为底的X的对数，当X <= 0 时，返回的结果为NULL  |
| LOG10(X)             | 返回以10为底的X的对数，当X <= 0 时，返回的结果为NULL |
| LOG2(X)              | 返回以2为底的X的对数，当X <= 0 时，返回NULL          |

- 进制间的转换

| 函数          | 用法                     |
| ------------- | ------------------------ |
| BIN(x)        | 返回x的二进制编码        |
| HEX(x)        | 返回x的十六进制编码      |
| OCT(x)        | 返回x的八进制编码        |
| CONV(x,f1,f2) | 返回f1进制数变成f2进制数 |

###### 2. 字符串函数

###### 3. 日期和时间函数

###### 4. 流程控制函数

> 流程处理函数可以根据不同的条件，执行不同的处理流程，可以在SQL语句中实现不同的条件选择。

| 函数                                              | 用法                                            |
| ------------------------------------------------- | ----------------------------------------------- |
| IF(value,value1,value2)                           | 如果value的值为TRUE，返回value1，否则返回value2 |
| IFNULL(value1, value2)                            | 如果value1不为NULL，返回value1，否则返回value2  |
| CASE WHEN 条件1 THEN 结果1 WHEN 条件2 THEN 结果2  | 相当于Java的if...else if...else...              |
| CASE expr WHEN 常量值1 THEN 值1 WHEN 常量值1 THEN | 相当于Java的switch...case...                    |

###### 5. 加密与解密函数

> MySQL中内置了一些可以查询MySQL信息的函数，这些函数主要用于帮助数据库开发或运维人员更好地对数据库进行维护工作。

| 函数                                    | 用法                                                     |
| --------------------------------------- | -------------------------------------------------------- |
| VERSION()                               | 返回当前MySQL的版本号                                    |
| CONNECTION_ID()                         | 返回当前MySQL服务器的连接数                              |
| DATABASE()，SCHEMA()                    | 返回MySQL命令行当前所在的数据库                          |
| USER()，CURRENT_USER()、SYSTEM_USER()， | 返回当前连接MySQL的用户名，返回结果格式为“主机名@用户名” |
| CHARSET(value)                          | 返回字符串value自变量的字符集                            |
| COLLATION(value)                        | 返回字符串value的比较规则                                |

##### 聚合函数

> 对一组数据进行汇总的函数，输入的是一组数据的集合，输出的是单个值（输入一组数据，输出一个值）。

```mysql
SELECT [column,] group function(column), ...
FROM table
[WHERE condition]
[GROUP BY column]
[ORDER BY column]
[LIMIT];
```

- AVG()

- SUM()

- MAX()

- COUNT()

  > OUNT(*)返回表中记录总数

###### GROUP BY

> 使用GROUP BY子句将表中的数据分成若干组。

```mysql
SELECT column, group_function(column)
FROM table
[WHERE condition]
[GROUP BY group_by_expression]
[ORDER BY column];
```

- 使用多个列分组

- GROUP BY 中使用WITH ROLLUP

  > 使用WITH ROLLUP 关键字之后，在所有查询出的分组记录之后增加一条记录，该记录计算查询出的所有记录的总和，即统计记录数量。

##### HAVING

> HAVING不能单独使用，必须要跟GROUP BY 一起使用。

```mysql
SELECT column, group_function
FROM table
[WHERE  condition]
[GROUP BY  group_by_expression]
[HAVING  group_conditon]
[ORDER BY  column];
```

##### SELECT的执行过程

```mysql
# 在 SELECT 语句执行这些步骤的时候，每个步骤都会产生一个虚拟表，然后将这个虚拟表传入下一个步骤中作为输入。需要注意的是，这些步骤隐含在 SQL 的执行过程中，对于我们来说是不可见的。

SELECT DISTINCT player_id, player_name, count(*) as num # 顺序 5
FROM player JOIN team ON player.team_id = team.team_id # 顺序 1
WHERE height > 1.80 # 顺序 2
GROUP BY player.team_id # 顺序 3
HAVING num > 2 # 顺序 4
ORDER BY num DESC # 顺序 6
LIMIT 2 # 顺序 7
```

###### 查询的结构

1. 方式一

   ```mysql
   SELECT ...,...,...
   FROM ...,...,...
   WHERE 多表的链接条件
   AND 不包含组函数的过滤条件
   GROUP BY ...,...
   HAVING 包含组函数的过滤条件
   ORDER BY ... ASC/DESC
   LIMIT ...,...

   # 其中：
   #（1）from：从哪些表中筛选
   #（2）on：关联多表查询时，去除笛卡尔积
   #（3）where：从表中筛选的条件
   #（4）group by：分组依据
   #（5）having：在统计结果中再次筛选
   #（6）order by：排序
   #（7）limit：分页
   ```

2. 方式二

   ```mysql
   SELECT ...,...,...
   FROM ... JOIN ...
   ON 多表的连接条件
   JOIN ...
   ON ...
   WHERE 不包含组函数的过滤条件
   AND/OR 不包含组函数的过滤条件
   GROUP BY ...,...
   HAVING 包含组函数的过滤条件
   ORDER BY ... ASC/DESC
   LIMIT ...,...
   ```

###### SELECT 执行顺序

1. 关键字的顺序是不能颠倒的：

   ```mysql
   SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT ...
   ```

2. SELECT语句的执行顺序

   ```mysql
   FROM -> WHERE -> GROUP BY -> HAVING -> SELECT 的字段 -> DISTINCT ->  ORDER BY -> LIMIT
   
   1 FROM <left_table>
   2. ON <join_condition>
   3. <join_type> JOIN <right_table>
   4. WHERE <where_conditon>
   5. GROUP BY <group_by_list>
   6. HAVING <having_conditon>
   7. SELECT 
   8. DISTINCT <select_list>
   9. ORDER BY <order_by_condition>
   10. LIMIT <limit_number>
   ```

###### SQL的执行原理

> SELECT 是先执行 FROM 这一步的。在这个阶段，如果是多张表联查，还会经历下面的几个步骤：
>
> 1. 首先先通过 CROSS JOIN 求笛卡尔积，相当于得到虚拟表 vt（virtual table）1-1；
> 2. 通过 ON 进行筛选，在虚拟表 vt1-1 的基础上进行筛选，得到虚拟表 vt1-2；
> 3. 添加外部行。如果我们使用的是左连接、右链接或者全连接，就会涉及到外部行，也就是在虚拟
>     表 vt1-2 的基础上增加外部行，得到虚拟表 vt1-3。
>     当然如果我们操作的是两张以上的表，还会重复上面的步骤，直到所有表都被处理完为止。这个过程得
>     到是我们的原始数据。
>     SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT...
>     FROM -> WHERE -> GROUP BY -> HAVING -> SELECT 的字段 -> DISTINCT -> ORDER BY -> LIMIT
>     SELECT DISTINCT player_id, player_name, count(*) as num # 顺序 5
>     FROM player JOIN team ON player.team_id = team.team_id # 顺序 1
>     WHERE height > 1.80 # 顺序 2
>     GROUP BY player.team_id # 顺序 3
>     HAVING num > 2 # 顺序 4
>     ORDER BY num DESC # 顺序 6
>     LIMIT 2 # 顺序 7
>     当我们拿到了查询数据表的原始数据，也就是最终的虚拟表 vt1 ，就可以在此基础上再进行 WHERE 阶
>     段。在这个阶段中，会根据 vt1 表的结果进行筛选过滤，得到虚拟表 vt2 。
>     然后进入第三步和第四步，也就是 GROUP 和 HAVING 阶段。在这个阶段中，实际上是在虚拟表 vt2 的
>     基础上进行分组和分组过滤，得到中间的虚拟表 vt3 和 vt4 。
>     当我们完成了条件筛选部分之后，就可以筛选表中提取的字段，也就是进入到 SELECT 和 DISTINCT
>     阶段。
>     首先在 SELECT 阶段会提取想要的字段，然后在 DISTINCT 阶段过滤掉重复的行，分别得到中间的虚拟表
>     vt5-1 和 vt5-2 。
>     当我们提取了想要的字段数据之后，就可以按照指定的字段进行排序，也就是 ORDER BY 阶段，得到
>     虚拟表 vt6 。
>     最后在 vt6 的基础上，取出指定行的记录，也就是 LIMIT 阶段，得到最终的结果，对应的是虚拟表
>     vt7 。
>     当然我们在写 SELECT 语句的时候，不一定存在所有的关键字，相应的阶段就会省略。
>     同时因为 SQL 是一门类似英语的结构化查询语言，所以我们在写 SELECT 语句的时候，还要注意相应的
>     关键字顺序，所谓底层运行的原理，就是我们刚才讲到的执行顺序。

##### 子查询

> 子查询指一个**查询语句嵌套**在另一个查询语句内部的查询;
>
> SQL 中子查询的使用大大增强了 SELECT 查询的能力，因为很多时候查询需要从结果集中获取数据，或者需要从同一个表中先计算得出一个数据结果，然后与这个数据结果（可能是某个标量，也可能是某个集合）进行比较。

- 子查询（内查询）在主查询之前一次执行完成；
- 子查询的结果被主查询（外查询）使用；

```mysql
SELECT select_list
FROM table
WHERE expr operator
				(SELECT select_list
                FROM table);
```

###### 子查询的分类

1. 按内查询的结果返回一条还是多条记录，将子查询分为**单行子查询、多行子查询**。
2. 按内查询是否被执行多次，将子查询划分为**相关(或关联)子查询和不相关(或非关联)子查询**。
   1. 子查询从数据表中查询了数据结果，如果这个数据结果只执行一次，然后这个数据结果作为主查询的条
      件进行执行，那么这样的子查询叫做***不相关子查询***。
   2. 如果子查询需要执行多次，即采用循环的方式，先从外部查询开始，每次都传入子查询进行查
      询，然后再将结果反馈给外部，这种嵌套的执行方式就称为***相关子查询***。

###### 单行子查询

| 操作符 | 含义                     |
| ------ | ------------------------ |
| =      | equal to                 |
| >      | greater than             |
| >=     | greater than or equal to |
| <      | less than                |
| <=     | less than or equal to    |
| <>     | not equal to             |

###### 多行子查询

| 操作符 | 含义                                                     |
| ------ | -------------------------------------------------------- |
| IN     | 等于列表中的任意一个                                     |
| ANY    | 需要和单行比较操作符一起使用，和子查询返回的某一个值比较 |
| ALL    | 需要和单行比较操作符一起使用，和子查询返回的所有值比较   |
| SOME   | 实际上是ANY的别名，作用相同，一般常使用ANY               |

##### 创建和管理表

- 一条数据的存储过程

  ```
  创建数据库 -> 确认字段 -> 创建数据表 -> 插入数据
  ```

- mysql数据库系统从大到小

  ```
  数据库服务器、数据库、数据表、数据表的行与列
  ```

###### mysql中的数据类型

| 类型             | 类型举例                                                |
| ---------------- | ------------------------------------------------------- |
| 整数类型         | TINYINT、SMALLINT、MEDIUMINT、INT(或INTEGER)、BIGINT    |
| 浮点类型         | FLOAT、DOUBLE                                           |
| 定点数类型       | DECIMAL                                                 |
| 位类型           | BIT                                                     |
| 日期时间类型     | YEAR、TIME、DATE、DATETIME、TIMESTAMP                   |
| 文本字符串类型   | CHAR、VARCHAR、TINYTEXT、TEXT、MEDIUMTEXT、LONGTEXT     |
| 枚举类型         | ENUM                                                    |
| 集合类型         | SET                                                     |
| 二进制字符串类型 | BINARY、VARBINARY、TINYBLOB、BLOB、MEDIUMBLOB、LONGBLOB |
| JSON类型         | JSON对象、JSON数组                                      |
| 空间数据类型     | 单值：GEOMETRY、POINT、LINESTRING、POLYGON；            |

###### 创建数据库

- 创建数据库

  ```mysql
  CREATE DATABASE 数据库名;
  ```

- 创建数据库并指定字符集

  ```mysql
  CREATE DATABASE 数据库名 CHARACTER SET 字符集;
  ```

- 3：判断数据库是否已经存在，不存在则创建数据库（ 推荐）

  ```mysql
  CREATE DATABASE IF NOT EXISTS 数据库名；
  ```

###### 使用数据库

- 查看当前所有的数据库

  ```mysql
  SHOW DATABASES; #有一个S，代表多个数据库
  ```

- 查看当前正在使用的数据库

  ```mysql
  SELECT DATABASE(); #使用的一个 mysql 中的全局函数
  ```

- 查看指定库下所有的表

  ```mysql
  SHOW TABLES FROM 数据库名;
  ```

- 查看数据库的创建信息

  ```mysql
  SHOW CREATE DATABASE 数据库名;
  或者：
  SHOW CREATE DATABASE 数据库名\G
  ```

- 使用/切换数据库

  ```mysql
  USE 数据库名;
  ```

###### 修改数据库

- 修改数据库名

  ```mysql
  rename database old_name to new_name
  ```

- 更改数据库字符集

  ```mysql
  ALTER DATABASE 数据库名 CHARACTER SET 字符集; #比如：gbk、utf8等
  ```

###### 删除数据库

```mysql
DROP DATABASE 数据库名;
DROP DATABASE IF EXISTS 数据库名;
```

###### 创建表

```mysql
CREATE TABLE [IF NOT EXISTS] 表名(
		字段1， 数据类型 [约束条件] [默认值],
		字段2， 数据类型 [约束条件] [默认值],
		字段3， 数据类型 [约束条件] [默认值],
		...
		[表约束条件]
);
```

###### 查看数据表结构

```mysql
SHOW CREATE TABLE 表名\G
```

###### 修改表 - ALTER

> 修改表指的是修改数据库中已经存在的数据表的结构。

- 向已有的表中添加列 - ADD

  ```mysql
  ALTER TABLE 表名 ADD [COLUMN] 字段名 字段类型 [FIRST|AFTER 字段名];
  ```

- 修改现有表中的列（可以修改列的数据类型，长度、默认值和位置）- MODIFY

  ```mysql
  ALTER TABLE 表名 MODIFY [COLUMN] 字段名1 字段类型 [DEFAULT 默认值] [FIRST|AFTER 字段名2];
  ```

- 删除现有表中的列 -DROP

  ```mysql
  ALTER TABLE 表名 DROP [COLUMN] 字段名
  ```

- 重命名现有表中的列 - CHANGE

  ```mysql
  ALTER TABLE 表名 CHANGE [column] 列名 新列名 新数据类型;
  ```

###### 重命名表 - RENAME

```mysql
RENAME TABLE emp TO myemp;
```

###### 删除表 - DROP

- 在MySQL中，当一张数据表没有与其他任何数据表形成关联关系时，可以将当前数据表直接删除。
- 数据和结构都被删除
- 所有正在运行的相关事务被提交
- 所有相关索引被删除

```mysql
DROP TABLE [IF EXISTS] 数据表1 [, 数据表2, ..., 数据表n];
```

###### 清空表 - TRUNCATE

- 删除表中所有的数据
- 释放表的存储空间

```mysql
TRUNCATE TABLE 表名;
```

##### 数据处理之增删改

###### 插入数据(INSERT INTO)

1. 为表的所有字段按默认顺序插入数据

   ```mysql
   INSERT INTO 表名
   VALUES (value1,value2,...);
   ```

2. 为表的指定字段插入数据

   ```mysql
   INSERT INTO 表名(column1 [,column2, ...,columnn])
   VALUES (value [,value2,...,valuen]);
   ```

3. 同时插入多条记录

   ```mysql
   INSERT INTO table_name
   VALUES
   (value1 [,value2, ...,valun]);
   (value1 [,value2, ...,valun]);
   ...
   (value1 [,value2, ...,valun]);

   INSERT INTO table_name(column1 [, column2, …, columnn])
   VALUES
   (value1 [,value2, …, valuen]),
   (value1 [,value2, …, valuen]),
   ……
   (value1 [,value2, …, valuen]);
   ```

4. 将查询结果插入到表中

   > INSERT还可以将SELECT语句查询的结果插入到表中，此时不需要把每一条记录的值一个一个输入，只需要使用一条INSERT语句和一条SELECT语句组成的组合语句即可快速地从一个或多个表中向一个表中插入多行。

```mysql
INSERT INTO 目标表名
(tar_column1 [, tar_column2, …, tar_columnn])
SELECT
(src_column1 [, src_column2, …, src_columnn])
FROM 源表名
[WHERE condition]
```

###### 更新数据(UPDATE)

```mysql
UPDATE table_name
SET column=value1, column2=value2, ..., column=valuen
[WHERE condition]
```

###### 删除数据(DELETE)

```mysql
DELETE FROM table_name [WHERE <condition>]
```

##### 视图(VIEW)

what、why、how、优缺点、before/after

- what

  - 视图是一种**虚拟表**，本身是不具有数据的，占用很少的内存空间，它是SQL中的一个重要概念。
  - 视图建立在已有表的基础上，视图赖以建立的这些表称为**基表**。
  - **视图的创建和删除**只影响视图本身，不影响对应的基表。但是当对视图中的数据进行增加、删除和
    修改操作时，数据表中的数据会相应地发生变化，反之亦然。
  - 向视图提供数据内容的语句为 SELECT 语句, 可以将视图理解为存储起来的 SELECT 语句

- why

  > 视图一方面可以帮我们使用表的一部分而不是所有的表；
  >
  > 另一方面也可以针对不同的用户指定不同的查询视图。

###### 创建视图

```mysql
CREATE [OR REPLACE]
[ALGORITHM = {UNDEFINED | MARGE | TEMPTABLE}]
VIEW 视图名称 [(字段列表)]
AS 查询语句
[WITH [CASCADED|LOCAL] CHECK OPTION]

CREATE VIEW 视图名称
AS 查询语句
```

###### 查看视图

1. 查看数据库的表对象、视图对象

   ```mysql
   SHOW TABLES;
   ```

2. 查看视图的结构

   ```mysql
   DESC / DESCRIBE 视图名称;
   ```

3. 查看视图的属性信息

   ```mysql
   # 查看视图信息（显示数据表的存储引擎、版本、数据行数和数据大小等）
   SHOW TABLE STATUS LIKE '视图名称'\G
   ```

4. 查看视图的详细定义信息

   ```mysql
   SHOW CREATE VIEW 视图名称;
   ```

###### 更新视图的数据

> MySQL支持使用INSERT、UPDATE和DELETE语句对视图中的数据进行插入、更新和删除操作。当视图中的
> 数据发生变化时，数据表中的数据也会发生变化，反之亦然。

###### 修改视图

```mysql
ALTER VIEW 视图名称
AS
查询语句
```

###### 删除视图

```mysql
DROP VIEW 视图名称;
DROP VIEW IF EXISTS 视图名称;
```

##### 存储过程与函数

- 是一组经过**预先编译的 SQL 语句**的封装。
- 存储过程和函数能够将复杂的SQL逻辑封装在一起，应用程序无须关注存储过程和函数内部复杂的SQL逻辑，而只需要简单地调用存储过程和函数即可。
- 存储过程预先存储在 MySQL 服务器上，需要执行的时候，客户端只需要向服务器端发出调用存储过程的命令，服务器端就可以把预先存储好的这一系列 SQL 语句全部执行。

###### 分类

1. 没有参数（无参数无返回）
2. 仅仅带 IN 类型（有参数无返回）
3. 仅仅带 OUT 类型（无参数有返回）
4. 既带 IN 又带 OUT（有参数有返回）
5. 带 INOUT（有参数有返回）

###### 创建存储过程(PROCEDURE)

```mysql
“DELIMITER //”语句的作用是将MySQL的结束符设置为//，并以“END //”结束存储过程。存储过程定义完毕之后再使用“DELIMITER ;”恢复默认结束符。

DELIMITER //
CREATE PROCEDURE 存储过程名(IN|OUT|INOUT 参数名 参数类型，...)
[characteristics ...]
BEGIN
	存储过程体
	
END //
DELIMITER ;
```

调用存储过程(CALL)

```mysql
CALL 存储过程名（实参列表）
```

1. 调用in模式的参数：

   ```mysql
   CALL sp1('值');
   ```

2. 调用out模式的参数：

   ```mysql
   SET @name;
   CALL sp1(@name);
   SELECT @name;
   ```

3. 调用inout模式的参数：

   ```mysql
   SET @name=值;
   CALL sp1(@name);
   SELECT @name;
   ```

###### 存储函数的使用(FUNCTION)

```mysql
DELIMITER //
CREATE FUNCTION 函数名(参数名 参数类型，...)
RETURNS 返回值类型
[characteristics ...]
BEGIN
	函数体   # 函数体中肯定有RETURN 语句
	
END //
DELIMITER ;
```

###### 调用存储函数(SELECT)

```mysql
SELECT 函数名(实参列表)
```

###### 存储过程和函数的查看、修改、删除

- 查看(SHOW)

  1. 使用SHOW CREATE语句查看存储过程和函数的创建信息

     ```mysql
     SHOW CREATE {PROCEDURE | FUNCTION} 存储过程名或函数名 [\G]
     ```

  2. 使用SHOW STATUS语句查看存储过程和函数的状态信息

     ```mysql
     SHOW {PROCEDURE | FUNCTION} STATUS [LIKE 'pattern']
     ```

  3. 从information_schema.Routines表中查看存储过程和函数的信息

     ```mysql
     # MySQL中存储过程和函数的信息存储在information_schema数据库下的Routines表中。可以通过查询该表的记录来查询存储过程和函数的信息。
   
     SELECT * FROM information_schema.Routines
     WHERE ROUTINE_NAME='存储过程或函数的名' [AND ROUTINE_TYPE = {'PROCEDURE|FUNCTION'}];
     ```

- 修改(ALTER)

  > 修改存储过程或函数，不影响存储过程或函数功能，只是修改相关特性。

  ```mysql
  ALTER {PROCEDURE | FUNCTION} 存储过程或函数的名 [characteristic ...]
  ```

- 删除(DROP)

  ```mysql
  DROP {PROCEDURE | FUNCTION} [IF EXISTS] 存储过程或函数的名
  ```

##### 变量

> 可以使用变量来**存储查询或计算的中间结果数据**，或者输出最终的结果数据。

###### 1. 系统变量

- 变量由系统定义，不是用户定义，属于服务器层面。
- 启动MySQL服务，生成MySQL服务实例期间，MySQL将为MySQL服务器内存中的系统变量赋值，这些系统变量定义了当前MySQL服务实例的属性、特征。
- 系统变量分为***全局系统变量***（需要添加global 关键字）以及***会话系统变量***（需要添加 session 关键字）
- **全局系统变量**针对于所有会话（连接）有效，但不能跨重启
- **会话系统变量**仅针对于当前会话（连接）有效。会话期间，当前会话对某个会话系统变量值的修改，不会影响其他会话同一个会话系统变量的值。
- 会话1对某个**全局系统变量值**的修改会导致会话2中同一个全局系统变量值的修改。

**查看所有或部分系统变量(SHOW)**

查看所有全局变量

```mysql
SHOW GLOBAL VARIABLES;
```

查看所有会话变量

```mysql
SHOW SESSION VARIABLES;
```

查看满足条件的部分系统变量

```mysql
SHOW GLOBAL VARIABLES LIKE '%标识符%';
```

查看满足条件的部分会话变量

```mysql
SHOW SESSION VARIABLES LIKE '%标识符%';
```

**查看指定系统变量(SELECT)**

> 作为 MySQL 编码规范，MySQL 中的系统变量以两个“@” 开头，其中“@@global”仅用于标记**全局系统变量**，“@@session”仅用于标记**会话系统变量**。
>
> “@@”首先标记会话系统变量，如果会话系统变量不存在，则标记全局系统变量。

- 查看指定的系统变量的值

  ```mysql
  SELECT @@global.变量名;
  ```

- 查看指定的会话变量的值

  ```mysql
  SELECT @@session.变量名;
  或
  SELECT @@变量名;
  ```

**修改系统变量的值(SELECT)**

- 修改MySQL配置文件，继而修改MySQL系统变量的值（该方法需要重启MySQL服务）
- 在MySQL服务运行期间，使用“set”命令重新设置系统变量的值

```mysql
# 为某个系统变量赋值
SET @@global.变量名=变量值;
SET GLOBAL 变量名=变量值;

# 为某个会话变量赋值
SET @@session.变量名=变量值;
SET SESSION 变量名=变量值;
```

###### 2. 用户自定义变量

- MySQL 中的用户变量以一个“@” 开头。
- 根据作用范围不同，又分为***会话用户变量***和***局部变量***。
- 会话用户变量：作用域和**会话变量**一样，只对当前连接会话有效。
- 局部变量：只在 BEGIN 和 END 语句块中有效。局部变量只能在**存储过程和函数**中使用。

**定义用户变量**

```mysql
# 方式1：“=” 或 “:=”
SET @用户变量 = 值;
SET @用户变量 := 值;

# 方式2：“:=” 或 INTO关键字
SELECT @用户变量 := 表达式 [FROM 等子句];
SELECT 表达式 INTO @用户变量 [FROM 等子句];
```

**查看用户变量的值（查看、比较、运算等）**

```mysql
SELECT @用户变量
```

**定义局部变量(DECLARE)**

- 定义：可以使用***DECLARE 语句***定义一个局部变量
- 作用域：仅仅在定义它的 BEGIN ... END 中有效
- 位置：只能放在 BEGIN ... END 中，而且只能放在第一句

```mysql
BEGIN
    #声明局部变量
    DECLARE 变量名1 变量数据类型 [DEFAULT 变量默认值];
    DECLARE 变量名2,变量名3,... 变量数据类型 [DEFAULT 变量默认值];
    
    #为局部变量赋值
    SET 变量名1 = 值;
    SELECT 值 INTO 变量名2 [FROM 子句];
    
    #查看局部变量的值
    SELECT 变量1,变量2,变量3;
END
```

##### 定义条件与处理程序

> 定义条件是事先定义程序执行过程中可能遇到的问题， 处理程序定义了在遇到问题时应当采取的处理方式，并且保证存储过程或函数在遇到警告或错误时能继续执行。这样可以增强存储程序处理问题的能力，避免程序异常停止运行。

###### 定义条件

> 定义条件就是**给MySQL中的错误码命名**，这有助于存储的程序代码更清晰。它将一个错误名字和指定的错误条件关联起来。这个名字可以随后被用在定义处理程序的DECLARE HANDLER 语句中。

```mysql
DECLARE 错误名称 CONDITION FOR 错误码（或错误条件）
```

###### 定义处理程序

> 可以为SQL执行过程中发生的某种类型的错误定义特殊的处理程序。

```mysql
DECLARE 处理方式 HANDLER FOR 错误类型 处理语句
```

- 处理方式：处理方式有3个取值：CONTINUE、EXIT、UNDO。

CONTINUE ：表示遇到错误不处理，继续执行。
EXIT ：表示遇到错误马上退出。
UNDO ：表示遇到错误后撤回之前的操作。MySQL中暂时不支持这样的操作。

- 错误类型（即条件）可以有如下取值：
  - SQLSTATE '字符串错误码' ：表示长度为5的sqlstate_value类型的错误代码；
  - MySQL_error_code ：匹配数值类型错误代码；
  - 错误名称：表示DECLARE ... CONDITION定义的错误条件名称。
  - SQLWARNING ：匹配所有以01开头的SQLSTATE错误代码；
  - NOT FOUND ：匹配所有以02开头的SQLSTATE错误代码；
  - SQLEXCEPTION ：匹配所有没有被SQLWARNING或NOT FOUND捕获的SQLSTATE错误代码；
- 处理语句：如果出现上述条件之一，则采用对应的处理方式，并执行指定的处理语句。语句可以是像“ SET 变量 = 值”这样的简单语句，也可以是使用BEGIN ... END 编写的复合语句。

##### 流程控制

> 解决复杂问题不可能通过一个 SQL 语句完成，我们需要执行多个 SQL 操作。流程控制语句的作用就是控制存储过程中 SQL 语句的执行顺序，是我们完成复杂操作必不可少的一部分。

###### 条件判断语句：IF语句和CASE语句

- IF语句

```mysql
IF 表达式1 THEN 操作1
[ELSEIF 表达式2 THEN 操作2]...
[ELSE 操作N]
END IF
```

- CASE语句

```mysql
#情况一：类似于switch
CASE 表达式
WHEN 值1 THEN 结果1或语句1(如果是语句，需要加分号)
WHEN 值2 THEN 结果2或语句2(如果是语句，需要加分号)
...
ELSE 结果n或语句n(如果是语句，需要加分号)
END [case]（如果是放在begin end中需要加上case，如果放在select后面不需要）

#情况二：类似于多重if
CASE
WHEN 条件1 THEN 结果1或语句1(如果是语句，需要加分号)
WHEN 条件2 THEN 结果2或语句2(如果是语句，需要加分号)
...
ELSE 结果n或语句n(如果是语句，需要加分号)
END [case]（如果是放在begin end中需要加上case，如果放在select后面不需要）
```

###### 循环语句：LOOP、WHILE和REPEAT语句

- 循环结构之LOOP

  > LOOP循环语句用来重复执行某些语句。LOOP内的语句一直重复执行直到循环被退出（使用LEAVE子句），跳出循环过程。

  ```mysql
  [loop_label:] LOOP
  循环执行的语句
  END LOOP [loop_label]
  ```


- 循环结构之WHILE

  > WHILE语句创建一个**带条件判断**的循环过程。WHILE在执行语句执行时，先对指定的表达式进行判断如果为真，就执行循环内的语句，否则退出循环。

  ```mysql
  [while_label:] WHILE 循环条件 DO
  	循环体
  END WHILE [while_label];
  ```

  ```mysql
  DELIMITER //

  CREATE PROCEDURE test_while()
  BEGIN
    DECLARE i INT DEFAULT 0;
    
    WHILE i < 10 DO
    	SET i = i + 1;
    END WHILE;
    
    SELECT i;
  END //

  DELIMITER ;
  #调用
  CALL test_while();
  ```

- 循环结构之REPEAT

  > REPEAT语句创建一个带条件判断的循环过程。与WHILE循环不同的是，REPEAT 循环**首先会执行一次循环**，然后在 UNTIL 中进行表达式的判断，如果满足条件就退出，即 END REPEAT；如果条件不满足，会就继续执行循环，直到满足退出条件为止。

  ```MYSQL
  [repeat_label:] REPEAT
  　　　　循环体的语句
  UNTIL 结束循环的条件表达式
  END REPEAT [repeat_label]
  ```

  ```MYSQL
  DELIMITER //
  
  CREATE PROCEDURE test_repeat()
  BEGIN
    DECLARE i INT DEFAULT 0;
    REPEAT
    
    SET i = i + 1;
    UNTIL i >= 10
    END REPEAT;
    
    SELECT i;
  END //
  
  DELIMITER ;
  ```

###### 跳转语句：ITERATE和LEAVE语句

- 跳转语句之LEAVE语句

  > LEAVE语句：可以用在循环语句内，或者以 BEGIN 和 END 包裹起来的程序体内，表示跳出循环或者跳出程序体的操作。类似break

  ```mysql
  LEAVE 标记名
  ```

- 跳转语句之ITERATE语句

  > ：只能用在循环语句（LOOP、REPEAT和WHILE语句）内，表示重新开始循环，将执行顺序转到语句段开头处。类似continue

  ```mydql
  ITERATE label
  ```

---

### MySQL高级篇

##### mysql的基本信息

- 查看mysql版本

  ```mysql
  mysql --version
  ```

- 查看mysql运行状态

  ```mysql
  ubuntu: systemctl status mysql.service
  centos: systemctl status mysqld.service
  启动：systemctl start mysqld.service
  关闭：systemctl stop mysqld.service
  重启：systemctl restart mysqld.service
  ```

- 修改密码

  ```mysql
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
  ```

- 修改Host为通配符%

  ```mysql
  update user set host = '%' where user ='root';
  flush privileges;
  ```

- 查看默认使用的字符集

  ```mysql
  show variables like 'character%';
  ```

- 修改字符集

  ```mysql
  vim /etc/mysql/my.cnf
  character_set_server=utf8

  1.修改已创建数据库的字符集:
  alter database dbtest1 character set 'utf8';

  2.修改已创建数据表的字符集:
  alter table t_emp convert to character set 'utf8';
  ```

- 各级别字符集

  - character_set_server：服务器级别的字符集
  - character_set_database：当前数据库的字符集
  - character_set_client：服务器解码请求时使用的字符集
  - character_set_connection：服务器处理请求时会把请求字符串从character_set_client转为character_set_connection
  - character_set_results：服务器向客户端返回数据时使用的字符集

##### mysql 的数据目录

- find / -name mysql

- show variables like 'datadir';

- mysql数据库文件的存放路径：/var/lib/mysql/

- mysql相关命令目录：/usr/bin (find . -name "mysql*")

- 配置文件目录：/etc/mysql

- mysql自带的系统数据库：

  1. mysql

     > MySQL 系统自带的核心数据库，它存储了MySQL的**用户账户和权限信息**，一些存储过程、事件的定义信息，一些运行过程中产生的日志信息，一些帮助信息以及时区信息等。

  2. information_schema

     > MySQL 系统自带的数据库，这个数据库保存着MySQL服务器维护的所有其他数据库的信息，比如有
     > 哪些表、哪些视图、哪些触发器、哪些列、哪些索引。这些信息并不是真实的用户数据，而是一些
     > 描述性信息，有时候也称之为元数据。在系统数据库information_schema 中提供了一些以
     > innodb_sys 开头的表，用于表示内部系统表。

  3. performance_schema

     > MySQL 系统自带的数据库，这个数据库里主要保存MySQL服务器运行过程中的一些状态信息，可以
     > 用来监控 MySQL 服务的各类性能指标。包括统计最近执行了哪些语句，在执行过程的每个阶段都
     > 花费了多长时间，内存的使用情况等信息。

  4. sys

     > MySQL 系统自带的数据库，这个数据库主要是通过视图的形式把information_schema 和
     > performance_schema 结合起来，帮助系统管理员和开发人员监控 MySQL 的技术性能。

##### 用户管理

- 登录mysql服务器

  ```
  mysql –h hostname|hostIP –P port –u username –p DatabaseName –e "SQL语句"
  ```

  - -h参数后面接主机名或者主机IP，hostname为主机，hostIP为主机IP。
  - -P参数后面接MySQL服务的端口，通过该参数连接到指定的端口。MySQL服务的默认端口是3306，
    不使用该参数时自动连接到3306端口，port为连接的端口号。
  - -u参数后面接用户名，username为用户名。
  - -p参数会提示输入密码。
  - DatabaseName参数指明登录到哪一个数据库中。如果没有该参数，就会直接登录到MySQL数据库中，然后可以使用USE命令来选择数据库。
  - -e参数后面可以直接加SQL语句。登录MySQL服务器以后即可执行这个SQL语句，然后退出MySQL服务器。

- 创建用户(CREATE USER)

  ```mysql
  CREATE USER 用户名 [IDENTIFIED BY '密码'][,用户名 [IDENTIFIED BY '密码']];
  ```

- 修改用户(UPDATE)

  ```mysql
  UPDATE mysql.user SET USER='xxx' WHERE USER='xxx';
  FLUSH PRIVILEGES;
  ```

- 删除用户(DROP USER)

  ```mysql
  DROP USER user[,user]...;
  FLUSH PRIVILEGES;

  DELETE FROM mysql.user WHERE Host=’hostname’ AND User=’username’;
  FLUSH PRIVILEGES;
  ```

- 设置当前用户密码(ALTER USER)

  ```mysql
  ALTER USER USER() IDENTIFIED BY 'new_password';
  ```

- 修改其他用户密码(ALTER USER)

  ```mysql
  使用ALTER语句来修改普通用户的密码:
  ALTER USER user [IDENTIFIED BY '新密码']
  [,user[IDENTIFIED BY '新密码']]…;
  
  使用SET命令来修改普通用户的密码:
  SET PASSWORD FOR 'username'@'hostname'='new_password';
  ```

##### 权限管理

- 查看所有权限

  ```mysql
  show privileges;
  ```

- 查看当前用户权限

  ```mysql
  SHOW GRANTS;
  SHOW GRANTS FOR CURRENT_USER;
  SHOW GRANTS FOR CURRENT_USER();
  ```

- 查看某用户的全局权限

  ```mysql
  SHOW GRANTS FOR 'user'@'主机地址' ;
  ```

- 授予权限(GRANT ... ON ... TO ...)

  ```mysql
  GRANT 权限1,权限2,…权限n ON 数据库名称.表名称 TO 用户名@用户地址 [IDENTIFIED BY ‘密码口令’];

  1. 给li4用户用本地命令行方式，授予atguigudb这个库下的所有表的插删改查的权限：
  GRANT SELECT,INSERT,DELETE,UPDATE ON atguigudb.* TO li4@localhost ;

  2. 授予通过网络方式登录的joe用户 ，对所有库所有表的全部权限，密码设为123。注意这里唯独不包
  括grant的权限：
  GRANT ALL PRIVILEGES ON *.* TO joe@'%' IDENTIFIED BY '123';
  ```

- 收回权限(REVOKE ... ON ... FROM ...)

  ```mysql
  REVOKE 权限1,权限2,…权限n ON 数据库名称.表名称 FROM 用户名@用户地址;
  
  1. 收回全库全表的所有权限
  REVOKE ALL PRIVILEGES ON *.* FROM joe@'%';
  
  2. 收回mysql库下的所有表的插删改查权限
  REVOKE SELECT,INSERT,UPDATE,DELETE ON mysql.* FROM joe@localhost;
  ```

###### db表

1. 用户列

  > db表用户列有3个字段，分别是Host、User、Db。这3个字段分别表示主机名、用户名和数据库
  > 名。表示从某个主机连接某个用户对某个数据库的操作权限，这3个字段的组合构成了db表的主键。

2. 权限列

  > Create_routine_priv和Alter_routine_priv这两个字段决定用户是否具有创建和修改存储过程的权限。

###### tables_priv表和columns_priv表

>tables_priv表用来对表设置操作权限，columns_priv表用来对表的某一列设置权限。

tables_priv表有8个字段，分别是Host、Db、User、Table_name、Grantor、Timestamp、Table_priv和
Column_priv，各个字段说明如下：

- Host 、Db 、User 和Table_name 四个字段分别表示主机名、数据库名、用户名和表名。
- Grantor表示修改该记录的用户。
- Timestamp表示修改该记录的时间。
- Table_priv 表示对象的操作权限。包括Select、Insert、Update、Delete、Create、Drop、Grant、
- References、Index和Alter。
- Column_priv字段表示对表中的列的操作权限，包括Select、Insert、Update和References。

###### procs_priv表

> procs_priv表可以对存储过程和存储函数设置操作权限。

##### user表

> 记录用户账户和权限信息

###### 1. 范围列（或用户列）

- host ： 表示连接类型
  - % 表示所有远程通过 TCP方式的连接
  - IP 地址 如 (192.168.1.2、127.0.0.1) 通过制定ip地址进行的TCP方式的连接
  - 机器名 通过制定网络中的机器名进行的TCP方式的连接
  - ::1 IPv6的本地ip地址，等同于IPv4的 127.0.0.1
  - localhost 本地方式通过命令行方式的连接 ，比如mysql -u xxx -p xxx 方式的连接。

###### 2. 权限列

- Grant_priv字段

  > 表示是否拥有GRANT权限

- Shutdown_priv字段

  >  表示是否拥有停止MySQL服务的权限

- Super_priv字段

  >  表示是否拥有超级权限

- Execute_priv字段

  > 表示是否拥有EXECUTE权限。拥有EXECUTE权限，可以执行存储过程和函数。

- Select_priv , Insert_priv等

  > 为该用户所拥有的权限。

###### 3. 安全列

> 安全列只有6个字段，其中两个是ssl相关的（ssl_type、ssl_cipher），用于加密；两个是x509
> 相关的（x509_issuer、x509_subject），用于标识用户；另外两个Plugin字段用于验证用户身份的插件，
> 该字段不能为空。如果该字段为空，服务器就使用内建授权验证机制验证用户身份。

###### 4. 资源控制列

> 资源控制列的字段用来限制用户使用的资源，包含4个字段，分别为：
> ①max_questions，用户每小时允许执行的查询操作次数；
>
> ②max_updates，用户每小时允许执行的更新操作次数； 
>
> ③max_connections，用户每小时允许执行的连接操作次数； 
>
> ④max_user_connections，用户允许同时建立的连接次数。

- 查看字段：

  ```mysql
  DESC mysql.user;
  ```

- 查看用户, 以列的方式显示数据：

  ```mysql
  SELECT * FROM mysql.user \G;
  ```

- 查询特定字段：

  ```mysql
  SELECT host,user,authentication_string,select_priv,insert_priv,drop_priv
  FROM mysql.user;
  ```

##### 角色管理(ROLE)

- 创建角色

  ```mysql
  CREATE ROLE 'role_name'[@'host_name'][, 'role_name'[@'host_name']]...
  ```

- 给角色赋予权限

  ```mysql
  GRANT privileges ON table_name TO 'role_name'[@'host_name'];
  ```

- 查看角色的权限

  ```mysql
  SHOW GRANTS FOR ''role_name;
  ```

- 回收角色的权限

  ```mysql
  REVOKE privileges ON tablename FROM 'rolename';
  ```

- 删除角色

  ```mysql
  DROP ROLE role [, role2]...
  ```

- 给用户赋予角色

  ```mysql
  GRANT role [, role2, ...] TO user [, user2, ...];
  ```

- 激活角色

  ```mysql
  方式1：使用set default role 命令激活角色
  SET DEFAULT ROLE ALL TO 'kangshifu'@'localhost';

  方式2：将activate_all_roles_on_login设置为ON
  show variables like 'activate_all_roles_on_login';
  SET GLOBAL activate_all_roles_on_login=ON;
  ```

- 撤销用户的角色

  ```mysql
  REVOKE role FROM user;
  ```

- 设置强制角色

  - 方式1：服务启动前设置

    ```mysql
    [mysqld]
    mandatory_roles='role1,role2@localhost,r3@%.atguigu.com'
    ```

  - 方式2：运行时设置

    ```mysql
    SET PERSIST mandatory_roles = 'role1,role2@localhost,r3@%.example.com'; #系统重启后仍然
    有效
    SET GLOBAL mandatory_roles = 'role1,role2@localhost,r3@%.example.com'; #系统重启后失效
    ```

##### MySQL的逻辑架构

###### 第一层：连接层

- 系统（客户端）访问MySQL 服务器前，做的第一件事就是建立***TCP 连接***。
- 经过三次握手建立连接成功后， MySQL 服务器对TCP 传输过来的**账号密码做身份认证、权限获取**。
  - 用户名或密码不对，会收到一个Access denied for user错误，客户端程序结束执行
  - 用户名密码认证通过，会从***权限表***查出账号拥有的权限与连接关联，之后的权限判断逻辑，都将依赖于此时读到的权限
- TCP 连接收到请求后，必须要***分配给一个线程***专门与这个客户端的交互。所以还会有个***线程池***，去走后面的流程。每一个连接从线程池中获取线程，省去了创建和销毁线程的开销。

###### 第二层：服务层

- SQL Interface: SQL接口
  - 接收用户的SQL命令，并且返回用户需要查询的结果。比如SELECT ... FROM就是调用SQL Interface
  - MySQL支持DML（数据操作语言）、DDL（数据定义语言）、存储过程、视图、触发器、自定
    义函数等多种SQL语言接口
- Parser: 解析器
  - 在解析器中对 SQL 语句进行***语法分析、语义分析***。***将SQL语句分解成数据结构***，并将这个结构传递到后续步骤，以后SQL语句的传递和处理就是基于这个结构的。如果在分解构成中遇到错误，那么就说明这个SQL语句是不合理的。
  - 在SQL命令传递到解析器的时候会***被解析器验证和解析***，并为其***创建语法树***，并**根据数据字典丰富查询语法树**，会验证该客户端是否具有执行该查询的权限。创建好语法树后，MySQL还会对SQl查询进行语法上的优化，进行查询重写。
- Optimizer: 查询优化器
  - SQL语句在语法解析之后、查询之前会使用查询优化器确定 SQL 语句的执行路径，生成一个***执行计划***。
  - 这个执行计划表明应该***使用哪些索引***进行查询（全表检索还是使用索引检索），表之间的连接顺序如何，最后会按照执行计划中的步骤调用存储引擎提供的方法来真正的执行查询，并将查询结果返回给用户。
  - 它使用“ 选取-投影-连接”策略进行查询。
- Caches & Buffers： 查询缓存组件
  - MySQL内部维持着一些Cache和Buffer，比如Query Cache用来缓存一条SELECT语句的执行结果，如果能够在其中找到对应的查询结果，那么就不必再进行查询解析、优化和执行的整个过程了，直接将结果反馈给客户端。
  - 这个缓存机制是由一系列小缓存组成的。比如表缓存，记录缓存，key缓存，权限缓存等 。
  - 这个查询缓存可以在不同客户端之间共享。
  - 从MySQL 5.7.20开始，不推荐使用查询缓存，并在MySQL 8.0中删除。

###### 第三层：引擎层

> 插件式存储引擎层（ Storage Engines），**真正的负责了MySQL中数据的存储和提取，对物理服务器级别**
> **维护的底层数据执行操作**，服务器通过API与存储引擎进行通信。不同的存储引擎具有的功能不同，这样
> 我们可以根据自己的实际需要进行选取。

- 查看引擎

  ```
  show engines;
  show engines \G;
  ```

##### SQL执行流程

- SQL语句->查询缓存->解析器->优化器->执行器

![请添加图片描述](https://img-blog.csdnimg.cn/2267957c4dd042658537fccdc944901e.png)


###### SQL语法顺序

| 手写                                                         | 机读                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| SELECT DISTINCT<br />          < select_list ><br /> FROM<br />           < left_table > < join_type ><br /> JOIN < right_table > ON < join_condition ><br /> WHERE<br />           < where_condition ><br /> GROUP BY<br />           < group_by_list ><br /> HAVING<br />           < having_condition ><br /> ORDER BY<br />           < order_by_condition ><br /> LIMIT < limit_number > | 1 FROM <left_table><br /> 2 ON <join_condition><br /> 3 <join_type> JOIN <right_table><br /> 4 WHERE <where_condition><br /> 5 GROUP BY <group_by_list><br /> 6 HAVING <having_condition><br /> 7 SELECT<br /> 8 DISTINCT <select_list><br /> 9 ORDER BY <order_by_condition><br /> 10 LIMIT <limit_number> |

##### 数据库缓冲池(buffer pool)

> InnoDB 存储引擎是***以页为单位***来管理存储空间的，我们进行的增删改查操作其实本质上都是在访问页面（包括读页面、写页面、创建新页面等操作）。而磁盘 I/O 需要消耗的时间很多，而在内存中进行操作，效率则会高很多，为了能让数据表或者索引中的数据随时被我们所用，DBMS 会申请占用内存来作为数据缓冲池，在真正访问页面之前，需要***把在磁盘上的页缓存到内存中的Buffer Pool***之后才可以访问。

- 查看缓冲池的大小

  ```mysql
  show variables like 'innodb_buffer_pool_size';
  ```

- 设置缓冲池的大小

  ```mysql
  set global innodb_buffer_pool_size = 268435456;
  
  [server]
  innodb_buffer_pool_size = 268435456
  ```

###### 多个Buffer Pool实例

- 查看缓冲池的个数

  ```mysql
  show variables like 'innodb_buffer_pool_instances';
  ```

- 设置缓冲池个数

  ```mysql
  [server]
  innodb_buffer_pool_instances = 2
  ```

##### 存储引擎

- 查看存储引擎

  ```mysql
  show engines;
  show engines \G;
  ```

- 查看默认的存储引擎

  ```mysql
  show variables like '%storage_engine%';
  SELECT @@default_storage_engine;
  ```

- 修改默认的存储引擎

  ```mysql
  SET DEFAULT_STORAGE_ENGINE=MyISAM;

  修改my.cnf文件：
  default-storage-engine=MyISAM
  # 重启服务
  systemctl restart mysqld.service
  ```

- 设置表的存储引擎

  1. 创建表时指定存储引擎

     ```mysql
     CREATE TABLE 表名（
     	建表语句；
     ） ENGINE = 存储引擎名称；
     ```

  2. 修改表的存储引擎

     ```mysql
     ALTER TABLE 表名 ENGINE = 存储引擎名称；
     ```
### MySQL补充篇
##### docker 配置mysql容器和远程链接

1. 拉取mysql镜像

   ```
   docker pull mysql
   ```

2. 根据镜像生成容器

   ```
   # docker run -d -p 3307:3306 -e MYSQL_ROOT_PASSWORD=123456 --name my_mysql mysql
   ```

3. 为mysql容器配置远程连接访问权限

   ```
   1. 进入容器：
   docker exec -it mysql bash
   2. 登录mysql：
   mysql -uroot -p123456
   3. 给root用户分配权限：
   alter user 'root'@'%' identified with mysql_native_password by '123456';
   4. 刷新权限：
   flush privileges;
   ```

##### mysql中的帮助命令

```
help command;
help statement;
```

##### navicat的使用

1.打开一个新的查询窗口: Ctrl + Q

2.关闭当前窗口:Ctrl + W

3.运行当前窗口的[SQL语句](https://so.csdn.net/so/search?q=SQL%E8%AF%AD%E5%8F%A5&spm=1001.2101.3001.7020):Ctrl + R

4.运行选中的SQL语句:Ctrl + Shift + R

5.注释选中SQL语句:Ctrl +　/

6.取消注释SQL:Ctrl + Shift + /

7.选中当前行SQL:三击鼠标

8.复制一行内容到下一行:Ctrl + D

9.删除当前行:Ctrl + L

10.在表内容显示页面切换到表设计页面:Ctrl + D

11.在表设计页面，快速切换到表内容显示页面:Ctrl + O

12.打开mysql命令行窗口:F6

13.刷新:F5

14. 全选：ctrl + a
15. 选择当前行：shift+end/home
16. 选择多行：
    1. ctrl+shift+home/end
    2. shift+向下的箭头

##### SQL关键词

###### SQL规范

1. 数据库名、表名、表的别名、变量名是严格区分大小写的；
2. 关键字、函数名、列名（字段名）、列的别名（字段的别名）忽略大小写；
3. **SQL关键字、函数名、变量**等都用大写来书写；
4. 数据库名、表名、表的别名，字段名、字段的别名等都用小写来书写；

###### DDL：数据定义语言

1. CREATE
   1. create database
   2. create table
   3. create view
   4. CREATE PROCEDURE
   5. CREATE FUNCTION
2. ALTER
3. DROP
4. RENAME
5. TRUNCATE

###### DML：数据操作语言

1. INSERT(INSERT INTO)
2. DELETE(DELETE FROM)
3. UPDATE
4. SELECT
5. DISTINCT
6. DESC
7. ORDER BY
8. GROUP BY
9. HAVING
10. LIMIT
11. AVG()
12. SUM()
13. COUNT()
14. MAX()
15. MIN()
16. CALL
17. SHOW
    1. SHOW DATABASES
    2. SHOW TABLES
    3. SHOW GLOBAL
    4. SHOW SESSION
    5. SHOW INDEX

###### DCL：数据控制语言

1. COMMIT
2. ROLLBACK
3. SAVEPOINT
4. GRANT
5. REVOKE
6. INDEX

###### 其他

1. FROM
2. WHERE
3. databases
4. tables
5. as
6. USE
7. SHOW
8. source
9. DESC
10. IFNULL
11. NULL
12. IS NULL
13. ISNULL
14. IS NOT NULL
15. LEAST
16. GREATEST
17. MOD
18. between ... and ...
19. not between ... and ...
20. and &&
21. or ||
22. not !
23. in
24. not in
25. like
26. ASC
27. DESC
28. LENGTH
29. IF
30. CASE WHEN ... THEN ... WHEN ... THEN ... ELSE ... END
31. CASE ... WHEN ... THEN ... WHEN ... THEN ... ELSE ... END
32. user()
33. version()
34. IF EXISTS
35. IF NOT EXISTS
36. CHARACTER SET

###### 字段类型

1. INT
2. VARCHAR()
3. DECIMAL(a,b)
4. PRIMARY KEY