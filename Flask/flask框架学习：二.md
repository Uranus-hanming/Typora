[toc]
###### Flask 有两个主要依赖

- 路由、调试和Web 服务器网关接口（Web Server Gateway Interface，WSGI）子系统由Werkzeug（http://werkzeug.pocoo.org/）提供；
- 模板系统由Jinja2（http://jinja.pocoo.org/）提供。

###### Flask 并不原生支持数据库访问、Web 表单验证和用户认证等高级功能。

> 这些功能以及其他大多数Web 程序中需要的核心服务都以扩展的形式实现，然后再与核心包集成。开发者可以任意挑选符合项目需求的扩展，甚至可以自行开发。

###### 虚拟环境使用第三方实用工具virtualenv 创建。

```
输入以下命令可以检查系统是否安装了virtualenv：
virtualenv --version
```

- Ubuntu 用户可以使用下述命令安装virtualenv 包：

  ```shell
  sudo apt-get install python-virtualenv
  ```

- Mac OS X 系统，可以使用easy_install 安装virtualenv：

  ```shell
  sudo easy_install virtualenv
  ```

- 新建一个文件夹，用来保存示例代码（示例代码可从GitHub 库中获取）

  ```
  git clone https://github.com/miguelgrinberg/flasky.git
  cd flaskygit 
  checkout 1a
  ```

- 使用virtualenv 命令在flasky 文件夹中创建Python 虚拟环境。

> 这个命令只有一个必需的参数，即虚拟环境的名字。创建虚拟环境后，当前文件夹中会出现一个子文件夹，名字就是上述命令中指定的参数，与虚拟环境相关的文件都保存在这个子文件夹中。按照惯例，一般虚拟环境会被命名为venv：

```
virtualenv venv
```

- 激活虚拟环境：

  ```
  Linux 和Mac OS:
  source venv/bin/activate

  Windows 系统:
  venv\Scripts\activate
  ```

- 为了提醒你已经激活了虚拟环境，激活虚拟环境的命令会修改命令行提示符，加入环境名：

  ```
  (venv) $
  ```

- 当虚拟环境中的工作完成后，如果你想回到全局Python 解释器中，可以在命令行提示符下输入deactivate。

#### 程序的基本结构

###### 初始化

- Web 服务器使用一种名为Web 服务器网关接口（Web Server Gateway Interface，WSGI）的协议，把接收自客户端的所有请求都转交给这个对象处理。

```python
# 创建一个程序实例,程序实例是Flask 类的对象

from flask import Flask
# 将构造函数的name 参数传给Flask 程序,Flask 用这个参数决定程序的根目录，以便稍后能够找到相对于程序根目录的资源文件位置。
app = Flask(__name__)
```

###### 路由和视图函数

- 客户端（例如Web 浏览器）把请求发送给Web 服务器，Web 服务器再把请求发送给Flask程序实例。

- 程序实例需要知道对每个URL 请求运行哪些代码，所以保存了一个URL 到Python 函数的映射关系。处理URL 和函数之间关系的程序称为路由。

```python
#在Flask 程序中定义路由的最简便方式，是使用程序实例提供的app.route 修饰器，把修饰的函数注册为路由。
@app.route('/')
def index():  # index()函数称为视图函数
return '<h1>Hello World!</h1>'
```

- 动态路由

> 路由中的动态部分默认使用字符串，不过也可使用类型定义。例如，路由/user/\<int:id>只会匹配动态片段id 为整数的URL。Flask 支持在路由中使用int、float 和path 类型。

```python
@app.route('/user/<name>')
def user(name):
return '<h1>Hello, %s!</h1>' % name
```

###### 启动服务器

- 程序实例用run 方法启动Flask 集成的开发Web 服务器：

  > 服务器启动后，会进入轮询，等待并处理请求。轮询会一直运行，直到程序停止。

  ```python
  if __name__ == '__main__':  # 确保直接执行这个脚本时才启动开发Web 服务器。
  	app.run(debug=True)
  ```

#### 请求−响应循环

###### 程序和请求上下文

> 为了避免大量可有可无的参数把视图函数弄得一团糟，Flask 使用上下文临时把某些对象变为全局可访问。
>
> Falsk 使用上下文让特定的变量在一个线程中全局可访问，与此同时却不会干扰其他线程。

```python
from flask import request
@app.route('/')
def index():
	user_agent = request.headers.get('User-Agent')
	return '<p>Your browser is %s</p>' % user_agent
```

###### Flask上下文全局变量

> Flask 在分发请求之前激活（或推送）程序和请求上下文，请求处理完成后再将其删除。
>
> 程序上下文被推送后，就可以在线程中使用current_app 和g 变量。类似地，请求上下文被推送后，就可以使用request 和session 变量。如果使用这些变量时我们没有激活程序上下文或请求上下文，就会导致错误。

- current_app

  > 程序上下文，当前激活程序的程序实例

- g

  > 程序上下文，处理请求时用作临时存储的对象。每次请求都会重设这个变量

- request

  > 请求上下文，请求对象，封装了客户端发出的HTTP 请求中的内容

- session 

  > 请求上下文，用户会话，用于存储请求之间需要“记住”的值的词典

###### 请求调度

> 程序收到客户端发来的请求时，要找到处理该请求的视图函数。为了完成这个任务，Flask会在程序的URL 映射中查找请求的URL。URL 映射是URL 和视图函数之间的对应关系。

- / 和/user/<name> 路由在程序中使用app.route 修饰器定义。/static/<filename> 路由是Flask 添加的特殊路由，用于访问静态文件。
- URL 映射中的HEAD、Options、GET 是请求方法，由路由进行处理。Flask 为每个路由都指定了请求方法，这样不同的请求方法发送到相同的URL 上时，会使用不同的视图函数进行处理。HEAD 和OPTIONS 方法由Flask 自动处理。

```python
(venv) $ python
>>> from hello import app
>>> app.url_map
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
<Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])
```

###### 请求钩子

> 有时在处理请求之前或之后执行代码会很有用。
>
> 为了避免在每个视图函数中都使用重复的代码，Flask 提供了注册通用函数的功能，注册的函数可在请求被分发到视图函数之前或之后调用。

- 请求钩子使用装饰器实现。Flask 支持以下4 种钩子。
  - before_first_request：注册一个函数，在处理第一个请求之前运行。
  - before_request：注册一个函数，在每次请求之前运行。
  - after_request：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
  - teardown_request：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

- 在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量g。

  > 例如，before_request 处理程序可以从数据库中加载已登录用户，并将其保存到g.user 中。随后调用视图函数时，视图函数再使用g.user 获取用户。

###### 响应

- Flask 调用视图函数后，会将其返回值作为响应的内容。

- 如果视图函数返回的响应需要使用不同的状态码，那么可以把数字代码作为第二个返回值，添加到响应文本之后。

  ```python
  @app.route('/')
  def index():
  	return '<h1>Bad Request</h1>', 400
  ```

- 视图函数返回的响应还可接受第三个参数，这是一个由首部（header）组成的字典，可以添加到HTTP 响应中。

- 如果不想返回由1 个、2 个或3 个值组成的元组，Flask 视图函数还可以返回Response 对象

  > 。make_response() 函数可接受1 个、2 个或3 个参数（和视图函数的返回值一样），并返回一个Response 对象。有时我们需要在视图函数中进行这种转换，然后在响应对象上调用各种方法，进一步设置响应。

```python
from flask import make_response
@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
```

- 重定向

  ```python
  from flask import redirect
  @app.route('/')
  def index():
  	return redirect('http://www.example.com')
  ```

- 应由abort 函数生成，用于处理错误

  ```python
  # 如果URL 中动态参数id 对应的用户不存在，就返回状态码404：
  
  from flask import abort
  @app.route('/user/<id>')
  def get_user(id):
      user = load_user(id)
      if not user:
      	abort(404)
      return '<h1>Hello, %s</h1>' % user.name
  ```

#### Flask扩展

###### 使用Flask-Script支持命令行选项

> Flask 的开发Web 服务器支持很多启动设置选项，但只能在脚本中作为参数传给app.run()函数。这种方式并不十分方便，传递设置选项的理想方式是使用命令行参数。
>
> Flask-Script 是一个Flask 扩展，为Flask 程序添加了一个命令行解析器。Flask-Script 自带了一组常用选项，而且还支持自定义命令。

```python
from flask import Flask
from flask_script import Manager

app = Flask(__name__)

manager = Manager(app)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    manager.run()
```

#### Jinja2模板引擎

- 要想开发出易于维护的程序，关键在于编写形式简洁且结构良好的代码。
- 视图函数的作用很明确，即生成请求的响应。
- 模板是一个包含响应文本的文件，其中包含用占位变量表示的动态部分，其具体值只在请求的上下文中才能知道。使用真实值替换变量，再返回最终得到的响应字符串，这一过程称为渲染。

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

- 条件控制语句：

  ```jinja2
  {% if user %}
  	Hello, {{ user }}!
  {% else %}
  	Hello, Stranger!
  {% endif %}
  ```

- 使用for 循环：

  ```jinja2
  <ul>
  	{% for comment in comments %}
  		<li>{{ comment }}</li>
  	{% endfor %}
  </ul>
  ```

- Jinja2 还支持宏。宏类似于Python 代码中的函数。

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

- 为了重复使用宏，我们可以将其保存在单独的文件中，然后在需要使用的模板中导入：

  ```jinja2
  {% import 'macros.html' as macros %}
  <ul>
  	{% for comment in comments %}
  		{{ macros.render_comment(comment) }}
  	{% endfor %}
  </ul>
  ```

- 需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有模板中，以避免重复：

  ```jinja2
  {% include 'common.html' %}
  ```

- 另一种重复使用代码的强大方式是模板继承，它类似于Python 代码中的类继承。

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

###### 使用Flask-Bootstrap集成Twitter Bootstrap

- Bootstrap（http://getbootstrap.com/）是Twitter 开发的一个开源框架，它提供的用户界面组件可用于创建整洁且具有吸引力的网页，而且这些网页还能兼容所有现代Web 浏览器。
- Bootstrap 是客户端框架，因此不会直接涉及服务器。服务器需要做的只是提供引用了Bootstrap 层叠样式表（CSS） 和JavaScript 文件的HTML 响应， 并在HTML、CSS 和JavaScript 代码中实例化所需组件。这些操作最理想的执行场所就是模板。

- Flask 扩展一般都在创建程序实例时初始化。

- 初始化Flask-Bootstrap

  > 初始化Flask-Bootstrap 之后，就可以在程序中使用一个包含所有Bootstrap 文件的基模板。
  >
  > 这个模板利用Jinja2 的模板继承机制，让程序扩展一个具有基本页面结构的基模板，其中就有用来引入Bootstrap 的元素。

  ```python
  from flask_bootstrap import Bootstrap

  app = Flask(__name__)

  bootstrap = Bootstrap(app)
  ```

- 使用Flask-Bootstrap 的模板

  ```jinja2
  {% extends "bootstrap/base.html" %}
  
  {% block title %}Flasky{% endblock %}
  
  {% block navbar %}
  <div class="navbar navbar-inverse" role="navigation">
      <div class="container">
          <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                  <span class="sr-only">Toggle navigation</span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">Flasky</a>
          </div>
          <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                  <li><a href="/">Home</a></li>
              </ul>
          </div>
      </div>
  </div>
  {% endblock %}
  
  {% block content %}
  <div class="container">
      <div class="page-header">
          <h1>Hello, {{ name }}!</h1>
      </div>
  </div>
  {% endblock %}
  ```

  - Jinja2 中的extends 指令从Flask-Bootstrap 中导入bootstrap/base.html， 从而实现模板继承。

  - 。Flask-Bootstrap 中的基模板提供了一个网页框架，引入了Bootstrap 中的所有CSS 和JavaScript 文件。

  - 基模板中定义了可在衍生模板中重定义的块。block 和endblock 指令定义的块中的内容可添加到基模板中。

  - 上面这个user.html 模板定义了3 个块，分别名为title、navbar 和content。。这些块都是
    基模板提供的，可在衍生模板中重新定义。

    - 。title 块的作用很明显，其中的内容会出现在渲染后的HTML 文档头部，放在<title> 标签中。
    - navbar 和content 这两个块分别表示页面中的导航条和主体内容。

  - Flask-Bootstrap 的base.html 模板还定义了很多其他块，都可在衍生模板中使用。

    - doc 整个HTML 文档
    - html_attribs <html> 标签的属性
    - html <html> 标签中的内容
    - head <head> 标签中的内容
    - title <title> 标签中的内容
    - metas 一组<meta> 标签
    - styles 层叠样式表定义
    - body_attribs <body> 标签的属性
    - body <body> 标签中的内容
    - navbar 用户定义的导航条
    - content 用户定义的页面内容
    - scripts 文档底部的JavaScript 声明

  - 如果程序需要向已经有内容的块中添加新内容，必须使用Jinja2 提供的super() 函数。

    ```jinja2
    # 。例如，如果要在衍生模板中添加新的JavaScript 文件，需要这么定义scripts 块：
    {% block scripts %}
    {{ super() }}
    <script type="text/javascript" src="my-script.js"></script>
    {% endblock %}
    ```

###### 自定义错误页面

> 如果你在浏览器的地址栏中输入了不可用的路由，那么会显示一个状态码为404 的错误页面。现在这个错误页面太简陋、平庸，而且样式和使用了Bootstrap 的页面不一致。

- 像常规路由一样，Flask 允许程序使用基于模板的自定义错误页面。最常见的错误代码有两个：

  - 404，客户端请求未知页面或路由时显示；
  - 500，有未处理的异常时显示

- Flask-Bootstrap 提供了一个具有页面基本布局的基模板，同样，程序可以定义一个具有更完整页面布局的基模板，其中包含导航条，而页面内容则可留到衍生模板中定义。

- 自定义错误页面

  ```python
  @app.errorhandler(404)
  def page_not_found(e):
  	return render_template('404.html'), 404
  @app.errorhandler(500)
  def internal_server_error(e):
  	return render_template('500.html'), 500
  ```

- 包含导航条的程序基模板

  ```jinja2
  {% extends "bootstrap/base.html" %}
  {% block title %}Flasky{% endblock %}
  {% block navbar %}
  <div class="navbar navbar-inverse" role="navigation">
      <div class="container">
          <div class="navbar-header">
              <button type="button" class="navbar-toggle"
                      data-toggle="collapse" data-target=".navbar-collapse">
                  <span class="sr-only">Toggle navigation</span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">Flasky</a>
          </div>
          <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                  <li><a href="/">Home</a></li>
              </ul>
          </div>
      </div>
  </div>
  {% endblock %}
  {% block content %}
  <div class="container">
      {% block page_content %}{% endblock %}
  </div>
  {% endblock %}
  ```

  - 这个模板的content 块中只有一个<div> 容器，其中包含了一个名为page_content 的新的空块，块中的内容由衍生模板定义。

- 使用模板继承机制自定义404 错误页面

  ```jinja2
  {% extends "base.html" %}
  {% block title %}Flasky - Page Not Found{% endblock %}
  {% block page_content %}
  <div class="page-header">
  	<h1>Not Found</h1>
  </div>
  {% endblock %}
  ```

- 使用模板继承机制简化页面模板

  ```jinja2
  {% extends "base.html" %}
  {% block title %}Flasky{% endblock %}
  {% block page_content %}
  <div class="page-header">
  	<h1>Hello, {{ name }}!</h1>
  </div>
  {% endblock %}
  ```

###### 链接

> 任何具有多个路由的程序都需要可以连接不同页面的链接，例如导航条。
>
> 在模板中直接编写简单路由的URL 链接不难，但对于包含可变部分的动态路由，在模板中构建正确的URL 就很困难。而且，直接编写URL 会对代码中定义的路由产生不必要的依赖关系。如果重新定义路由，模板中的链接可能会失效。为了避免这些问题，Flask 提供了url_for() 辅助函数，它可以使用程序URL 映射中保存的信息生成URL。

- url_for() 函数最简单的用法是以视图函数名（或者app.add_url_route() 定义路由时使用的端点名）作为参数，返回对应的URL。
  - 在当前版本的hello.py 程序中调用url_for('index') 得到的结果是/。
  - 调用url_for('index', _external=True) 返回的则是绝对地址，在这个示例中是http://localhost:5000/。
  - 使用url_for() 生成动态地址时， 将动态部分作为关键字参数传入。例如，url_for('user', name='john', _external=True) 的返回结果是http://localhost:5000/user/john。
  - 传入url_for() 的关键字参数不仅限于动态路由中的参数。函数能将任何额外参数添加到查询字符串中。例如，url_for('index', page=2) 的返回结果是/?page=2。

###### 静态文件

> 默认设置下，Flask 在程序根目录中名为static 的子目录中寻找静态文件。如果需要，可在static 文件夹中使用子文件夹存放文件。服务器收到前面那个URL 后，会生成一个响应，包含文件系统中static/css/styles.css 文件的内容。

- 定义收藏夹图标

  ```jinja2
  {% block head %}
  {{ super() }}
  <link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
  	type="image/x-icon">
  <link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
  	type="image/x-icon">
  {% endblock %}
  ```

- 图标的声明会插入head 块的末尾。注意如何使用super() 保留基模板中定义的块的原始内容。

###### 使用Flask-Moment本地化日期和时间

- 初始化Flask-Moment

  ```python
  from flask.ext.moment import Moment
  moment = Moment(app)
  ```

- 如何在基模板的scripts 块中引入moment.js 库。

  ```jinja2
  {% block scripts %}
  {{ super() }}
  {{ moment.include_moment() }}
  {% endblock %}
  ```

- 为了处理时间戳，Flask-Moment 向模板开放了moment 类。

- 把变量current_time 传入模板进行渲染。

  ```python
  from datetime import datetime
  @app.route('/')
  def index():
  	return render_template('index.html',current_time=datetime.utcnow())
  ```

- 使用Flask-Moment 渲染时间戳

  ```jinja2
  <p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
  <p>That was {{ moment(current_time).fromNow(refresh=True) }}</p>
  ```

- format('LLL') 根据客户端电脑中的时区和区域设置渲染日期和时间。参数决定了渲染的方式，'L' 到'LLLL' 分别对应不同的复杂度。format() 函数还可接受自定义的格式说明符。

- 第二行中的fromNow() 渲染相对时间戳，而且会随着时间的推移自动刷新显示的时间。这个时间戳最开始显示为“a few seconds ago”，但指定refresh 参数后，其内容会随着时间的推移而更新。如果一直待在这个页面，几分钟后，会看到显示的文本变成“a minuteago”“2 minutes ago”等。

- Flask-Moment 实现了moment.js 中的format()、fromNow()、fromTime()、calendar()、valueOf()和unix() 方法。

- Flask-Moment 渲染的时间戳可实现多种语言的本地化。语言可在模板中选择，把语言代码传给lang() 函数即可：

  ```jinja2
  {{ moment.lang('es') }}
  ```

#### Web表单

- request.form 能获取POST 请求中提交的表单数据。

###### 跨站请求伪造保护

> 为了实现CSRF 保护，Flask-WTF 需要程序设置一个密钥。Flask-WTF 使用这个密钥生成加密令牌，再用令牌验证请求中表单数据的真伪。

- 设置密钥的方法

  ```python
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'hard to guess string'
  ```

- app.config 字典可用来存储框架、扩展和程序本身的配置变量。使用标准的字典句法就能把配置值添加到app.config 对象中。这个对象还提供了一些方法，可以从文件或环境中导入配置值。
- SECRET_KEY 配置变量是通用密钥，可在Flask 和多个第三方扩展中使用。如其名所示，加密的强度取决于变量值的机密程度。不同的程序要使用不同的密钥，而且要保证其他人不知道你所用的字符串。
- 为了增强安全性，密钥不应该直接写入代码，而要保存在环境变量中。

###### 表单类

> 使用Flask-WTF 时，每个Web 表单都由一个继承自Form 的类表示。这个类定义表单中的一组字段，每个字段都用对象表示。字段对象可附属一个或多个验证函数。验证函数用来验证用户提交的输入值是否符合要求。

- 定义表单类

  ```python
  from flask_wtf import Form
  from wtforms import StringField, SubmitField
  from wtforms.validators import Required
  class NameForm(Form):
      name = StringField('What is your name?', validators=[Required()])
      submit = SubmitField('Submit')
  ```
  - 这个表单中的字段都定义为类变量，类变量的值是相应字段类型的对象。
  - 在这个示例中，NameForm 表单中有一个名为name 的文本字段和一个名为submit 的提交按钮。
  - StringField类表示属性为type="text" 的<input> 元素。
  - SubmitField 类表示属性为type="submit" 的<input> 元素。
  - 字段构造函数的第一个参数是把表单渲染成HTML 时使用的标号。
  - StringField 构造函数中的可选参数validators 指定一个由验证函数组成的列表，在接受用户提交的数据之前验证数据。验证函数Required() 确保提交的字段不为空。

- WTForms 支持的HTML 标准字段
  - StringField 文本字段
    TextAreaField 多行文本字段
    PasswordField 密码文本字段
    HiddenField 隐藏文本字段
    DateField 文本字段，值为datetime.date 格式
    DateTimeField 文本字段，值为datetime.datetime 格式
    IntegerField 文本字段，值为整数
    DecimalField 文本字段，值为decimal.Decimal
    FloatField 文本字段，值为浮点数
    BooleanField 复选框，值为True 和False
    RadioField 一组单选框
    SelectField 下拉列表
    SelectMultipleField 下拉列表，可选择多个值
    FileField 文件上传字段
    SubmitField 表单提交按钮
    FormField 把表单作为字段嵌入另一个表单
    FieldList 一组指定类型的字段
- WTForms验证函数
  - Email 验证电子邮件地址
    EqualTo 比较两个字段的值；常用于要求输入两次密码进行确认的情况
    IPAddress 验证IPv4 网络地址
    Length 验证输入字符串的长度
    NumberRange 验证输入的值在数字范围内
    Optional 无输入值时跳过其他验证函数
    Required 确保字段中有数据
    Regexp 使用正则表达式验证输入值
    URL 验证URL
    AnyOf 确保输入值在可选值列表中
    NoneOf 确保输入值不在可选值列表中

###### 把表单渲染成HTML

- 表单字段是可调用的，在模板中调用后会渲染成HTML。

- 使用Bootstrap 中预先定义好的表单样式渲染整个Flask-WTF 表单

  ```jinja2
  {% import "bootstrap/wtf.html" as wtf %}
  {{ wtf.quick_form(form) }}
  ```
  - import 指令的使用方法和普通Python 代码一样，允许导入模板中的元素并用在多个模板中。
  - 导入的bootstrap/wtf.html 文件中定义了一个使用Bootstrap 渲染Falsk-WTF 表单对象的辅助函数。
  - wtf.quick_form() 函数的参数为Flask-WTF 表单对象，使用Bootstrap 的默认样式渲染传入的表单。

- 使用Flask-WTF 和Flask-Bootstrap 渲染表单

  ```jinja2
  {% extends "base.html" %}
  {% import "bootstrap/wtf.html" as wtf %}
  {% block title %}Flasky{% endblock %}
  {% block page_content %}
  <div class="page-header">
  	<h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
  </div>
  {{ wtf.quick_form(form) }}
  {% endblock %}
  ```
  - 模板的内容区现在有两部分。第一部分是页面头部，显示欢迎消息。这里用到了一个模板条件语句。Jinja2 中的条件语句格式为{% if condition %}...{% else %}...{% endif %}。如果条件的计算结果为True，那么渲染if 和else 指令之间的值。如果条件的计算结果为False，则渲染else 和endif 指令之间的值。在这个例子中，如果没有定义模板变量name，Web表单则会渲染字符串“Hello, Stranger!”。内容区的第二部分使用wtf.quick_form() 函数渲染NameForm 对象。

###### 在视图函数中处理表单

- 视图函数index() 不仅要渲染表单，还要接收表单中的数据。

- hello.py：路由方法

  ```python
  @app.route('/', methods=['GET', 'POST'])
  def index():
      name = None
      form = NameForm()
      if form.validate_on_submit():
          name = form.name.data
          form.name.data = ''
      return render_template('index.html', form=form, name=name)
  ```
  - app.route 修饰器中添加的methods 参数告诉Flask 在URL 映射中把这个视图函数注册为GET 和POST 请求的处理程序。如果没指定methods 参数，就只把视图函数注册为GET 请求的处理程序。把POST 加入方法列表很有必要，因为将提交表单作为POST 请求进行处理更加便利。表单也可作为GET 请求提交，不过GET 请求没有主体，提交的数据以查询字符串的形式附加到URL 中，可在浏览器的地址栏中看到。基于这个以及其他多个原因，提交表单大都作为POST 请求进行处理。
  - 局部变量name 用来存放表单中输入的有效名字，如果没有输入，其值为None。如上述代码所示，在视图函数中创建一个NameForm 类实例用于表示表单。提交表单后，如果数据能被所有验证函数接受，那么validate_on_submit() 方法的返回值为True，否则返回False。这个函数的返回值决定是重新渲染表单还是处理表单提交的数据。
  - 用户第一次访问程序时，服务器会收到一个没有表单数据的GET 请求，所以validate_on_submit() 将返回False。if 语句的内容将被跳过，通过渲染模板处理请求，并传入表单对象和值为None 的name 变量作为参数。用户会看到浏览器中显示了一个表单。
  - 用户提交表单后，服务器收到一个包含数据的POST 请求。validate_on_submit() 会调用name 字段上附属的Required() 验证函数。如果名字不为空，就能通过验证，validate_on_submit() 返回True。现在，用户输入的名字可通过字段的data 属性获取。在if 语句中，把名字赋值给局部变量name，然后再把data 属性设为空字符串，从而清空表单字段。最后一行调用render_template() 函数渲染模板，但这一次参数name 的值为表单中输入的名字，因此会显示一个针对该用户的欢迎消息。

- 如果用户提交表单之前没有输入名字，Required() 验证函数会捕获这个错误。说明扩展自动提供了很多功能。

###### 重定向和用户会话

- 最好别让Web 程序把POST 请求作为浏览器发送的最后一个请求。这种需求的实现方式是，使用重定向作为POST 请求的响应，而不是使用常规响应。

- 重定向是一种特殊的响应，响应内容是URL，而不是包含HTML 代码的字符串。浏览器收到这种响应时，会向重定向的URL 发起GET 请求，显示页面的内容。

- 程序可以把数据存储在用户会话中，在请求之间“记住”数据。用户会话是一种私有存储，存在于每个连接到服务器的客户端中。它是请求上下文中的变量，名为session，像标准的Python 字典一样操作。

- 默认情况下，用户会话保存在客户端cookie 中，使用设置的SECRET_KEY 进行加密签名。如果篡改了cookie 中的内容，签名就会失效，会话也会随之失效。

- 重定向和用户会话

  ```python
  from flask import Flask, render_template, session, redirect, url_for
  
  @app.route('/', methods=['GET', 'POST'])
  def index():
      form = NameForm()
      if form.validate_on_submit():
          session['name'] = form.name.data
          return redirect(url_for('index'))
      return render_template('index.html', form=form, name=session.get('name'))
  ```
  - 在程序的前一个版本中，局部变量name 被用于存储用户在表单中输入的名字。这个变量现在保存在用户会话中，即session['name']，所以在两次请求之间也能记住输入的值。
  - 在程序的前一个版本中，局部变量name 被用于存储用户在表单中输入的名字。这个变量现在保存在用户会话中，即session['name']，所以在两次请求之间也能记住输入的值。
  - redirect() 是个辅助函数，用来生成HTTP 重定向响应。
  - url_for() 函数的第一个且唯一必须指定的参数是端点名，即路由的内部名字。默认情况下，路由的端点是相应视图函数的名字。在这个示例中，处理根地址的视图函数是index()，因此传给url_for() 函数的名字是index。
  - 最后一处改动位于render_function() 函数中，使用session.get('name') 直接从会话中读取name 参数的值。和普通的字典一样，这里使用get() 获取字典中键对应的值以避免未找到键的异常情况，因为对于不存在的键，get() 会返回默认值None。

###### Flash消息

> 请求完成后，有时需要让用户知道状态发生了变化。

- flash消息

  ```python
  from flask import Flask, render_template, session, redirect, url_for, flash

  @app.route('/', methods=['GET', 'POST'])
  def index():
      form = NameForm()
      if form.validate_on_submit():
          old_name = session.get('name')
          if old_name is not None and old_name != form.name.data:
              flash('Looks like you have changed your name!')
          session['name'] = form.name.data
          return redirect(url_for('index'))
      return render_template('index.html', form=form, name=session.get('name'))
  ```
  - 在这个示例中，每次提交的名字都会和存储在用户会话中的名字进行比较，而会话中存储的名字是前一次在这个表单中提交的数据。如果两个名字不一样，就会调用flash() 函数，在发给客户端的下一个响应中显示一个消息。

- Flask 把get_flashed_messages() 函数开放给模板，用来获取并渲染消息

```python
{% block content %}
<div class="container">
    {% for message in get_flashed_messages() %}
    <div class="alert alert-warning">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        {{ message }}
    </div>
    {% endfor %}
    {% block page_content %}{% endblock %}
</div>
{% endblock %}
```

- 在模板中使用循环是因为在之前的请求循环中每次调用flash() 函数时都会生成一个消息，所以可能有多个消息在排队等待显示。get_flashed_messages() 函数获取的消息在下次调用时不会再次返回，因此Flash 消息只显示一次，然后就消失了。

#### 数据库

###### SQL数据库

- 关系型数据库把数据存储在表中，表模拟程序中不同的实体。
- 表的列数是固定的，行数是可变的。列定义表所表示的实体的数据属性。表中的行定义各列对应的真实数据。
- 表中有个特殊的列，称为主键，其值为表中各行的唯一标识符。
- 表中还可以有称为外键的列，引用同一个表或不同表中某行的主键。

###### NoSQL数据库

- 所有不遵循上节所述的关系模型的数据库统称为NoSQL 数据库。
- NoSQL 数据库一般使用集合代替表，使用文档代替记录。
- NoSQL 数据库采用的设计方式使联结变得困难。
- 减少了表的数量，却增加了数据重复量。数据重复可以提升查询速度。

###### Python数据库框架

- ORM:对象关系映射

###### 使用Flask-SQLAlchemy管理数据库

- Flask-SQLAlchemy 是一个Flask 扩展，简化了在Flask 程序中使用SQLAlchemy 的操作。
- SQLAlchemy 是一个很强大的关系型数据库框架，支持多种数据库后台。SQLAlchemy 提供了高层ORM，也提供了使用数据库原生SQL 的低层功能。
- FLask-SQLAlchemy数据库URL
  - MySQL mysql://username:password@hostname/database
  - Postgres postgresql://username:password@hostname/database
  - SQLite（Unix） sqlite:////absolute/path/to/database
  - SQLite（Windows） sqlite:///c:/absolute/path/to/database

- 程序使用的数据库URL 必须保存到Flask 配置对象的SQLALCHEMY_DATABASE_URI 键中。
- 配置对象中还有一个很有用的选项，即SQLALCHEMY_COMMIT_ON_TEARDOWN 键，将其设为True时，每次请求结束后都会自动提交数据库中的变动。

- 配置数据库

  > db 对象是SQLAlchemy 类的实例，表示程序使用的数据库，同时还获得了Flask-SQLAlchemy提供的所有功能。

  ```python
  import os
  
  from flask import Flask
  from flask_sqlalchemy import SQLAlchemy
  
  basedir = os.path.abspath(os.path.dirname(__file__))
  app = Flask(__name__)
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
  db = SQLAlchemy(app)
  ```

###### 定义模型

> 模型这个术语表示程序使用的持久化实体。在ORM 中，模型一般是一个Python 类，类中的属性对应数据库表中的列。

- Flask-SQLAlchemy 创建的数据库实例为模型提供了一个基类以及一系列辅助类和辅助函数，可用于定义模型的结构。

- 定义Role 和User 模型

  ```python
  import os
  
  from flask import Flask
  from flask_sqlalchemy import SQLAlchemy
  
  basedir = os.path.abspath(os.path.dirname(__file__))
  app = Flask(__name__)
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
  db = SQLAlchemy(app)


  class Role(db.Model):
      __tablename__ = 'roles'
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(64), unique=True)

      def __repr__(self):
          return '<Role %r>' % self.name


  class User(db.Model):
      __tablename__ = 'users'
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(64), unique=True, index=True)

      def __repr__(self):
          return '<User %r>' % self.username
  ```

  - 类变量\__tablename__ 定义在数据库中使用的表名。

  - 其余的类变量都是该模型的属性，被定义为db.Column类的实例。

  - db.Column 类构造函数的第一个参数是数据库列和模型属性的类型。

  ```
    # 最常用的SQLAlchemy列类型
    
    Integer int 普通整数，一般是32 位
    SmallInteger int 取值范围小的整数，一般是16 位
    BigInteger int 或long 不限制精度的整数
    Float float 浮点数
    Numeric decimal.Decimal 定点数
    String str 变长字符串
    Text str 变长字符串，对较长或不限长度的字符串做了优化
    Unicode unicode 变长Unicode 字符串
    UnicodeText unicode 变长Unicode 字符串，对较长或不限长度的字符串做了优化
    Boolean bool 布尔值
    Date datetime.date 日期
    Time datetime.time 时间
    DateTime datetime.datetime 日期和时间
    Interval datetime.timedelta 时间间隔
    Enum str 一组字符串
    PickleType 任何Python 对象自动使用Pickle 序列化
    LargeBinary str 二进制文件
    ```

  - db.Column 中其余的参数指定属性的配置选项。

    ```
    # 最常使用的SQLAlchemy列选项

    primary_key 如果设为True，这列就是表的主键
    unique 如果设为True，这列不允许出现重复的值
    index 如果设为True，为这列创建索引，提升查询效率
    nullable 如果设为True，这列允许使用空值；如果设为False，这列不允许使用空值
    default 为这列定义默认值
    ```

  - 两个模型都定义了\__repr()__ 方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用。

###### 关系

> 关系型数据库使用关系把不同表中的行联系起来。

```python
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username
```

- 添加到User 模型中的role_id 列被定义为外键，就是这个外键建立起了关系。传给db.ForeignKey() 的参数'roles.id' 表明，这列的值是roles 表中行的id 值。

- 添加到Role 模型中的users 属性代表这个关系的面向对象视角。对于一个Role 类的实例，其users 属性将返回与角色相关联的用户组成的列表。db.relationship() 的第一个参数表明这个关系的另一端是哪个模型。如果模型类尚未定义，可使用字符串形式指定。

- db.relationship() 中的backref 参数向User 模型中添加一个role 属性，从而定义反向关系。这一属性可替代role_id 访问Role 模型，此时获取的是模型对象，而不是外键的值。

- 如果无法决定外键，你就要为db.relationship() 提供额外参数，从而确定所用外键。

  ```
  # 常用的SQLAlchemy关系选项
  
  1、 backref 在关系的另一个模型中添加反向引用
  2、 primaryjoin 明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定
  3、 lazy 指定如何加载相关记录。可选值有select（首次访问时按需加载）、immediate（源对象加载后就加载）、joined（加载记录，但使用联结）、subquery（立即加载，但使用子查询）
  4、 noload（永不加载）和dynamic（不加载记录，但提供加载记录的查询）
  5、 uselist 如果设为Fales，不使用列表，而使用标量值
  6、 order_by 指定关系中记录的排序方式
  7、 secondary 指定多对多关系中关系表的名字
  8、 secondaryjoin SQLAlchemy 无法自行决定时，指定多对多关系中的二级联结条件
  ```

###### 数据库操作

- 创建表

  ```python
  db.create_all()
  ```

- 插入行

  ```
  from hello import Role, User
  admin_role = Role(name='Admin')
  mod_role = Role(name='Moderator')
  user_role = Role(name='User')
  user_john = User(username='john', role=admin_role)
  user_susan = User(username='susan', role=user_role)
  user_david = User(username='david', role=user_role)
  ```

- 通过数据库会话管理对数据库所做的改动，在Flask-SQLAlchemy 中，会话由db.session表示。准备把对象写入数据库之前，先要将其添加到会话中：

  ```python
  db.session.add(admin_role)
  db.session.add(mod_role)
  db.session.add(user_role)
  db.session.add(user_john)
  db.session.add(user_susan)
  db.session.add(user_david)

  或者简写成：
  db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])
  ```

- 为了把对象写入数据库，我们要调用commit() 方法提交会话：

  ```python
  db.session.commit()
  ```

- 修改行

  ```python
  admin_role.name = 'Administrator'
  db.session.add(admin_role)
  db.session.commit()
  ```

- 删除行

  ```python
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

- 查询行

  > Flask-SQLAlchemy 为每个模型类都提供了query 对象。

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

- 查看SQLAlchemy 为查询生成的原生SQL 查询语句，只需把query 对象转换成字符串：

  ```
  str(User.query.filter_by(role=user_role))

  'SELECT users.id AS users_id, users.username AS users_username,users.role_id AS users_role_id FROM users WHERE :param_1 = users.role_id'
  ```

- 常用的SQLAlchemy查询过滤器

  ```
  filter() 把过滤器添加到原查询上，返回一个新查询
  filter_by() 把等值过滤器添加到原查询上，返回一个新查询
  limit() 使用指定的值限制原查询返回的结果数量，返回一个新查询
  offset() 偏移原查询返回的结果，返回一个新查询
  order_by() 根据指定条件对原查询结果进行排序，返回一个新查询
  group_by() 根据指定条件对原查询结果进行分组，返回一个新查询
  ```

- 最常使用的SQLAlchemy查询执行函数

  ```
  all() 以列表形式返回查询的所有结果
  first() 返回查询的第一个结果，如果没有结果，则返回None
  first_or_404() 返回查询的第一个结果，如果没有结果，则终止请求，返回404 错误响应
  get() 返回指定主键对应的行，如果没有对应的行，则返回None
  get_or_404() 返回指定主键对应的行，如果没找到指定的主键，则终止请求，返回404 错误响应
  count() 返回查询结果的数量
  paginate() 返回一个Paginate 对象，它包含指定范围内的结果
  ```

###### 在视图函数中操作数据库

- 创建ORM

  ```python
  # demo3
  
  from flask import Flask
  from flask_sqlalchemy import SQLAlchemy
  
  app = Flask(__name__)
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:qq5253@localhost:3306/people?charset=utf8'
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
  db = SQLAlchemy(app)


  class Role(db.Model):
      __tablename__ = 'roles'
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(64), unique=True)

      def __repr__(self):
          return '<Role %r>' % self.name


  class User(db.Model):
      __tablename__ = 'users'
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(64), unique=True, index=True)

      def __repr__(self):
          return '<User %r>' % self.username


  db.create_all()
  ```

- 在视图函数中操作数据库

```python
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
from flask import Flask, render_template, session, redirect, url_for, flash
from demo3 import User, db, app

app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))


if __name__ == '__main__':
    app.run(debug=True)
  ```

- 这个模板使用known 参数在欢迎消息中加入了第二行，从而对已知用户和新用户显示不同的内容。

```jinja2
# index.html

{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
    {% if not known %}
    <p>Pleased to meet you!</p>
    {% else %}
    <p>Happy to see you again!</p>
    {% endif %}
</div>
{{ wtf.quick_form(form) }}
{% endblock %}
```

- base.html

  ```jinja2
  {% extends "bootstrap/base.html" %}
  
  {% block title %}Flasky{% endblock %}
  
  {% block head %}
  {{ super() }}
  <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
  <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
  {% endblock %}
  
  {% block navbar %}
  <div class="navbar navbar-inverse" role="navigation">
      <div class="container">
          <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                  <span class="sr-only">Toggle navigation</span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">Flasky</a>
          </div>
          <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                  <li><a href="/">Home</a></li>
              </ul>
          </div>
      </div>
  </div>
  {% endblock %}
  
  {% block content %}
  <div class="container">
      {% for message in get_flashed_messages() %}
      <div class="alert alert-warning">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          {{ message }}
      </div>
      {% endfor %}
      {% block page_content %}{% endblock %}
  </div>
  {% endblock %}


  {% block scripts %}
  {{ super() }}
  {{ moment.include_moment() }}
  {% endblock %}
  ```

使用Flask-Migrate实现数据库迁移

> 数据库迁移框架能跟踪数据库模式的变化，然后增量式的把变化应用到数据库中。

- 创建迁移仓库
- 创建迁移脚本
- 更新数据库

###### 电子邮件

- 使用Flask-Mail提供电子邮件支持

  > Flask-Mail 连接到简单邮件传输协议（Simple Mail Transfer Protocol，SMTP）服务器，并把邮件交给这个服务器发送。

- Flask-Mail SMTP服务器的配置

  ```
  MAIL_SERVER localhost 电子邮件服务器的主机名或IP 地址
  MAIL_PORT 25 电子邮件服务器的端口
  MAIL_USE_TLS False 启用传输层安全（Transport Layer Security，TLS）协议
  MAIL_USE_SSL False 启用安全套接层（Secure Sockets Layer，SSL）协议
  MAIL_USERNAME None 邮件账户的用户名
  MAIL_PASSWORD None 邮件账户的密码
  ```

- 初始化Flask-Mail

  ```
  from flask_mail import Mail
  mail = Mail(app)
  ```

- 保存电子邮件服务器用户名和密码的两个环境变量要在环境中定义。

  ```
  在Linux 或Mac OS X 中使用bash:
  export MAIL_USERNAME=<Gmail username>
  export MAIL_PASSWORD=<Gmail password>

  Windows:
  set MAIL_USERNAME=<Gmail username>
  set MAIL_PASSWORD=<Gmail password>
  ```

- 在程序中集成发送电子邮件功能

  ```python
  import os
  from flask import Flask, render_template, session, redirect, url_for
  from flask_bootstrap import Bootstrap
  from flask_moment import Moment
  from flask_wtf import FlaskForm
  from wtforms import StringField, SubmitField
  from wtforms.validators import DataRequired
  from flask_sqlalchemy import SQLAlchemy
  from flask_migrate import Migrate
  from flask_mail import Mail, Message

  basedir = os.path.abspath(os.path.dirname(__file__))

  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'hard to guess string'
  app.config['SQLALCHEMY_DATABASE_URI'] =\
      'sqlite:///' + os.path.join(basedir, 'data.sqlite')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
  app.config['MAIL_PORT'] = 587
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
  app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
  app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
  app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
  app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

  bootstrap = Bootstrap(app)
  moment = Moment(app)
  db = SQLAlchemy(app)
  migrate = Migrate(app, db)
  mail = Mail(app)


  class Role(db.Model):
      __tablename__ = 'roles'
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(64), unique=True)
      users = db.relationship('User', backref='role', lazy='dynamic')

      def __repr__(self):
          return '<Role %r>' % self.name


  class User(db.Model):
      __tablename__ = 'users'
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(64), unique=True, index=True)
      role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

      def __repr__(self):
          return '<User %r>' % self.username


  def send_email(to, subject, template, **kwargs):
      msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
      msg.body = render_template(template + '.txt', **kwargs)
      msg.html = render_template(template + '.html', **kwargs)
      mail.send(msg)


  class NameForm(FlaskForm):
      name = StringField('What is your name?', validators=[DataRequired()])
      submit = SubmitField('Submit')


  @app.shell_context_processor
  def make_shell_context():
      return dict(db=db, User=User, Role=Role)


  @app.errorhandler(404)
  def page_not_found(e):
      return render_template('404.html'), 404


  @app.errorhandler(500)
  def internal_server_error(e):
      return render_template('500.html'), 500


  @app.route('/', methods=['GET', 'POST'])
  def index():
      form = NameForm()
      if form.validate_on_submit():
          user = User.query.filter_by(username=form.name.data).first()
          if user is None:
              user = User(username=form.name.data)
              db.session.add(user)
              db.session.commit()
              session['known'] = False
              if app.config['FLASKY_ADMIN']:
                  send_email(app.config['FLASKY_ADMIN'], 'New User',
                             'mail/new_user', user=user)
          else:
              session['known'] = True
          session['name'] = form.name.data
          return redirect(url_for('index'))
      return render_template('index.html', form=form, name=session.get('name'),
                             known=session.get('known', False))
  ```

- 异步发送电子邮件

#### 大型程序的结构

###### 项目结构

- flasky
  - app
    - \__init__.py
    - templates
    - static
    - email.py
    - models.py
    - main
      - \__init__.py
      - errors.py
      - forms.py
      - views.py
  - tests
    - \__init__.py
    - test.py
  - migrations
  - venv
  - requirements.txt
  - config.py
  - manage.py

- 这种结构有4 个顶级文件夹：
  - • Flask程序一般都保存在名为app 的包中；
  - • 和之前一样，migrations文件夹包含数据库迁移脚本；
  - • 单元测试编写在 tests包中；
  - • 和之前一样，venv文件夹包含 Python 虚拟环境。

- 同时还创建了一些新文件：
  - • requirements.txt列出了所有依赖包，便于在其他电脑中重新生成相同的虚拟环境；
  - • config.py 存储配置；
  - • manage.py用于启动程序以及其他的程序任务。

###### 配置选项

###### 程序包

- 程序包用来保存程序的所有代码、模板和静态文件。

###### 使用程序工厂函数

- 在单个文件中开发程序很方便，但却有个很大的缺点，因为程序在**全局作用域**中创建，所以无法动态修改配置。这个问题的解决方法是**延迟创建程序实例，把创建过程移到可显式调用的工厂函数中**。
- 延迟创建程序实例，把创建过程移到可显式调用的工厂函数中。这种方法**不仅可以给脚本留出配置程序的时间，还能够创建多个程序实例**。
- 构造文件导入了大多数正在使用的Flask 扩展。由于尚未初始化所需的程序实例，所以没有初始化扩展，创建扩展类时没有向构造函数传入参数。create_app() 函数就是程序的工厂函数，接受一个参数，是程序使用的配置名。配置类在config.py 文件中定义，其中保存的配置可以使用Flask app.config 配置对象提供的from_object() 方法直接导入程序。至于配置对象，则可以通过名字从config 字典中选择。程序创建并配置好后，就能初始化扩展了。在之前创建的扩展对象上调用init_app() 可以完成初始化过程。

```python
# app/__init__.py：程序包的构造文件

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
```

###### 在蓝本中实现程序功能

- 在蓝图中定义的路由处于休眠状态，直到蓝图注册到程序上后，路由才真正成为程序的一部分。
- 使用位于全局作用域中的蓝本时，定义路由的方法几乎和单脚本程序一样。

- 和程序一样，蓝图可以在单个文件中定义，也可使用更结构化的方式在包中的多个模块中创建。为了获得最大的灵活性，程序包中创建了一个子包，用于保存蓝图。

```python
# app/main/__init__.py：创建蓝本

from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors
```

- 通过实例化一个Blueprint 类对象可以创建蓝本。这个构造函数有两个必须指定的参数：蓝本的名字和蓝本所在的包或模块。和程序一样，大多数情况下第二个参数使用Python 的\__name__ 变量即可。
- 程序的路由保存在包里的app/main/views.py 模块中，而错误处理程序保存在app/main/
  errors.py 模块中。导入这两个模块就能把路由和错误处理程序与蓝本关联起来。注意，这些模块在app/main/\__init__.py 脚本的末尾导入，这是为了避免循环导入依赖，因为在views.py 和errors.py 中还要导入蓝本main。

- 蓝本在工厂函数create_app() 中注册到程序上

  ```python
  # app/_init_.py：注册蓝本

  def create_app(config_name):
      # ...
      from .main import main as main_blueprint
      app.register_blueprint(main_blueprint)
      return app
  ```

- app/main/errors.py：蓝本中的错误处理程序

  > 在蓝本中编写错误处理程序稍有不同，如果使用errorhandler 修饰器，那么只有蓝本中的错误才能触发处理程序。要想注册程序全局的错误处理程序，必须使用app_errorhandler。

  ```python
  from flask import render_template
  from . import main
  @main.app_errorhandler(404)
  def page_not_found(e):
  	return render_template('404.html'), 404
  @main.app_errorhandler(500)
  def internal_server_error(e):
  	return render_template('500.html'), 500
  ```

- app/main/views.py：蓝本中定义的程序路由

  > 在蓝本中编写视图函数主要有两点不同：第一，和前面的错误处理程序一样，路由修饰器由蓝本提供；第二，url_for() 函数的用法不同。你可能还记得，url_for() 函数的第一个参数是路由的端点名，在程序的路由中，默认为视图函数的名字。例如，在单脚本程序中，index() 视图函数的URL 可使用url_for('index') 获取。
  >
  > 在蓝本中就不一样了，Flask 会为蓝本中的全部端点加上一个命名空间，这样就可以在不同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突。命名空间就是蓝本的名字（Blueprint 构造函数的第一个参数），所以视图函数index() 注册的端点名是main.index，其URL 使用url_for('main.index') 获取。
  >
  > url_for() 函数还支持一种简写的端点形式，在蓝本中可以省略蓝本名，例如url_for('.index')。在这种写法中，命名空间是当前请求所在的蓝本。这意味着同一蓝本中的重定向可以使用简写形式，但跨蓝本的重定向必须使用带有命名空间的端点名。
  >
  > 为了完全修改程序的页面，表单对象也要移到蓝本中，保存于app/main/forms.py 模块。

  ```python
  from datetime import datetime
  from flask import render_template, session, redirect, url_for
  from . import main
  from .forms import NameForm
  from .. import db
  from ..models import User
  @main.route('/', methods=['GET', 'POST'])
  def index():
      form = NameForm()
      if form.validate_on_submit():
          # ...
          return redirect(url_for('.index'))
      return render_template('index.html',
          form=form, name=session.get('name'),
          known=session.get('known', False),
          current_time=datetime.utcnow())
  ```

###### 启动脚本

> 顶级文件夹中的manage.py 文件用于启动程序。

- manage.py：启动脚本

  ```python
  import os
  from app import create_app, db
  from app.models import User, Role
  from flask.ext.script import Manager, Shell
  from flask.ext.migrate import Migrate, MigrateCommand
  
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

###### 需求文件

> 程序中必须包含一个requirements.txt 文件，用于记录所有依赖包及其精确的版本号。

- pip 可以使用如下命令自动生成这个文件：

  ```
  pip freeze >requirements.txt
  ```

- 创建这个虚拟环境的完全副本

  ```
  pip install -r requirements.txt
  ```

###### 单元测试

###### 创建数据库

#### 用户认证

- Flask-Login：管理已登录用户的用户会话。
- Werkzeug：计算密码散列值并进行核对。
- itsdangerous：生成并核对加密安全令牌。
- Flask-Mail：发送与认证相关的电子邮件。
- Flask-Bootstrap：HTML 模板。
- Flask-WTF：Web 表单。

###### 使用Werkzeug实现密码散列

> 若想保证数据库中用户密码的安全，关键在于不能存储密码本身，而要存储**密码的散列值**。
>
> 计算密码散列值的函数接收密码作为输入，使用一种或多种加密算法转换密码，最终得到一个和原始密码没有关系的字符序列。
>
> 核对密码时，密码散列值可代替原始密码，因为计算散列值的函数是可复现的：只要输入一样，结果就一样。

- generate_password_hash(password, method=pbkdf2:sha1, salt_length=8)：

  > 这个函数将原始密码作为输入，以字符串形式输出密码的散列值，输出的值可保存在用户数据库中。method 和salt_length 的默认值就能满足大多数需求。

- check_password_hash(hash, password)：

  > 这个函数的参数是从数据库中取回的密码散列值和用户输入的密码。返回值为True 表明密码正确。

```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
```

###### 创建认证蓝本

> 把创建程序的过程移入工厂函数后，可以使用蓝本在全局作用域中定义路由。
>
> 对于不同的程序功能，我们要使用不同的蓝本，这是保持代码整齐有序的好方法。

```python
from flask import Blueprint
auth = Blueprint('auth', __name__)
```

```python
def create_app(config_name):
    # ...
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
```

###### 使用Flask-Login认证用户

> 专门用来管理用户认证系统中的认证状态，且不依赖特定的认证机制。

- pip install flask-login
- Flask-Login要求实现的用户方法
  - is_authenticated() 如果用户已经登录，必须返回True，否则返回False
  - is_active() 如果允许用户登录，必须返回True，否则返回False。如果要禁用账户，可以返回False
  - is_anonymous() 对普通用户必须返回False
  - get_id() 必须返回用户的唯一标识符，使用Unicode 编码字符串

```python
# app/models.py：修改User 模型，支持用户登录

from flask_login import UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

```python
# app/__init__.py：初始化Flask-Login

from flask_login import LoginManager
login_manager = LoginManager()
# LoginManager 对象的session_protection 属性可以设为None、'basic' 或'strong'，以提供不同的安全等级防止用户会话遭篡改。
# 设为'strong' 时，Flask-Login 会记录客户端IP地址和浏览器的用户代理信息，如果发现异动就登出用户。
login_manager.session_protection = 'strong'
# login_view 属性设置登录页面的端点。回忆一下，登录路由在蓝本中定义，因此要在前面加上蓝本的名字。
login_manager.login_view = 'auth.login'
def create_app(config_name):
    # ...
    login_manager.init_app(app)
    # ...
```

```python
# app/models.py：加载用户的回调函数
# 加载用户的回调函数接收以Unicode 字符串形式表示的用户标识符。如果能找到用户，这个函数必须返回用户对象；否则应该返回None。

from . import login_manager
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
```

###### 保护路由

> 为了保护路由只让认证用户访问，Flask-Login 提供了一个login_required 修饰器。

```python
from flask_login import login_required
@app.route('/secret')
@login_required
def secret():
	return 'Only authenticated users are allowed!'
```

###### 添加登录表单