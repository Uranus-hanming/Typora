[toc]

#### 一、Django源码的前置知识

###### 安装插件

- python

- django

- remote-ssh

- SFTP

  - 打开方式：ctrl + shift + p
  - 上传：鼠标右键 -> upload file
  - sftp.json:

  ```json
  {
      "name": "My Server",
      "host": "localhost",
      "protocol": "sftp",
      "port": 8022,
      "username": "root",
      "password": "123456",
      "remotePath": "/root/work-project/first_project/first_django",
      "ignore": [
          ".vscode",
          ".git",
          ".DS_Store"
      ],
      "uploadOnSave": true,  
      "useTempFile": false,
      "openSsh": false
  }
  
  # "uploadOnSave": # 实时同步
  ```

###### 脚本文件配置

- 打开方式：运行 -> 打开配置

- 路径：.vscode/launch.json

- 脚本1：

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
  
  # python manage.py runserver 0.0.0.0:8000 --noreload
  # "justMyCode"：默认为True，配置为False时表示可以进入模块中进行断点
  ```

- 脚本2：

  ```json
  {
      // 使用 IntelliSense 了解相关属性。 
      // 悬停以查看现有属性的描述。
      // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
      "version": "0.2.0",
      "configurations": [
          {
              "name": "Python: Django",
              "type": "debugpy",
              "request": "launch",
              "program": "${workspaceRoot}/django/bin/django-admin.py",
              "cwd": "D:/typora/work-project",
              "env": {
                  "PYTHONPATH": "${workspaceRoot}"
              },
              "args": [
                  "startproject",
                  "first_django"
              ]
          }
      ]
  }
  
  # "env"：将环境变量修正为当前目录的配置
  # 含义：
  	cd 目录；
  	python django-admin.py startproject first_django
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

  > 在设置中找到格式化，勾选format on save

- 如何配置python虚拟环境？

- open recent: 打开最近文件

- 如何设置git?
  - 如何提交代码到远程仓库及下拉更新？
  - 如何查看提交历史完整记录信息？

###### 配置python解释器

在设置中搜索python，在Python:Default Interpreter Path中添加python.exe路径：

`C:/Users/hanming.qin/AppData/Local/Programs/Python/Python310/python.exe`

###### 魔法函数

- getattr

  ```python
  getattr(global_settings, setting)
  # 获取属性值，等同于 global_settings.settings
  ```

- setattr

  ```python
  setattr(cls, name, value)
  # 给cls对象设置属性值，即对象拥有了属性：setting=setting_value
  setattr(self, setting, setting_value)
  # 给self对象设置属性值，即对象拥有了属性：setting=setting_value
  ```

- isinstance

  ```python
  # 判断类型
  isinstance(setting_value, (list, tuple))
  ```

- dir

  > 返回一个对象的**属性**和**方法**列表

- hasattr

###### 元类

```python
from django.db import models
class Books(models.Model):
    pass

class Model(metaclass=ModelBase):
    pass

class ModelBase(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        # name：要创建的类名
        # bases：继承的父类
        # attrs：类的属性
        #return super().__new__(cls, name, bases, attrs)
        new_class._prepare()
        new_class._meta.apps.register_model(new_class._meta.app_label, new_class)
        return new_class
    
    def _prepare(cls):
        # from django.db.models.manager import Manager
        manager = Manager()  # 得到一个管理对象
        manager.auto_created = True
        cls.add_to_class("objects", manager)  # 模型类的objects属性
        
    def add_to_class(cls, name, value):
        setattr(cls, name, value)

from django.db.models.query import QuerySet
class Manager(BaseManager.from_queryset(QuerySet)):
    pass

class BaseManager:
    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        # 返回创建的动态类
        # 模型类.objects拥有所有QuerySet类所有方法的根本原因
        # 因此想要查看模型类管理器所拥有的方法，参考from django.db.models.query import QuerySet 的方法。
        return type(class_name, (cls,), {
            '_queryset_class': queryset_class,
            **cls._get_queryset_methods(queryset_class),
        })

```



###### 导入的模块含义

- from django.conf import settings

  ```
  <LazySettings "first_django.settings">
  工程项目中的settings.py文件
  ```

- `sys` 模块主要提供与Python解释器及其环境交互的一些功能

  - `sys.argv`：获取命令行参数列表，第一个元素是脚本名称
  - `sys.exit()`：以指定的状态码退出程序
  - `sys.stdin`、`sys.stdout`、`sys.stderr`：用于读取输入和输出
  - `sys.path`：包含模块搜索路径的列表
  - `sys.version`：获取Python解释器的版本信息

- `os` 模块主要用于与操作系统进行交互。提供了访问文件系统、执行系统命令等功能

  - `os.listdir()`：列出指定目录中的所有文件和目录

    ```python
    import os
    print(os.listdir('.'))  # 列出当前目录下的所有文件和目录
    ```

  - `os.mkdir()`：创建目录

  - `os.remove()`：删除文件

  - `os.path`：提供了一系列路径操作函数

    ```python
    print(os.path.join('dir', 'file.txt'))  # 输出 'dir/file.txt'
    print(os.path.abspath('file.txt'))  # 输出 'file.txt' 的绝对路径
    ```

  - `os.system()`：执行系统命令

    ```python
    os.system('echo Hello, World!')  # 在命令行打印 'Hello, World!'
    ```

  - `os.getenv()` 和 `os.putenv()`：获取和设置环境变量

  - 进程管理

    - `os.getpid()`：获取当前进程ID
    - `os.fork()` 和 `os.exec*()` 系列函数：用于创建和管理进程（仅在类 Unix 系统上可用）

  - os.walk(path)

    ```python
    for root, dirs, files in os.walk(path):
        pass
    ```

  - os.environ
  
    ```python
    # 设置环境变量 DJANGO_SETTINGS_MODULE 的默认值为 "first_django.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_django.settings")
    ```
  
    
  
- from importlib import import_module

  ```python
  # 以字符串的方式导入模块
  # mod是first_django.settings文件对象，可以通过 mod.属性名 来获取对象的key-value中的value值
  mod = import_module("first_django.settings")
  ```

  




#### 二、Django命令源码解析

###### django-admin startproject first_django

```
django\core\management\templates.py
	class TemplateCommand(BaseCommand):
		# 最终执行具体的业务逻辑的方法
		def handle(self, app_or_project, name, target=None, **options):
			pass

django\core\management\commands\startproject.py
	class Command(TemplateCommand):
		def handle(self, **options):
			# 执行的是父类 TemplateCommand 中的 handle()
			super().handle('project', project_name, target, **options)

django\core\management\base.py
	class BaseCommand:
		def execute(self, *args, **options):def execute(self, *args, **options):
			# self指的是django.core.management.commands.startproject.Command 对象
			# 执行的是Command类中的 handle 方法
			output = self.handle(*args, **options)

		def run_from_argv(self, argv):
			# self指的是django.core.management.commands.startproject.Command 对象
			# Command类中没有定义execute方法，就找父类 TemplateCommand，父类 TemplateCommand 也没有实现execute()，
			# 所以最终执行的是BaseCommand类中的execute()
			self.execute(*args, **cmd_options)

django\core\management\__init__.py
	class ManagementUtility:
		def load_command_class(app_name, name):
			# 以字符串的方式导入模块
		    module = import_module("%s.management.commands.%s" % (app_name, name))
		    # 实例化的是django\core\management\commands\startproject路径下的Command
		    return module.Command()

		def fetch_command(self, subcommand):
			# subcommand='startproject'
			# app_name='django.core'
			app_name = commands[subcommand]
			klass = load_command_class(app_name, subcommand)
			return klass  # 返回的是django.core.management.commands.startproject.Command 对象

		def execute(self):
			# 即子命令，本例子中为：startproject
			subcommand = self.argv[1]
			# 执行的实际是django.core.management.commands.startproject.Command对象run_from_argv()
			self.fetch_command(subcommand).run_from_argv(self.argv)

	def execute_from_command_line(argv=None):
		# argv=None
	    utility = ManagementUtility(argv)  # 实例化ManagementUtility
	    utility.execute()  # 执行ManagementUtility类的execute()

django-admin.py
执行命令：django-admin.py startproject second_django

	from django.core.management import execute_from_command_line
	sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
	sys.exit(execute_from_command_line())

```



###### django-admin startapp books



###### python 进入交互模式和 python manage.py shell的区别



###### python manage.py makemigrations



###### python manage.py migrate



###### python manage.py runserver 0.0.0.0:8000



#### 三、Django内置的ORM框架

- 数据库的配置信息位置：settings.py
- 默认的全局配置文件：django/conf/global_settings.py

###### 问题思考

1. QuerySet 是什么？
2. Django中的模型类为什么支持这样的链式操作？
3. 链式表达式是如何被翻译成SQL语句的，又该如何查看？
4. 为什么能对查询结果使用切片？当使用Django操作数据库时，懒查询指的是什么？
5. DjangoBooks为什么要通过objects属性才能调用all()、filter。等方法，为什么要通过objects 属性才能进行链式操作？

###### setting.py配置加载逻辑

```
django/conf/__init__.py
	class Settings:
		def __init__(self, settings_module):  # 'first_django.settings'
			# 先从 global_settings 导入属性，然后再从 first_django.settings 属性，如果属性名相同的会覆盖global_settings中的属性，
			# 因此给用户的感觉是配置会优先从first_django.settings中查找，找不到时才去global_settings中查找
			for setting in dir(global_settings):
	            if setting.isupper():
	                # self指的是Settings对象，这里的含义是将global_settings属性值赋给Settings对象
	                setattr(self, setting, getattr(global_settings, setting))
	        
	        self.SETTINGS_MODULE = settings_module
	        # 导入first_django.settings
	        mod = importlib.import_module(self.SETTINGS_MODULE)

	        for setting in dir(mod):
	            if setting.isupper():
	                setting_value = getattr(mod, setting)
	                setattr(self, setting, setting_value)

	class LazySettings(LazyObject):
		def _setup(self, name=None):
			# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_django.settings")  # manage.py文件中的配置
			# ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
			settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
			self._wrapped = Settings(settings_module)

		def __getattr__(self, name):
	        if self._wrapped is empty:
	            self._setup(name)
	        # self._wrapped是 Settings 对象，因此是去获取Settings对象中的属性
	        val = getattr(self._wrapped, name)
	        # 添加缓存，懒加载，获取属性的时候，会首先从__dict__里面获取。如果该属性存在就输出其值，如果不存在则会去找_getatrr_方法。
	        self.__dict__[name] = val
	        return val

		settings = LazySettings()

from django.conf import settings
# 获取数据库配置信息
settings.DATABASES  # 调用的是LazySettings对象的__getattr__方法
```

###### mysqlclient模块操作

```python
import MySQLdb
conn = MySQLdb.Connect(host='', port=3306, user='root', passwd='', db='', charset='utf8')
cursor = conn.cursor()
cursor.execute('sql原生语句')

cursor.fetchone()
cursor.fetchmany(5)
cursor.fetchall()
connection.commit() # cursor.execute()执行数据库修改的时候要执行commit()方法

cursor.close()
conn.close()
```

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

cursor.close()
conn.close()
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

