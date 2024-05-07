[toc]

#### 一、Django源码的前置知识



#### 二、Django命令原理解析



#### 三、Django内置的ORM框架

- 数据库的配置信息位置：settings.py
- 默认的全局配置文件：django/conf/global_settings.py

###### 问题思考

1. QuerySet 是什么？
2. Django中的模型类为什么支持这样的链式操作？
3. 链式表达式是如何被翻译成SQL语句的，又该如何查看？
4. 为什么能对查询结果使用切片？当使用Django操作数据库时，懒查询指的是什么？
5. DjangoBooks为什么要通过objects属性才能调用all()、filter。等方法，为什么要通过objects 属性才能进行链式操作？

###### 在django中执行原生SQL语句

```python
# 使用Django内置变量connection执行原生SQL语句来操作数据库
from django.db import connection

cursor = connection.cursor()
cursor.execute('select * from djang_books')
cursor.fetchone()
cursor.fetchmany(5)
cursor.fetchall()
connection.commit() # cursor.execute()执行数据库修改的时候要执行commit()方法
```

###### 重要的类

1. 基础类RawSQL：django/db/models/sql/query.py
2. 基础类Query：django/db/models/sql/query.py
3. 

#### 四、Django内置的模板系统



#### 五、Django核心模块的源码



#### 六、Django的视图层



#### 七、Django的中间件原理



#### 八、Django中的辅助代码

