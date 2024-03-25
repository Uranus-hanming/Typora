[toc]

### Flask框架

---

#### flask基本操作

- 啟動flask項目：python manage.py runserver
- 數據庫遷移命令創建數據庫：python manage.py db upgrade
- 部署程序依賴包及其精確的版本號：pip freeze >requirements.txt
- 在新的環境創建完全副本：pip install -r requirements.txt

#### flask上下文全局變量

- current_app:當前激活程序的程序實例
- g：處理請求時用作臨時存儲的對象。每次請求都會重設這個變量
- request:請求對象，封裝了客戶端發出的HTTP請求中的內容
- session:用戶會話，用於存儲請求之間需要“記住”的值的詞典

#### 請求鉤子

- before_first_request：注册一个函数，在处理第一个请求之前运行。

- before_request：注册一个函数，在每次请求之前运行。

- after_request：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。

- teardown_request：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。


在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量g。

#### Jinjia2變量過濾器

- safe 渲染值时不转义
- capitalize 把值的首字母转换成大写，其他字母转换成小写
- lower 把值转换成小写形式
- upper 把值转换成大写形式
- title 把值中每个单词的首字母都转换成大写
- trim 把值的首尾空格去掉
- striptags 渲染之前把值中所有的HTML 标签都删掉
- 

### Flask-SQLAlchemy管理数据库

#### 通過SQLAlchemy連接數據庫

```python
from sqlalchemy import create_engine

# 数据库的配置变量
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'xt_flask'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

# 创建数据库引擎
engine = create_engine(DB_URI)

#创建连接
with engine.connect() as con:
    rs = con.execute('SELECT 1')
    print rs.fetchone()
```

#### 创建`ORM`模型：

```python
from sqlalchemy import Column,Integer,String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'xt_flask'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

engine = create_engine(DB_URI,echo=True)

# 所有的类都要继承自`declarative_base`这个函数生成的基类
Base = declarative_base(engine)
class User(Base):
    # 定义表名为users
    __tablename__ = 'users'

    # 将id设置为主键，并且默认是自增长的
    id = Column(Integer,primary_key=True)
    # name字段，字符类型，最大的长度是50个字符
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(100))

    # 让打印出来的数据更好看，可选的
    def __repr__(self):
        return "<User(id='%s',name='%s',fullname='%s',password='%s')>" % (self.id,self.name,self.fullname,self.password)
```

#### 添加数据到表中

```python
Base.metadata.create_all()

# 添加数据到表中：和数据库打交道的，是一个叫做Session的对象：
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
# 或者
# Session = sessionmaker()
# Session.configure(bind=engine)
session = Session()
ed_user = User(name='ed',fullname='Ed Jones',password='edspassword')
session.add(ed_user)

# 现在只是把数据添加到session中，但是并没有真正的把数据存储到数据库中。如果需要把数据存储到数据库中，还要做一次commit操作：
session.commit()
```

#### 查找數據：通过`session.query()`方法实现

```python
for instance in session.query(User).order_by(User.id):
for instance in session.query(User.name):
for instance in session.query(User.name,User.fullname):
for instance in session.query(User,User.name).all():
for instance in session.query(User).order_by(User.id)[1:3]:
for name in session.query(User.name).filter_by(fullname='Ed Jones'):
for name in session.query(User.name).filter(User.fullname=='Ed Jones'):
```

#### Flask-SQLAlchemy第三方包和SQLAlchemy模块

###### models.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 配置 sqlalchemy 数据库驱动
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:qq5253@localhost:3306/people?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 初始化
db = SQLAlchemy(app)


# 创建数据库模型
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)

db.create_all()
```

###### user.py

```python
from models import db, User, app
from flask_cors import CORS

# 跨域配置
CORS(app)

@app.route("/")
def login():
    pass

# 增加单个数据
user = User(name='ming', age=26)
db.session.add(user)
db.session.commit()

# 增加多个数据
user1 = User(name='a', age=1)
user2 = User(name='b', age=2)
user3 = User(name='c', age=3)
db.session.add_all([user1, user2, user3])
db.session.commit()

# 查询一个数据
data = User.query.first()
print('User [id:{0},name:{1}]'.format(data.age, data.name))

# 查询所有数据
users = User.query.all()
for user in users:
    print('User [id:{0},name:{1}]'.format(user.age, user.name))

# 查询数据量
num = User.query.count()

# 按条件查询
user = User.query.filter_by(age=18)
# 按条件过滤
user0 = db.session.query(User).filter(User.name == "tom").first()
# 自动以主键查询
user1 = User.query.get(1)
# 按照组
user2 = User.query.group_by('age')
# 排序
user3 = User.query.order_by(User.age)
# 倒序排序
user4 = User.query.order_by(User.age.desc())

# 修改User模型中主键为 2 的记录
data = User.query.get(2)
data.age = 26
db.session.commit()

# 根据过滤条件进行修改
user5 = db.session.query(User).filter(User.name == "tom").first()
user5.age = 26
db.session.commit()

# 删除了 User模型中主键为 2 的记录
data = User.query.get(2)
db.session.delete(data)
db.session.commit()

# 删除全部
users = User.query.all()
for i in users:
    db.session.delete(i)
db.session.commit()
```



#### SQLAlchemy列类型

| 类型名       | Python类型         | 说　　明                                             |
| ------------ | ------------------ | ---------------------------------------------------- |
| Integer      | int                | 普通整数，一般是32 位                                |
| SmallInteger | int                | 取值范围小的整数，一般是16 位                        |
| BigInteger   | int 或long         | 不限制精度的整数                                     |
| Float        | float              | 浮点数                                               |
| Numeric      | decimal.Decimal    | 定点数                                               |
| String       | str                | 变长字符串                                           |
| Text         | str                | 变长字符串，对较长或不限长度的字符串做了优化         |
| Unicode      | unicode            | 变长Unicode 字符串                                   |
| UnicodeText  | unicode            | 变长Unicode 字符串，对较长或不限长度的字符串做了优化 |
| Boolean      | bool               | 布尔值                                               |
| Date         | datetime.date      | 日期                                                 |
| Time         | datetime.time      | 时间                                                 |
| DateTime     | datetime.datetime  | 日期和时间                                           |
| Interval     | datetime.timedelta | 时间间隔                                             |
| Enum         | str                | 一组字符串                                           |
| Pickle       | Type               | 任何Python 对象自动使用Pickle 序列化                 |
| LargeBinary  | str                | 二进制文件                                           |

#### SQLAlchemy列选项

- primary_key 如果设为True，这列就是表的主键
  unique 如果设为True，这列不允许出现重复的值
  index 如果设为True，为这列创建索引，提升查询效率
  nullable 如果设为True，这列允许使用空值；如果设为False，这列不允许使用空值
  default 为这列定义默认值

#### SQLAlchemy关系选项

- 选项名							说　　明
  backref 			在关系的另一个模型中添加反向引用
  primaryjoin 	明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定
  lazy					指定如何加载相关记录。可选值有select（首次访问时按需加载）、immediate（源对象加
  载后就加载）、joined（加载记录，但使用联结）、subquery（立即加载，但使用子查询），
  noload（永不加载）和dynamic（不加载记录，但提供加载记录的查询）
  uselist				 如果设为Fales，不使用列表，而使用标量值
  order_by 			指定关系中记录的排序方式
  secondary 		  指定多对多关系中关系表的名字
  secondaryjoin SQLAlchemy 	无法自行决定时，指定多对多关系中的二级联结条件

#### 常用的SQLAlchemy查询过滤器

- filter() 把过滤器添加到原查询上，返回一个新查询
- filter_by() 把等值过滤器添加到原查询上，返回一个新查询
- limit() 使用指定的值限制原查询返回的结果数量，返回一个新查询
- offset() 偏移原查询返回的结果，返回一个新查询
- order_by() 根据指定条件对原查询结果进行排序，返回一个新查询
- group_by() 根据指定条件对原查询结果进行分组，返回一个新查询

#### SQLAlchemy查询执行函数

- all() 以列表形式返回查询的所有结果
  first() 返回查询的第一个结果，如果没有结果，则返回None
  first_or_404() 返回查询的第一个结果，如果没有结果，则终止请求，返回404 错误响应
  get() 返回指定主键对应的行，如果没有对应的行，则返回None
  get_or_404() 返回指定主键对应的行，如果没找到指定的主键，则终止请求，返回404 错误响应
  count() 返回查询结果的数量
  paginate() 返回一个Paginate 对象，它包含指定范围内的结果

#### Flask-Migrate数据库迁移

- flask-migrate是基于Alembic进行的一个封装，并继承到Flask中，而所有的操作都是Alembic做的，它能跟踪模型的变化，并将变化映射到数据库中。
- 

#### Flask-Mail SMTP服务器的配置

- 配　　置				默认值						说　　明
  MAIL_SERVER 		localhost 	电子邮件服务器的主机名或IP 地址
  MAIL_PORT 			25 				电子邮件服务器的端口
  MAIL_USE_TLS 		False 		   启用传输层安全（Transport Layer Security，TLS）协议
  MAIL_USE_SSL 		False 		    启用安全套接层（Secure Sockets Layer，SSL）协议
  MAIL_USERNAME 	None		   邮件账户的用户名
  MAIL_PASSWORD 	None 		  邮件账户的密码

#### Flask 程序的基本结构

```
| - projectName
	| - app  //程序包
		| - templates //jinjia2模板
		|- static //css,js 图片等静态文件
		| - main  //py程序包 ，可以有多个这种包，每个对应不同的功能
			| - __init__.py
			|- errors.py
			|- forms.py
			|- views.py
		|- __init__.py
		|- email.py //邮件处理程序
		|- models.py //数据库模型
	|- migrations //数据迁移文件夹
	| - tests  //单元测试
		|- __init__.py
		|- test*.py //单元测试程序，可以包含多个对应不同的功能点测试
	|- venv  //虚拟环境
	|- requirements.txt //列出了所有依赖包以及版本号，方便在其他位置生成相同的虚拟环境以及依赖
	|- config.py //全局配置文件，配置全局变量
	|- manage.py //启动程序

```

- 4 个顶级文件夹

  1. Flask程序一般都保存在名为app 的包中；
  2. migrations文件夹包含数据库迁移脚本；
  3. 单元测试编写在 tests包中；
  4. venv文件夹包含 Python 虚拟环境。

- requirements.txt列出了所有依赖包，便于在其他电脑中重新生成相同的虚拟环境；

  ```
  命令自动生成文件:pip freeze >requirements.txt
  创建虚拟环境的完全副本:pip install -r requirements.txt
  ```

- config.py 存储配置；

- manage.py用于启动程序以及其他的程序任务。

#### Flask擴展

- Flask-Script：为Flask 程序添加了一个命令行解析器。Flask-Script 自带
  了一组常用选项，而且还支持自定义命令。

  ```python
  from flask.script import Manager
  manager = Manager(app)
  # ...
  if __name__ == '__main__':
  	manager.run()
  ```

- Jinja2模板引擎:

  ```python
  from flask import Flask, render_template
  # ...
  @app.route('/')
  def index():
  	return render_template('index.html')
  ```

- Flask-Bootstrap:Bootstrap（http://getbootstrap.com/）是Twitter 开发的一个开源框架，它提供的用户界面组件可用于创建整洁且具有吸引力的网页，而且这些网页还能兼容所有现代Web 浏览器。

  ```
  from flask.ext.bootstrap import Bootstrap
  # ...
  bootstrap = Bootstrap(app)
  ```

- Flask-Moment:本地化日期和时间

- Flask-WTF:可以把处理Web 表单的过程变成一种愉悦的体验。

- Flask-SQLAlchemy管理数据库：

  ```python
  from flask.sqlalchemy import SQLAlchemy
  basedir = os.path.abspath(os.path.dirname(__file__))
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir,'data.sqlite')
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
  db = SQLAlchemy(app)

  class User(db.Model):
      # 类变量__tablename__ 定义在数据库中使用的表名。
  	__tablename__ = 'users'
  	id = db.Column(db.Integer, primary_key=True)
  	username = db.Column(db.String(64), unique=True, index=True)
      
  	def __repr__(self):
  		return '<User %r>' % self.username
  ```

  - 創建表：db.create_all()

  - 刪除表：db.drop_all()

  - 插入行：

    ```python
    user_role = Role(name='User')
    db.session.add(user_role) / db.session.add_all([admin_role, mod_role, ...])
    db.session.commit()
    ```

  - 修改行

    ```
    >>> admin_role.name = 'Administrator'
    >>> db.session.add(admin_role)
    >>> db.session.commit()
    ```

  - 删除行

    ```
    >>> db.session.delete(mod_role)
    >>> db.session.commit()
    ```

  - 查询行:query 对象

    ```
    Role.query.all()
    User.query.filter_by(role=user_role).all()
    ```

- Flask-Migrate实现数据库迁移:

  ```python
  from flask_migrate import Migrate, MigrateCommand
  # ...
  migrate = Migrate(app, db)
  manager.add_command('db', MigrateCommand)
  ```

- Flask-Mail提供电子邮件支持:

  ```python
  from flask.mail import Message
  app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
  app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
  def send_email(to, subject, template, **kwargs):
  msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
  msg.body = render_template(template + '.txt', **kwargs)
  msg.html = render_template(template + '.html', **kwargs)
  mail.send(msg)
  ```

#### 創建藍圖

Blueprint把不同功能的module分开。

django中路由分配是将总路由通过include分配给app的urls.py路由文件，而**Flask是通过蓝图注册方式将蓝图添加到主app中**，user.py，admin.py主要是创建蓝图，然后为创建的蓝图添加路由配置，接着我们就可以在主路由文件manage.py中将我们创建的蓝图注册到主app中。

```python
__init.py
import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    from data_statistics import demo
    app.register_blueprint(demo.api)

    # 3.註冊藍圖
    if __name__ == '__main__':
        app.run(debug=True)


create_app()

```

```python
demo.py
from flask import Flask, Blueprint

# 1.實例化一個藍圖對象
api = Blueprint("api", __name__, url_prefix='/api')


# 2.藍圖定義的路由和視圖
@api.route("/index")
def index():
    return "hello world!"

# 訪問： http://127.0.0.1:5000/api/index
```

```python
# user.py
from flask import Blueprint
bp = Blueprint('user',__name__,url_prefix='/user/') # 'user':藍圖名

# 参数static_folder可以指定静态文件的路径
bp = Blueprint('admin',__name__,url_prefix='/admin',static_folder='static')
# 在构造函数Blueprint中有一个template_folder参数可以设置模板的路径
# Flask默认会去项目根目录下的templates文件夹中查找admin.html文件，如果找到了就直接返回，如果没有找到，才会去蓝图文件所在的目录下的templates文件夹中寻找。
bp = Blueprint('admin',__name__,url_prefix='/admin',template_folder='templates')

@bp.route('/')
def index():
    return "用户首页"

@bp.route('profile/')
def profile():
    return "个人简介"

# main.py
from flask import Flask
import user

app = Flask(__name__)
# 通过app.register_blueprint()方法将这个蓝图注册进url映射中
app.register_blueprint(user.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
```



#### 導包

- ##### from . import,“.” 代表使用相对路径导入，即从当前项目中寻找需要导入的包或函数

- .代表当前目录，..代表上一层目录，...代表上上层目录。

#### 數據庫遷移命令

```python
# 初始化迁移脚本文件夹
python manage.py db init
# 创建迁移脚本 在此你可以在迁移文件夹versions中检查脚本代码 自动迁移不一定总是正确的
python manage.py db migrate
# 确认无误 更新数据库
python manage.py db upgrade
```

```python
manage.py
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
```

#### Mysql的系统数据库

- **sys系统数据库**

  sys数据库里面包含了一系列的存储过程、自定义函数以及视图来帮助我们快速的了解系统的元数据信息。sys系统数据库结合了information_schema和performance_schema的相关数据，让我们更加容易的检索元数据。

- **performance_schema性能字典**

  此数据库为数据库性能优化提供重要的参考信息

- **INFORMATION_SCHEMA数据字典**

  INFORMATION_SCHEMA数据字典：此数据库存贮了其他所有数据库的信息（元数据）。元数据是关于数据的数据，如database name或table name，列的数据类型，或访问权限等。

- **mysql数据库**

  该数据库也是个核心数据库，存储用户的权限信息与帮助信息。

#### 路由保護 @login_required

为了保护路由只让认证用户访问，Flask-Login 提供了一个login_required 修饰器。如果未认证的用户访问这个路由，Flask-Login 会拦截请求，把用户发往登录页面。

```python
from flask_login import login_required
@app.route('/secret')
@login_required
def secret():
	return 'Only authenticated users are allowed!'
```

#### URL

```python
1. @app.route('/article/<converter:variable>/')
@app.route('/article/<id>/')
def article(id):
   return '%s article detail' % id

2. 接受两个URL
@app.route('/<any(article,blog):url_path>/')
def item(url_path):
  return url_path

3. ?=的形式来传递参数,例如：/article?id=xxx
- 通过request.args.get('id')来获取id的值
- post方法，则可以通过request.form.get('id')来进行获取

4. 指定HTTP方法：
@app.route('/login/',methods=['GET','POST'])
def login():
    return 'login'

5. 页面跳转和重定向：
- 永久性重定向：http的状态码是301
- 暂时性重定向：http的状态码是302
- 重定向是通过flask.redirect(location,code=302)这个函数来实现，location表示需要重定向到的URL，配合url_for()函数来使用

 from flask import Flask,url_for,redirect

 app = Flask(__name__)
 app.debug = True

 @app.route('/login/',methods=['GET','POST'])
 def login():
     return 'login page'

 @app.route('/profile/',methods=['GET','POST'])
 def profile():
     name = request.args.get('name')

     if not name:
     # 如果没有name，说明没有登录，重定向到登录页面
         return redirect(url_for('login'))
     else:
         return name
```

### Jinja2 模板

- 要渲染一个模板，通过`render_template`方法

```python
from flask import Flask,render_template
app = Flask(__name__)

@app.route('/about/')
def about():
    return render_template('about.html')
```

- 如果想更改模板文件地址，应该在创建`app`的时候，给`Flask`传递一个关键字参数`template_folder`，指定具体的路径

```python
from flask import Flask,render_template
app = Flask(__name__,template_folder=r'C:\templates')

@app.route('/about/')
def about():
    return render_template('about.html')
```

- 模板文件中有参数需要传递

```python
from flask import Flask,render_template
app = Flask(__name__)

@app.route('/about/')
def about():
    # return render_template('about.html',user='zhiliao')
    return render_template('about.html',**{'user':'zhiliao'})
```

- 模板中的邏輯處理

```jinja2
1. <html lang="en">
2. <head>
3.    <title>My Webpage</title>
4. </head>
5. <body>
6.     <ul id="navigation">
    	# {% ... %}：用来装载一个控制语句
7.     {% for item in navigation %}
8.         <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
9.     {% endfor %}
10.    </ul>
11.
    	# {{ ... }}：用来装载一个变量，模板渲染的时候，会把这个变量代表的值替换掉。
12.    {{ a_variable }}
13.    {{ user.name }}
14.    {{ user['name'] }}
15.
    	# {# ... #}：用来装载一个注释，模板渲染的时候会忽视这中间的值。
16.    {# a comment #}
17. </body>
18.</html>
```

- 过滤器是通过管道符号（`|`）进行使用的，例如：`{{ name|length }}`，将返回name的长度。过滤器相当于是一个函数，把当前的变量传入到过滤器中，然后过滤器根据自己的功能，再返回相应的值，之后再将结果渲染到页面中。
- include語句：把一个模板引入到另外一个模板中，类似于把一个模板的代码copy到另外一个模板的指定位置。
- 賦值（set）語句：在模板中添加变量

```jinja2
{% set name='zhiliao' %}

# 赋值为列表和元组
{% set navigation = [('index.html', 'Index'), ('about.html', 'About')] %}

# 赋值语句创建的变量在其之后都是有效的，如果不想让一个变量污染全局环境，可以使用with语句来创建一个内部的作用域，将set语句放在其中，这样创建的变量只在with代码块中才有效。
{% with %}
    {% set foo = 42 %}
    {{ foo }}           foo is 42 here
{% endwith %}
```

- 模板繼承：通过继承可以把模板中许多重复出现的元素抽取出来，放在父模板中，并且父模板通过定义`block`给子模板开一个口，子模板根据需要，再实现这个`block`
- 靜態文件的配置：通过`url_for`全局函数

```jinja2
<link href="{{ url_for('static',filename='about.css') }}">

# 在模板中引用蓝图，应该要使用蓝图名+.+static来引用
<link href="{{ url_for('admin.static',filename='about.css') }}">
```

- 類視圖

```python
from flask import views, render_template, request, Flask

app = Flask(__name__)


class LoginView(views.MethodView):
    # 当客户端通过get方法进行访问的时候执行的函数
    def get(self):
        return render_template("login.html")

    # 当客户端通过post方法进行访问的时候执行的函数
    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        if email == 'xx@qq.com' and password == '111111':
            return "登录成功！"
        else:
            return "用户名或密码错误！"


# 通过add_url_rule添加类视图和url的映射，并且在as_view方法中指定该url的名称，方便url_for函数调用
app.add_url_rule('/myuser/', view_func=LoginView.as_view('loginview'))
if __name__ == '__main__':
    app.run(debug=True)
```

### 零散知識點

```python
request.args.get() # 请求时，记录请求中的所有的参数，返回一个类字典格式数据类型。get请求是获取参数.
request.form.post() # 请求时， 记录请求中的所有的参数，返回一个类字典格式数据类型。post请求是获取请求体中参数.
return redirect(url_for('home')) # url_for对视图函数进行反转，第一个参数为视图函数名，如果视图函数有参数，可加在后面，返回url，redirect是重定向到括号里面的url，这里为url_for的返回值.
db.session.merge(data)
```