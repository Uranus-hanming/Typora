[toc]
##### flask的基本模块

###### 1.request

> 請求對象，封裝了客戶端發出的HTTP請求中的內容

```python
from flask import request
```

###### 2.current_app

> 当前激活程序的程序实例

###### 3.g

> 處理請求時用作臨時存儲的對象。每次請求都會重設這個變量

```
from flask import g
```

###### 4.session

> 用戶會話，用於存儲請求之間需要“記住”的值的詞典



##### flask_sqlalchemy的使用

> flask_sqlalchemy是Flask框架的一个插件；
>
> flask_sqlalchemy的使用是对SQLAlchemy进行封装和优化，使得我们在Flask中使得sqlalchemy更加简单。

###### 安装

```shell
pip install flask_sqlalchemy
```

###### 数据库连接

```python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

DB_RUI = 'mysql+pymysql://user:password@host:port/database?charset=utf8'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)
```

###### 创建ORM模型类

```python
#2、创建模型类
# 还是跟使用sqlalchemy一样，定义模型。现在不再是需要使用delarative_base来创建一个基类。而是使用db.Model来作为基类。
# 在模型类中，Column、String、Integer以及relationship等，都不需要导入了，直接使用db下面相应的属性名就可以了。

class User(db.Model):   #db.Model：固定的写法
    __tablename__='t_user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    uname=db.Column(db.String(50))
    pwd=db.Column(db.String(50))

    def __repr__(self):
        return f'用户名:{self.uname}~~密码:{self.pwd}'
```

###### 字段类型

1. 数值型int/long/float/Numeric
   - Integer
   - SmallInteger
   - BigInteger
   - Float 浮点数
   - decimal.Decimal 定点数
2. 字符串类型str
   - String(长度)
   - Text
3. 日期和时间类型
   - Date
   - Time
   - DateTime
4. JSON类型
5. 布尔值类型Boolean

###### 字段选项

1. primary_key ：如果设为True，这列就是表的主键
2. unique： 如果设为True，这列不允许出现重复的值
3. index ：如果设为True，为这列创建索引，提升查询效率
4. nullable： 如果设为True，这列允许使用空值；如果设为False，这列不允许使用空值
5. default： 为这列定义默认值

###### 将ORM模型映射到数据库表

- 删除数据库表：db.drop_all()
- 创建数据库表：db.create_all()

###### 添加数据

```python
@app.route('/add')
def add():
    name=request.args.get('name')
    pwd=request.args.get('pwd')
    #插入到数据库表t_user中
    user=User(uname=name,pwd=pwd)
    db.session.add(user) # db.session.add_all([admin_role, mod_role, ...])
    db.session.commit()
    return '添加成功'
```

###### 查询数据

```python
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
```

###### 修改数据

```python
admin_role = db.session.query(User).filter(User.name == "tom").first()
admin_role.name = 'Administrator'
# db.session.add(admin_role)
db.session.commit()

user = User(**data)
db.session.merge(user)
db.session.commit()
```

###### 删除数据

```python
@app.route('/delete')
def delete_user():
    name=request.args.get('name')
    user=User.query.filter(User.uname==name).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    return "删除成功"

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

##### 蓝图Blueprint

> Flask蓝图提供了模块化管理程序路由的功能，把不同功能的module分开，使程序结构清晰、简单易懂。
>
> 蓝图对象没有办法独立运行，必须将它注册到一个应用对象上才能生效。
>
> Blueprint 是一个存储操作方法的容器，这些操作在这个Blueprint 被注册到一个应用之后就可以被调用，Flask 可以通过Blueprint来组织URL以及处理请求。
>
> django中路由分配是将总路由通过include分配给app的urls.py路由文件，而**Flask是通过蓝图注册方式将蓝图添加到主app中**，user.py，admin.py主要是创建蓝图，然后为创建的蓝图添加路由配置，接着我们就可以在主路由文件manage.py中将我们创建的蓝图注册到主app中。

- demo1.py

  ```python
  from  flask import Blueprint

  api = Blueprint('api', __name__)

  @api.route('/', methods=['xxx'])
  def xxx():
    	pass
  ```

- demo2.py

  ```python
  from flask import Flask
  from demo1.py import api
  
  app = Flask(__name__)
  # 注册蓝图
  app.register_blueprint(api, url_prefix='/api')
  ```

##### 用户校验

###### 用户密码

- 密码生成

  ```python
  from werkzeug.security import generate_password_hash
  
  pwhash = generate_password_hash(password, method='sha256')
  ```


- 密码校验

  ```python
  from werkzeug.security import check_password_hash
  
  check_password_hash(pwhash: str, password: str) -> bool
  ```

###### 令牌token

> 用户成功登录后，后端会给前端返回token令牌，并将其存储在cookie中，每当用户访问其他接口时都会带着令牌来访问后端，后端都会对token令牌进行校验，校验成功了才执行相应接口的操作（在每个接口上调用装饰器）

```python
import jwt
from flask import current_app

# 制作令牌
token = jwt.encode({
  'aaa':aaa,
  'bbb':bbb,
  'ccc':ccc
})
current_app.config['SECRET_KEY']

# 校验令牌
token = request.headers.get('aaa', '')
data = jwt.decode(token, current_app.config['SECRET_KEY'])
user = User.query.filter_by(username=data['bbb']).first()
```

##### 创建ftp服务

```python
import ftplib

class FtpHelper(object):
    def __init__(
            self,
            host,               # type str
            username,           # type str
            password,           # type str
            port=21             # type str
    ):
        self._host = host
        self._user = username
        self._pwd = password
        self._port = port
        self._ftp = None
        
    def connect(self):
      	self._ftp = ftplib.FTP()
        self._ftp.connect(host=self._host, port=self._port)
        self._ftp.login(user=self._user, passwd=self._pwd)
        pass
    
    def download(self, filename, remote_dir, save_dir):
        if self._ftp is None:
        	self.connect()
        buf_size = 1024
        resp = None
        save_path = os.path.join(save_dir, filename)
        remote_path = os.path.join(remote_dir, filename)
        try:
            fb = open(save_path, 'wb')
            resp = self._ftp.retrbinary('RETR %s' % remote_path, fb.write, buf_size)
            fb.close()
            local_path = save_path
        except Exception as e:
            pass
            local_path = None
        return local_path
    
    def upload(self, filename, local_dir, remote_dir, force_replace=False):
        if self._ftp is None:
        	self.connect()
        local_file_path = os.path.join(local_dir, filename)
        try:
            self.cd(remote_dir)
            filename_list = self._ftp.nlst()   #获取目录下的文件
            upload_path = os.path.join(remote_dir, filename).replace(os.sep, '/')
            if (upload_path not in filename_list) or force_replace:
                bufsize = 1024
                fp = open(local_file_path, 'rb')
                # 上传FTP文件
                self._ftp.storbinary('STOR ' + filename, fp, bufsize)
                fp.close()
            self.cd_root()
        except Exception as expt:
            upload_path = None
        return upload_path
	    def delete(self, filename):
        if self._ftp is None:
            self.connect()
        try:
            self._ftp.delete(filename)
        except Exception as e:
            pass
        return 'delete ok!'
```

##### jinja2

> 要想开发出易于维护的程序，关键在于编写形式简洁且结构良好的代码。
>
> 视图函数的作用很明确，即生成请求的响应。
>
> 模板是一个包含响应文本的文件，其中包含用占位变量表示的动态部分，其具体值只在请求的上下文中才能知道。使用真实值替换变量，再返回最终得到的响应字符串，这一过程称为渲染。

1. 要渲染一个模板，通过`render_template`方法

   ```python
   from flask import Flask,render_template
   app = Flask(__name__)

   @app.route('/about/')
   def about():
       return render_template('about.html')
   ```

2. 如果想更改模板文件地址，应该在创建`app`的时候，给`Flask`传递一个关键字参数`template_folder`，指定具体的路径

   ```python
   from flask import Flask,render_template
   app = Flask(__name__,template_folder=r'C:\templates')

   @app.route('/about/')
   def about():
       return render_template('about.html')
   ```

3. 模板文件中有参数需要传递

   ```python
   from flask import Flask,render_template
   app = Flask(__name__)

   @app.route('/about/')
   def about():
       # return render_template('about.html',user='zhiliao')
       return render_template('about.html',**{'user':'zhiliao'})
   ```

4. 模板中的逻辑处理

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

5. 过滤器是通过管道符号（`|`）进行使用的，例如：`{{ name|length }}`，将返回name的长度。过滤器相当于是一个函数，把当前的变量传入到过滤器中，然后过滤器根据自己的功能，再返回相应的值，之后再将结果渲染到页面中。

6. include語句：把一个模板引入到另外一个模板中，类似于把一个模板的代码copy到另外一个模板的指定位置。

7. 赋值（set）語句：在模板中添加变量

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


7. 模板继承：通过继承可以把模板中许多重复出现的元素抽取出来，放在父模板中，并且父模板通过定义`block`给子模板开一个口，子模板根据需要，再实现这个`block`

8. 静态文件的配置：通过`url_for`全局函数

   ```jinja2
   <link href="{{ url_for('static',filename='about.css') }}">

   # 在模板中引用蓝图，应该要使用蓝图名+.+static来引用
   <link href="{{ url_for('admin.static',filename='about.css') }}">
   ```

9. 类视图



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

if name == 'main':
	app.run(debug=True)
```

###### 渲染模板

> Flask 提供的render_template 函数把Jinja2 模板引擎集成到了程序中。render_template 函数的第一个参数是模板的文件名。随后的参数都是键值对，表示模板中变量对应的真实值。

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
```

###### 变量

- Jinja2 能识别所有类型的变量，甚至是一些复杂的类型，例如列表、字典和对象。

```jinja2
{{ name }}
{{ mydict['key'] }}
{{ mylist[3] }}
{{ mylist[myintvar] }}
{{ myobj.somemethod() }}
```

###### 使用过滤器修改变量，过滤器名添加在变量名之后，中间使用竖线分隔。

```jinja2
{{ name|capitalize }}
```

- Jinja2变量过滤器
  - safe 渲染值时不转义
  - capitalize 把值的首字母转换成大写，其他字母转换成小写
  - lower 把值转换成小写形式
  - upper 把值转换成大写形式
  - title 把值中每个单词的首字母都转换成大写
  - trim 把值的首尾空格去掉
  - striptags 渲染之前把值中所有的HTML 标签都删掉

###### 控制结构

1. 条件控制语句：

  ```jinja2
  {% if user %}
  	Hello, {{ user }}!
  {% else %}
  	Hello, Stranger!
  {% endif %}
  ```

2. 使用for 循环：

  ```jinja2
  <ul>
  	{% for comment in comments %}
  		<li>{{ comment }}</li>
  	{% endfor %}
  </ul>
  ```

3. Jinja2 还支持宏。宏类似于Python 代码中的函数。

  ```jinja2
  {% macro render_comment(comment) %}
  	<li>{{ comment }}</li>
  {% endmacro %}

  <ul>
      {% for comment in comments %}
      	{{ render_comment(comment) }}
      {% endfor %}
  </ul>
  ```

4. 为了重复使用宏，我们可以将其保存在单独的文件中，然后在需要使用的模板中导入：

  ```jinja2
  {% import 'macros.html' as macros %}
  <ul>
  	{% for comment in comments %}
  		{{ macros.render_comment(comment) }}
  	{% endfor %}
  </ul>
  ```

5. 需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有模板中，以避免重复：

  ```jinja2
  {% include 'common.html' %}
  ```

6. 另一种重复使用代码的强大方式是模板继承，它类似于Python 代码中的类继承。

  - 首先，创建一个名为base.html 的基模板：

    ```jinja2
    <html>
    <head>
        {% block head %}
        <title>{% block title %}{% endblock %} - My Application</title>
    {% endblock %}
    </head>
    <body>
        {% block body %}
        {% endblock %}
    </body>
    </html>
    ```

  - block 标签定义的元素可在衍生模板中修改。下面这个示例是基模板的衍生模板：

    ```jinja2
    {% extends "base.html" %}
    {% block title %}Index{% endblock %}
    {% block head %}
        {{ super() }}
        <style>
        </style>
    {% endblock %}
    {% block body %}
    <h1>Hello, World!</h1>
    {% endblock %}
    ```

##### 路由装饰器@app.route()传参方式

1. @app.route('/article/\<converter:variable>/')

   ```python
   @app.route('/article/<id>/')
   def article(id):
      return '%s article detail' % id
   ```

2. 接受两个URL

   ```python
   @app.route('/<any(article,blog):url_path>/')
   def item(url_path):
     return url_path
   ```

3. ?=的形式来传递参数,例如：/article?id=xxx

   - 通过request.args.get('id')来获取id的值
   - post方法，则可以通过request.form.get('id')来进行获取

4. 指定HTTP方法

   ```python
   @app.route('/login/',methods=['GET','POST'])
   def login():
       return 'login'
   ```

5. 页面跳转和重定向

   - 永久性重定向：http的状态码是301
   - 暂时性重定向：http的状态码是302
   - 重定向是通过flask.redirect(location,code=302)这个函数来实现，location表示需要重定向到的URL，配合url_for()函数来使用

   ```python
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

##### Flask程序的基本结构

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


##### flask第三方组件

###### 1. jinja2

> 模板在Python的web开发中广泛使用，它能够有效的将**业务逻辑**和**页面逻辑**分开，使代码可读性增强、并且更加容易理解和维护。
>
> jinja2是Flask作者开发的一个**模板系统**

###### 2. werkzurg

> 是一个WSGI工具包

###### 3. wtforms 

> wtforms组件有两个作用，自动生成html标签和对用户请求数据进行校验。

###### 4. SQLAlchemy

> SQLAlchemy 是目前python中最强大的 ORM框架, 功能全面, 使用简单。

###### 5. redis

###### 6. flask_admin

> 是flask的扩张，主要用于对flask应用程序增加管理界面。



##### flask的返回形式有哪些？

###### 1. 返回HttpResponse对象

```python
@app.route("/home")
def home():
	return "hello world"           # 相当于django中return HttpResponse("")
```

###### 2. 重定向（redirect）

> 当访问"/home"这个路径的时候，视图函数home会重定向到路径"/login" 并会触发"/login"对应的视图函数。

```python
from flask import redirect          # 导入flask中的redirect

@app.route("/home")
def home():
	return redirect("/login")         # 重定向至"/login"路径
```

###### 3. 返回模板页面（render_template） 

```python
from flask import render_template        # 导入flask中的render_template

@app.route("/home")
def home():
	return render_template("home.html")        # 渲染模板home.html并返回
```

###### 4. 返回标准的json字符串

> 返回json字符串，并且会在响应头中加Content-Type:application/json，即告诉浏览器数据是json字符串，浏览器收到后会自动进行反序列化，**而使用json.dumps()则不会加此响应头**。

```python
from flask import jsonify

@app.route("/json")
def jsons():
	d = {"name":"tom"}
	return jsonify(d)
```

###### 5. 打开文件并返回文件内容（自动识别文件格式）

> 自动识别文件类型**，即在返回文件内容时加一个响应头Content-Type:文件类型。**

```python
from flask importsend_file

@app.route("/file")
def file():
	return send_file("01.mp4")
```

##### flask中的request模块（from flask import request）

- 当浏览器去访问一个地址时，Http协议会向后台传递一个request对象。这个request对象包含**请求头、请求参数、以及请求方式**，当然后台可以取到request。然后进行逻辑处理。
- request中包含了前端发送过来的所有数据 ，请求的 request 对象中保存了一次HTTP请求的一切信息。
- 在flask框架中，request对象是一个全局的，在任何地方都可以使用。

###### 1. request.args（get请求） 

> 如果是url参数，例如：url?param1=xx&param2=xx，那么则可以使用request.args来获取参数。

```python
@app.route('/center/add')
def center():
    if request.method == 'GET':  # 请求方式是get
        name = request.args.get('name')  # args取get方式参数
        age = request.args.get('age')
```

###### 2. request.form（post请求/form表单请求）

> 客户端提交过来FormData数据在request.form中

```python
@app.route('/center/add', methods=['GET', 'POST'])  # 支持get和post方法
def center():
    if request.method == 'POST':
        name = request.form.get('name')  # form取post方式参数
        age = request.form.get('age')
        
        # form 表单请求中存在同一个参数名多个值的情况：
        hobby = request.form.getlist('hobby')  # getlist取一键多值类型的参数
        return "姓名：%s 年龄：%s 特长：%s" % (name, age, hobby)
```

###### 3. request.method

> 如果需要区分GET/POST请求方法，则可以使用request.method来进行判断区分。

###### 4. request.data（json请求） 

> 如果是json格式的请求数据，则是采用request.data来获取请求体的字符串。

```python
from flask import Flask, request
import json
 
app = Flask(__name__)
 
 
@app.route('/json', methods=['POST'])
def json_request():
    data = json.loads(request.data)  # 将json字符串转为dict
    name = data['name']
    age = data['age']
    return F"name is {name}, age is {age}"
 
 
if __name__ == '__main__':
    app.run()
```

###### 5. request.files（上传文件请求） 

> 序列化文件，**存储用save()方法，且可以通过filename获取文件名**

```python
from flask import Flask, request
 
app = Flask(__name__)
 
 
@app.route('/upload_file', methods=['POST'])
def file_request():
    file = request.files.get('file')
    if file is None:
        return "未上传文件！"
    file.save(f"{file.name}.jpg")
    return f"{file}文件上传成功！"
 
 
if __name__ == '__main__':
    app.run()
```

###### 6. request.get_json()

###### 7. request.values 

> **只要是个参数都保存在其中，用于查看**，不要使用to_dict()，键重复会覆盖

###### 8. request.cookies 

> 存在浏览器端的字符串也会一起带过来

###### 9. request.headers 

> 请求头中的信息

###### 10. request获取各种路径 

- request.path：获取当前的url路径
- request.script_root：当前url路径的上一级路径
- request.url：当前url的全部路径
- request.url_root