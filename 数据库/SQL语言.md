[toc]

##### SQL

> **SQL** (Structured Query Language:结构化查询语言) 是用于管理***关系型数据库管理系统（RDBMS）***。 SQL 的范围包括***数据插入、查询、更新和删除***，数据库模式创建和修改，以及数据访问控制。

- SQL: Structured Query Language: 结构化查询语言
- RDBMS 指关系型数据库管理系统，全称 Relational Database Management System
- RDBMS 中的数据存储在被称为表的数据库对象中。
- 表是相关的数据项的集合，它由列和行组成。

##### SQL命令

- **SELECT** - 从数据库中提取数据
- **UPDATE** - 更新数据库中的数据
- **DELETE** - 从数据库中删除数据
- **INSERT INTO** - 向数据库中插入新数据
- **CREATE DATABASE** - 创建新数据库
- **ALTER DATABASE** - 修改数据库
- **CREATE TABLE** - 创建新表
- **ALTER TABLE** - 变更（改变）数据库表
- **DROP TABLE** - 删除表
- **CREATE INDEX** - 创建索引（搜索键）
- **DROP INDEX** - 删除索引

###### 1. SQL SELECT 语句 - 从数据库中选取数据

- SELECT 语句用于从数据库中选取数据。
- 结果被存储在一个结果表中，称为***结果集***。

```sql
SELECT column_name,column_name
FROM table_name;
SELECT * FROM table_name;
```

###### 2. SQL SELECT DISTINCT 语句 - 返回唯一不同的值 

- SELECT DISTINCT 语句用于返回唯一不同的值。

```mysql
SELECT DISTINCT country FROM Websites;
```

###### 3. SQL WHERE 子句 - 过滤记录

- WHERE 子句用于***过滤记录***，提取那些满足指定条件的记录。
- SQL 使用单引号来环绕**文本值**（大部分数据库系统也接受双引号）。如果是**数值字段**，请不要使用引号。

WHERE子句中的运算符：

| 运算符  | 描述                                                       |
| ------- | ---------------------------------------------------------- |
| =       | 等于                                                       |
| <>      | 不等于。**注释：**在 SQL 的一些版本中，该操作符可被写成 != |
| >       | 大于                                                       |
| <       | 小于                                                       |
| >=      | 大于等于                                                   |
| <=      | 小于等于                                                   |
| BETWEEN | 在某个范围内                                               |
| LIKE    | 搜索某种模式                                               |
| IN      | 指定针对某个列的多个可能值                                 |
| and     | 与，同时满足两个条件的值                                   |
| or      | 或，满足其中一个条件的值                                   |
| not     | 非，满足不包含该条件的值                                   |
| is null | 空值判断                                                   |

```sql
Select * from emp where comm is null;	查询 emp 表中 comm 列中的空值。
Select * from emp where sal between 1500 and 3000;	查询 emp 表中 SAL 列中大于 1500 的小于 3000 的值。
Select * from emp where sal in (5000,3000,1500);	查询 EMP 表 SAL 列中等于 5000，3000，1500 的值。
Select * from emp where ename like 'M%';	查询 EMP 表中 Ename 列中有 M 的值，M 为要查询内容中的模糊信息。
 % 表示多个字值，_ 下划线表示一个字符；
 M% : 通配符，正则表达式，表示的意思为模糊查询信息为 M 开头的。
 %M% : 表示查询包含M的所有内容。
 %M_ : 表示查询以M在倒数第二位的所有内容。
```

###### 4. SQL AND & OR 运算符 - 基于一个以上的条件对记录进行过滤

- AND & OR 运算符用于基于一个以上的条件对记录进行过滤。

```sql
SELECT * FROM Websites
WHERE alexa > 15
AND (country='CN' OR country='USA');
```

###### 5. SQL ORDER BY 关键字 - 对结果集进行排序

- ORDER BY 关键字用于对结果集进行排序。
- ORDER BY 关键字用于对结果集按照一个列或者多个列进行排序。
- ORDER BY 关键字***默认按照升序***对记录进行排序。如果需要按照降序对记录进行排序，您可以使用 DESC 关键字。

```sql
SELECT * FROM Websites
ORDER BY alexa DESC;	Descending

SELECT * FROM Websites
ORDER BY country,alexa;		按照 "country" 和 "alexa" 列排序
```

###### 6. SQL INSERT INTO 语句 - 向表中插入新记录

- INSERT INTO 语句用于向表中插入新记录。

1. 第一种形式无需指定要插入数据的列名，只需提供被插入的值即可：

   ```sql
   INSERT INTO table_name
   VALUES (value1,value2,value3,...);
   ```

2. 第二种形式需要指定列名及被插入的值：

   ```sql
   INSERT INTO table_name (column1,column2,column3,...)
   VALUES (value1,value2,value3,...);
   ```

###### 7. SQL UPDATE 语句 - 更新表中已存在的记录

- UPDATE 语句用于更新表中已存在的记录。

```sql
UPDATE table_name
SET column1=value1,column2=value2,...
WHERE some_column=some_value;
```

###### 8. SQL DELETE FROM 语句 - 用于删除表中的行

- DELETE 语句用于删除表中的记录。

```sql
DELETE FROM table_name
WHERE some_column=some_value;

在不删除表的情况下，删除表中所有的行。这意味着表结构、属性、索引将保持不变：
DELETE FROM table_name;
```

###### 9. LIMIT - 用于规定要返回的记录的数目

```sql
SELECT column_name(s)
FROM table_name
LIMIT number;
```

###### 10. SQL LIKE 操作符 - 用于在 WHERE 子句中搜索列中的指定模式

- LIKE 操作符用于在 WHERE 子句中搜索列中的指定模式。

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name LIKE pattern;
```

| 通配符                       | 描述                       |
| ---------------------------- | -------------------------- |
| %                            | 替代 0 个或多个字符        |
| _                            | 替代一个字符               |
| [*charlist*]                 | 字符列中的任何单一字符     |
| [^*charlist*]或[!*charlist*] | 不在字符列中的任何单一字符 |

- MySQL 中使用 **REGEXP** 或 **NOT REGEXP** 运算符 (或 RLIKE 和 NOT RLIKE) 来操作正则表达式。

```sql
选取 name 以 "G"、"F" 或 "s" 开始的所有网站：
SELECT * FROM Websites
WHERE name REGEXP '^[GFs]';

选取 name 以 A 到 H 字母开头的网站：
SELECT * FROM Websites
WHERE name REGEXP '^[A-H]';

选取 name 不以 A 到 H 字母开头的网站：
SELECT * FROM Websites
WHERE name REGEXP '^[^A-H]';
```

###### 11. SQL IN 操作符 - 允许您在 WHERE 子句中规定多个值

- IN 操作符允许您在 WHERE 子句中规定多个值。

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name IN (value1,value2,...);
```

###### 12. SQL BETWEEN 操作符 - 用于选取介于两个值之间的数据范围内的值

- BETWEEN 操作符选取介于两个值之间的数据范围内的值。这些值可以是数值、文本或者日期。

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name BETWEEN value1 AND value2;
```

###### 13. SQL 别名 as - 为表名称或列名称指定别名

- 通过使用 SQL，可以为表名称或列名称指定别名，创建别名是为了让列名称的可读性更强。
- 在查询中涉及超过一个表
- 在查询中使用了函数
- 列名称很长或者可读性差
- 需要把两个列或者多个列结合在一起

1. 列的 SQL 别名语法：

   ```sql
   SELECT column_name AS alias_name
   FROM table_name;

   把三个列（url、alexa 和 country）结合在一起，并创建一个名为 "site_info" 的别名：
   SELECT name, CONCAT(url, ', ', alexa, ', ', country) AS site_info
   FROM Websites;
   ```

2. 表的 SQL 别名语法：

   ```sql
   SELECT column_name(s)
   FROM table_name AS alias_name;
   
   使用 "Websites" 和 "access_log" 表，并分别为它们指定表别名 "w" 和 "a"（通过使用别名让 SQL 更简短）：
   SELECT w.name, w.url, a.count, a.date
   FROM Websites AS w, access_log AS a
   WHERE a.site_id=w.id and w.name="菜鸟教程";
   ```

###### 14. SQL 连接(JOIN) - 用于把来自两个或多个表的行结合起来

- SQL JOIN 子句用于把来自两个或多个表的行结合起来，基于这些表之间的共同字段。
- **INNER JOIN**：如果表中有至少一个匹配，则返回行
- **LEFT JOIN**：即使右表中没有匹配，也从左表返回所有的行
- **RIGHT JOIN**：即使左表中没有匹配，也从右表返回所有的行
- **FULL JOIN**：只要其中一个表中存在匹配，则返回行

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传
![在这里插入图片描述](https://img-blog.csdnimg.cn/c95e186982124769b92326f666696314.png#pic_center)



1. LEFT JOIN

   ```sql
   SELECT <select_list>
   FROM tableA
   LEFT JOIN tableB
   ON A.key=B.key
   ```

2. LEFT JOIN ... WHERE

   ```sql
   SELECT <select_list>
   FROM tableA
   LEFT JOIN tableB
   ON A.key=B.key
   WHERE B.key IS NULL
   ```

3. INNER JOIN = JOIN

   ```sql
   SELECT <select_list>
   FROM tableA
   INNER JOIN tableB
   ON A.key=B.key

   SELECT <select_list>
   FROM tableA
   JOIN tableB
   ON A.key=B.key
   ```

4. RIGHT JOIN

   ```sql
   SELECT <select_list>
   FROM tableA
   RIGHT JOIN tableB
   ON A.key=B.key
   ```

5. RIGHT JOIN ... WHERE

   ```sql
   SELECT <select_list>
   FROM tableA
   RIGHT JOIN tableB
   ON A.key=B.key
   WHERE A.key IS NULL
   ```

6. FULL OUTER JOIN

   ```sql
   SELECT <select_list>
   FROM tableA
   FULL OUTER JOIN tableB
   ON A.key=B.key
   ```

7. FULL OUTER JOIN ... WHERE

   ```sql
   SELECT <select_list>
   FROM tableA
   FULL OUTER JOIN tableB
   ON A.key=B.key
   WHERE A.key IS NULL
   OR B.key IS NULL
   ```

###### 14.1 SQL INNER JOIN 关键字

- INNER JOIN 关键字在表中存在至少一个匹配时返回行。

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传
![在这里插入图片描述](https://img-blog.csdnimg.cn/ffeaacf451cf43eebcbfcd8661b2dbb0.gif#pic_center)


```sql
SELECT column_name(s)
FROM table1
INNER JOIN table2
ON table1.column_name=table2.column_name;

或：

SELECT column_name(s)
FROM table1
JOIN table2
ON table1.column_name=table2.column_name;
```

###### 14.2 SQL LEFT JOIN 关键字

- LEFT JOIN 关键字从左表（table1）返回所有的行，即使右表（table2）中没有匹配。如果右表中没有匹配，则结果为 NULL。

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传
![在这里插入图片描述](https://img-blog.csdnimg.cn/547e52d054d54188ba739ef64ecdaef6.gif#pic_center)


```sql
SELECT column_name(s)
FROM table1
LEFT JOIN table2
ON table1.column_name=table2.column_name;

或：

SELECT column_name(s)
FROM table1
LEFT OUTER JOIN table2
ON table1.column_name=table2.column_name;
```

###### 14.3 SQL RIGHT JOIN 关键字

- RIGHT JOIN 关键字从右表（table2）返回所有的行，即使左表（table1）中没有匹配。如果左表中没有匹配，则结果为 NULL。

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传
![在这里插入图片描述](https://img-blog.csdnimg.cn/4bbf6b2daa7f49b2a1ada4361a730dfb.gif#pic_center)


```sql
SELECT column_name(s)
FROM table1
RIGHT JOIN table2
ON table1.column_name=table2.column_name;

或：

SELECT column_name(s)
FROM table1
RIGHT OUTER JOIN table2
ON table1.column_name=table2.column_name;
```

###### 14.4 SQL FULL OUTER JOIN 关键字

- FULL OUTER JOIN 关键字只要左表（table1）和右表（table2）其中一个表中存在匹配，则返回行.
- FULL OUTER JOIN 关键字结合了 LEFT JOIN 和 RIGHT JOIN 的结果。
- MySQL中不支持 FULL OUTER JOIN

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传
![在这里插入图片描述](https://img-blog.csdnimg.cn/cfbac1bfe53e4ead82350cbe6eb2143b.gif#pic_center)



###### 15. SQL UNION 操作符 - 合并两个或多个 SELECT 语句的结果

- UNION 操作符用于合并两个或多个 SELECT 语句的结果集。
- UNION 内部的每个 SELECT 语句必须拥有相同数量的列。列也必须拥有相似的数据类型。同时，每个 SELECT 语句中的列的顺序必须相同。
- 默认地，UNION 操作符选取不同的值。如果允许重复的值，请使用 UNION ALL。

1. SQL UNION 语法：

   ```sql
   SELECT column_name(s) FROM table1
   UNION
   SELECT column_name(s) FROM table2;
   ```

2. SQL UNION ALL 语法：

   ```sql
   SELECT column_name(s) FROM table1
   UNION ALL
   SELECT column_name(s) FROM table2;
   ```

###### 16. SQL SELECT INTO 语句 - 从一个表复制信息到另一个表

- SELECT INTO 语句从一个表复制数据，然后把数据插入到另一个新表中。
- MySQL 数据库不支持 SELECT ... INTO 语句，但支持 [INSERT INTO ... SELECT](https://www.runoob.com/sql/sql-insert-into-select.html) 。

```sql
CREATE TABLE 新表
AS
SELECT * FROM 旧表 
```

###### 17. SQL INSERT INTO SELECT 语句 - 从一个表复制信息到另一个表

- INSERT INTO SELECT 语句从一个表复制数据，然后把数据插入到一个已存在的表中。目标表中任何已存在的行都不会受影响。

1. 从一个表中复制所有的列插入到另一个已存在的表中：

   ```sql
   INSERT INTO table2
   SELECT * FROM table1;
   ```

2. 只复制希望的列插入到另一个已存在的表中：

   ```sql
   INSERT INTO table2
   (column_name(s))
   SELECT column_name(s)
   FROM table1;
   ```

###### 18. SQL CREATE DATABASE 语句 - 用于创建数据库

```sql
CREATE DATABASE dbname;
```

###### 19. SQL CREATE TABLE 语句 - 创建数据库中的表

```sql
CREATE TABLE table_name
(
column_name1 data_type(size),
column_name2 data_type(size),
column_name3 data_type(size),
....
);
```

###### 20. SQL 约束（Constraints）

- SQL 约束用于规定表中的数据规则。
- 如果存在违反约束的数据行为，行为会被约束终止。
- 约束可以在创建表时规定（通过 CREATE TABLE 语句），或者在表创建之后规定（通过 ALTER TABLE 语句）。

```sql
CREATE TABLE table_name
(
column_name1 data_type(size) constraint_name,
column_name2 data_type(size) constraint_name,
column_name3 data_type(size) constraint_name,
....
);
```

| 约束类型                                    | 描述                                                         |
| :------------------------------------------ | ------------------------------------------------------------ |
| **NOT NULL**                                | 指示某列不能存储 NULL 值。                                   |
| **UNIQUE**                                  | 保证某列的每行必须有唯一的值。                               |
| **PRIMARY KEY** - NOT NULL 和 UNIQUE 的结合 | 确保某列（或两个列多个列的结合）有唯一标识，有助于更容易更快速地找到表中的一个特定的记录。 |
| **FOREIGN KEY**                             | 保证一个表中的数据匹配另一个表中的值的参照完整性。           |
| **CHECK**                                   | 保证列中的值符合指定的条件。                                 |
| **DEFAULT**                                 | 规定没有给列赋值时的默认值。                                 |

###### 21. SQL CREATE INDEX 语句 - 用于在表中创建索引

- 可以在表中创建索引，以便更加快速高效地查询数据。
- 用户无法看到索引，它们只能被用来加速搜索/查询。
- 更新一个包含索引的表需要比更新一个没有索引的表花费更多的时间，这是由于索引本身也需要更新。因此，理想的做法是仅仅在常常被搜索的列（以及表）上面创建索引。

1. 在表上创建一个简单的索引。允许使用重复的值：

   ```sql
   CREATE INDEX index_name
   ON table_name (column_name)
   ```

2. 在表上创建一个唯一的索引。不允许使用重复的值：唯一的索引意味着两个行不能拥有相同的索引值。

   ```
   CREATE UNIQUE INDEX index_name
   ON table_name (column_name)
   ```

###### 22. SQL 撤销索引、撤销表以及撤销数据库

1. DROP INDEX 语句

   ```mysql
   ALTER TABLE table_name DROP INDEX index_name
   ```

2. DROP TABLE 语句

   ```sql
   DROP TABLE table_name
   ```

3. DROP DATABASE 语句

   ```sql
   DROP DATABASE database_name
   ```

4. TRUNCATE TABLE 语句 - 仅仅需要删除表内的数据，但并不删除表本身

   ```sql
   TRUNCATE TABLE table_name
   ```

###### 23. SQL ALTER TABLE 语句 - 在已有的表中添加、删除或修改列

1. 在表中添加列：

   ```mysql
   ALTER TABLE table_name
   ADD column_name datatype
   ```

2. 删除表中的列：

   ```mysql
   ALTER TABLE table_name
   DROP COLUMN column_name
   ```

3. 改变表中列的数据类型：

   ```mysql
   ALTER TABLE table_name
   MODIFY COLUMN column_name datatype
   ```

###### 24. SQL AUTO_INCREMENT 字段 - 新记录插入表中时生成一个唯一的数字

- 在每次插入新记录时，自动地创建主键字段的值。

```mysql
CREATE TABLE Persons
(
ID int NOT NULL AUTO_INCREMENT,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255),
PRIMARY KEY (ID)
)

让 AUTO_INCREMENT 序列以其他的值起始:
ALTER TABLE Persons AUTO_INCREMENT=100
```

###### 25. SQL 视图（Views）

- 在 SQL 中，视图是基于 SQL 语句的结果集的可视化的表。
- 视图包含行和列，就像一个真实的表。视图中的字段就是来自一个或多个数据库中的真实的表中的字段。
- 可以向视图添加 SQL 函数、WHERE 以及 JOIN 语句，也可以呈现数据，就像这些数据来自于某个单一的表一样。

1. 创建视图

   ```sql
   CREATE VIEW view_name AS
   SELECT column_name(s)
   FROM table_name
   WHERE condition
   ```

2. 更新视图

   ```sql
   CREATE OR REPLACE VIEW view_name AS
   SELECT column_name(s)
   FROM table_name
   WHERE condition
   ```

3. 撤销视图

   ```sql
   DROP VIEW view_name
   ```

##### SQL Aggregate 函数

###### 1. SQL AVG() 函数 - 返回数值列的平均值

```sql
SELECT AVG(column_name) FROM table_name
```

###### 2. SQL COUNT() 函数 - 返回匹配指定条件的行数

1. COUNT(column_name) 函数返回指定列的值的数目（NULL 不计入）：

```sql
SELECT COUNT(column_name) FROM table_name;
```

2. COUNT(*) 函数返回表中的记录数：

```sql
SELECT COUNT(*) FROM table_name;
```

3. COUNT(DISTINCT column_name) 函数返回指定列的不同值的数目：

```sql
SELECT COUNT(DISTINCT column_name) FROM table_name;
```

###### 3. SQL FIRST() 函数 - 返回指定的列中第一个记录的值

```sql
SELECT FIRST(column_name) FROM table_name;

mysql:
SELECT column_name FROM table_name
ORDER BY column_name ASC
LIMIT 1;
```

###### 4. SQL LAST() 函数 - 返回指定的列中最后一个记录的值

```sql
SELECT LAST(column_name) FROM table_name;

mysql:
SELECT column_name FROM table_name
ORDER BY column_name DESC
LIMIT 1;
```

###### 5. SQL MAX() 函数 - 返回指定列的最大值

```sql
SELECT MAX(column_name) FROM table_name;
```

###### 6. SQL MIN() Function - 返回指定列的最小值。

```sql
SELECT MIN(column_name) FROM table_name;
```

###### 7. SQL SUM() 函数 - 返回数值列的总数。

```sql
SELECT SUM(column_name) FROM table_name;
```

###### 8. SQL GROUP BY 语句 - 用于结合聚合函数，根据一个或多个列对结果集进行分组

- GROUP BY 语句可结合一些聚合函数来使用
- GROUP BY 语句用于结合聚合函数，根据一个或多个列对结果集进行分组。

```sql
SELECT column_name, aggregate_function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name;

多表连接：
SELECT Websites.name,COUNT(access_log.aid) AS nums FROM access_log
LEFT JOIN Websites
ON access_log.site_id=Websites.id
GROUP BY Websites.name;
```

###### 9. SQL HAVING 子句 - 可以让我们筛选分组后的各组数据

- 在 SQL 中增加 HAVING 子句原因是，WHERE 关键字无法与聚合函数一起使用。
- HAVING 子句可以让我们筛选分组后的各组数据。

```sql
SELECT column_name, aggregate_function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name
HAVING aggregate_function(column_name) operator value;
```

###### 10. SQL EXISTS 运算符 - 判断查询子句是否有记录

- EXISTS 运算符用于判断查询子句是否有记录，如果有一条或多条记录存在返回 True，否则返回 False。

```sql
SELECT column_name(s)
FROM table_name
WHERE EXISTS
(SELECT column_name FROM table_name WHERE condition);
```

- EXISTS 可以与 NOT 一同使用，查找出不符合查询语句的记录：

```sql
SELECT Websites.name, Websites.url 
FROM Websites 
WHERE NOT EXISTS (SELECT count FROM access_log WHERE Websites.id = access_log.site_id AND count > 200);
```

###### 11. SQL UCASE() 函数 - 把字段的值转换为大写

```sql
SELECT UCASE(column_name) FROM table_name;
```

###### 12. SQL LCASE() 函数 - 把字段的值转换为小写

```sql
SELECT LCASE(column_name) FROM table_name;
```

###### 13. SQL MID() 函数 - 从文本字段中提取字符

```sql
SELECT MID(column_name,start[,length]) FROM table_name;
```

| 参数        | 描述                                                        |
| ----------- | ----------------------------------------------------------- |
| column_name | 必需。要提取字符的字段。                                    |
| start       | 必需。规定开始位置（起始值是 1）。                          |
| length      | 可选。要返回的字符数。如果省略，则 MID() 函数返回剩余文本。 |

###### 14. SQL LEN() 函数 - 返回文本字段中值的长度

```sql
SELECT LENGTH(column_name) FROM table_name;
```

###### 15. SQL ROUND() 函数 - 把数值字段舍入为指定的小数位数 

```sql
SELECT ROUND(column_name,decimals) FROM TABLE_NAME;
```

| 参数        | 描述                         |
| ----------- | ---------------------------- |
| column_name | 必需。要舍入的字段。         |
| decimals    | 可选。规定要返回的小数位数。 |

###### 16. SQL NOW() 函数 - 返回当前系统的日期和时间 

```sql
SELECT NOW() FROM table_name;
```

###### 17. SQL FORMAT() 函数 - 对字段的显示进行格式化 

```sql
SELECT FORMAT(column_name,format) FROM table_name;
```

| 参数        | 描述                   |
| ----------- | ---------------------- |
| column_name | 必需。要格式化的字段。 |
| format      | 必需。规定格式。       |