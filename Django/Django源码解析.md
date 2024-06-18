[toc]

#### 一、Django源码的前置知识

###### 脚本文件配置

- 路径：.vscode/launch.json

- 脚本：

  ```json
  {
      // 使用 IntelliSense 了解相关属性。 
      // 悬停以查看现有属性的描述。
      // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
      "version": "0.2.0",
      "configurations": [
          {
              "name": "Python 调试程序: Django",
              "type": "debugpy",
              "request": "launch",
              "args": [
                  "runserver",
                  "0.0.0.0:8000",
                  "--noreload"
              ],
              "django": true,
              "justMyCode": false,
              "autoStartBrowser": false,
              "program": "${workspaceFolder}\\manage.py"
          }
      ]
  }
  ```

###### vscode配置及快捷操作

- F5: debug模式运行
- shift + F5: 停止debug运行
- ctrl + F5: 非debug模式运行
- debug模式快捷键：
  - F5: 进入下一个断点
  - F10: 执行下一行代码
  - F11: 进入代码内部
  - shift + F11: 从代码内部出来
- ctrl + `: 打开终端和隐藏终端
- ctrl + shift + n: 打开新的终端
- 搜索：
  - search: 查询内容
  - files to include：可以在指定的文件中查询
  - files to exclude：可以排除文件进行搜索
- outline: 包含三种，分别为类、属性和方法
- 可以设置自动保存，及保存时自动格式化？
- 如何配置python虚拟环境？
- open recent: 打开最近文件
- 如何设置git?
  - 如何提交代码到远程仓库及下拉更新？
  - 如何查看提交历史完整记录信息？



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

- cache.get() -> \_\_getattr__()
- cache.set() -> \_\_setattr__()
- cache.delete() -> \_\_delattr__()
- cache['default'] -> \_\_getitem__()

cache == caches['default'] == django.core.cache.backends.locmem.LocMemCache()

cache.get() == LocMemCache().get()

```python
from django.utils.module_loading import import_string

# 可以写成模块路径，以字符串的形式进行导入
import_string("django.core.cache.backends.locmem.LocMemCache")
```

###### 邮件

```python
from django.core.mail import get_connection, send_mail

password = 'qinzghnwppchbqvbajh'
conn = get_connection(host='smtp.qq.com', username='973355982@qq.com', password=password)

send_mail('来自B站的邮件测试', '邮件内容信息，hello world!', from_email='973355982@qq.com', recipient_list=['2963545066@qq.com'], connection=conn)
```

- 发送多封邮件

```python
from django.core.mail.message import EmailMessage

subject = "这是多封邮件 - 主题"
body = "这是多封邮件 - 内容"
messages = []
for i in range(3):
    messages.append(EmailMessage(subject, body, '973355982@qq.com', to=['2963545066@qq.com'], cc=['973355982@qq.com'])

conn.send_messages(messages)
```

###### 文件处理

- 文件迁移

  ```
  from django.core.files.move import file_move_safe
  ```

- 



#### 六、Django的视图层



#### 七、Django的中间件原理



#### 八、Django中的辅助代码

