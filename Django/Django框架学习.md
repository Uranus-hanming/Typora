[toc]

#### Django框架

> 一个重量级的python web框架，Django配备了常用的大部分组件
>
> MVC设计模式：模型层/视图层/控制层

- 基本配置setting.py
- 路由系统urls.py
- 原生HTML模板系统template.py
- 视图view.py
- Model模型，数据库连接和ORM数据库管理model.py
- 中间件middleware.py
- Cookie & Seesion
- 分页
- 数据库后台管理系统admin

##### 项目开发

###### 1. 创建项目

```
django-admin startproject myproject
```

###### 2. 项目目录结构

```
myproject/
|- manage.py
|- myproject
		|- __init.py__
		|- settings.py
		|- urls.py
		|- wsgi.py
```

1. manage.py：项目的主程序
   - python3 manage.py runserver 启动服务
   - python3 manage.py startapp 创建应用
   - python3 manage.py migrate 数据库迁移
   - python manage.py createsuperuser 创建超级用户（先进行数据库迁移）
   - python manage.py makemigrations
   - python manage.py migrate
2. myproject：项目包文件夹
   - \_\_init__.py：包初始化文件
   - wigs.py：WEB服务网关接口的配置文件，仅部署项目时使用
   - urls.py：项目的基础路由配置文件
   - settings.py：Django的配置文件，启动服务时自动调用

###### 3. 视图函数（view）

> 视图函数是用于接受一个浏览器请求并通过**HttpResponse对象**返回数据的函数。
>
> request用于绑定**HttpRequest对象**，通过此对象可以获取浏览器的参数和数据

```python
# file : <项目名>/views.py
from django.http import HttpResponse
def page1_view(request):
    html = "<h1>这是第1个页面</h1>"
    return HttpResponse(html)
```

###### 4. 路由配置url

- settings.py中的ROOT_URLCONF指定了主路由配置列表urlpatterns的文件位置

  ```
  ROOT_URLCONF = 'dadashop.urls'
  ```

- urls.py主路由配置文件

  > urlpatterns是一个**路由-视图函数映射关系的列表**，此列表的映射关系由**url函数**来确定
  >
  > 主路由配置文件可以不处理用户具体路由，即做**路由的分发**（分布式请求处理），具体的请求由各自的应用来进行处理。

  ```python
  from django.urls import path, include

  urlpatterns = [
      path('admin/', admin.site.urls),
  ]
  ```

  ```python
  from django.conf.urls import url, include
  from django.contrib import admin

  urlpatterns = [
  		url(r'^admin', admin.site.urls),
  		url(r'^v1/users', include('user.urls'))，
  		url(r'^person/(?P<name>\w+)/(?P<age>\d{1,2})',views.person_view)
  ]
  ```

- url()函数

  > 用于描述路由与视图函数的对应关系
  >
  > from django.conf.urls import url, include
  >
  > url(regex, views, name=None)

  - regex:字符串类型，匹配的请求路径，允许是正则表达式
  - view:指定路径所对应的**视图处理函数**的名称
  - name:为地址起别名，在模板中地址反向解析时使用

- url反向解析

  > url反向解析是指在视图或模板中，用为url定义的名称来查找或计算出响应的路由
  >
  > url(regex, views, kwargs=None, name="别名")

###### url传递参数的方式和url()函数，及视图函数获取参数的方式

- url传递参数的方式

  1. 位置传递：http://login/p1/p2/p3

  2. 关键字传递：http://login/?p1=1&p2=2&p3=3

     - 视图函数中获取关键字参数

       ```python
       arg1 = retuest.GET.get('p1')
       arg2 = retuest.GET.get('p2')
       arg3 = retuest.GET.get('p3')
       ```

- url()函数对路由传递参数的限制

  - \<数据类型:数据名称>：位置匹配并对对应参数的数据类型进行限定

    > 视图函数的参数获取是按url()函数中的数据名称进行匹配的

    ```python
    from django.urls import path
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('login/<int:age>', view.login),
    ]
    ```

  - (?P<name>pattern)：位置匹配并对对应参数根据正则匹配进行限定，如何对关键字参数进行限定？

    > 视图函数的参数获取是按url()函数中的数据名称进行匹配的

    ```python
    from django.urls import path, include, re_path
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('login/<int:age>', view.login),
        re_path(r'^add/(?P<table>\w+)$', view.log)
    ]
    ```

    

###### 5. HTTP请求

- HTTP1.0定义了三种请求方法： GET, POST 和 HEAD方法(最常用)
- HTTP1.1新增了五种请求方法：OPTIONS, PUT, DELETE, TRACE 和 CONNECT 方法。

- HttpRequest对象

###### 6. HTTP响应 - 状态吗

- Django中的响应对象HttpResponse

  ```
  HttpResponse(content=响应体, content_type=响应体数据类型, status=状态码)
  ```

  - content_type响应体数据类型：
    - `'text/html'`（默认的，html文件）
    - `'text/plain'`（纯文本）
    - `'text/css'`（css文件）
    - `'text/javascript'`（js文件）
    - `'multipart/form-data'`（文件提交）
    - `'application/json'`（json传输）
    - `'application/xml'`（xml文件）

###### 7. GET方式传参

- 通过**查询字符串**将数据传递给服务器

  ```
  URL格式：xxx?name1=value1&name2=value2
  ```

- 服务器端接受数据

  1. 判断request.method的值判断请求方法是否是get请求

     ```django
     if request.method == 'GET'
     		处理GET请求时的业务逻辑
     else:
     		处理其它请求的业务逻辑
     ```

  2. 获取客户端GET请求提交的数据

     ```
     request.GET['参数名']
     request.GET.get['参数名', '默认值']
     request.GET.getlist('参数名')
     ```

###### 8. POST传递参数

- 客户端通过表单等POST请求将数据传递给服务器端

- 服务器端接受数据

  1. 判断request.method的值判断请求方法是否是POST请求

     ```
     if request.method == 'POST'
     		处理POST请求时的业务逻辑
     else:
     		处理其它请求的业务逻辑
     ```

  2. 使用post方式接收客户端数据

     ```
     request.POST['参数名']
     request.POST.get['参数名', '默认值']
     request.POST.getlist('参数名')
     ```

###### 9. django返回数据的方式

1. 返回HttpResponse对象

   ```python
   from django.http import HttpResponse

   def home(request):
      return HttpResponse('这里是伟大的home页面')
   ```

2. 重定向（HttpResponseRedirect）

   ```python
   from django.http import HttpResponseRedirect

   def home(request):
      return HttpResponseRedirect('/login')
   ```

3. 返回模板页面（render）

   ```python
   from django.shorcuts import render

   def home(request):
   	return render(request, 'home.html', {'username': 'kangpc'})
   ```

4. 返回jsion对象（JsonResponse）

   ```python
   from django.http import JsonResponse
   
   def case_list(request):
      return JsonResponse({'code': 0, 'data': {}, 'message': '提交成功'})
   ```

##### 模板Templates

> 模板是可以根据字典数据动态变化的html网页
>
> 模板可以根据视图中传递的字典数据动态生成相应的HTML网页。

###### 1. 通过 loader 获取模板,通过HttpResponse进行响应

```
from django.template import loader
# 1.通过loader加载模板
t = loader.get_template("模板文件名")
# 2.将t转换成 HTML 字符串
html = t.render(字典数据)
# 3.用响应对象将转换的字符串内容返回给浏览器
return HttpResponse(html)
```

###### 2. 使用 render() 直接加载并响应模板

```django
from django.shortcuts import render
return render(request,'模板文件名', 字典数据)
```

##### Django模板语言

###### 1. 模板的传惨

###### 2. 模板的变量

###### 3. 模板的标签

###### 4. 过滤器

###### 5. 模板的继承

##### Django中的应用app

###### 1. 创建应用app

```
python3 manage.py startapp app_name
```

- django应用的结构组成

  1. migrations 文件夹

     > 保存数据迁移的中间文件

  2. \_\_init__.py

     > 应用子包的初始化文件

  3. admin.py

     > 应用的后台管理配置文件

  4. apps.py

     > 应用的属性配置文件

  5. models.py

     > 与数据库相关的**模型映射类**文件

  6. tests.py

     > 应用的单元测试文件

  7. views.py

     > 定义视图处理函数的文件

- 配置安装应用

  > 在 **settings.py** 中配置应用, 让此应用能和整个项目融为一体

  ```
  # file : settings.py 
  INSTALLED_APPS = [
      ... ...,
      'app_name'
  ]
  ```

###### 2. 应用的分布式路由：http://ip:port/v1/users/name/

- include函数

  ```python
  # urls.py主路由配置文件

  from django.conf.urls import url, include
  from django.contrib import admin

  # include('app命字.url模块名')
  urlpatterns = [
  		url(r'^admin', admin.site.urls),
  		url(r'^v1/users/', include('user.urls'))
  ]
  ```

- 应用中的路由urls.py配置文件

  ```python
  from django.conf.urls import url
  from . import views
  
  urlpatterns = [
      url(r'^name/$', views.Class_name.as_view()),
  ]
  ```



##### 数据库和模型

###### 1. mysql数据库的配置

1. 安装pymysql：用作Python和mysql的接口
	- sudo pip install pymysql
2. 修改项目中__init__.py 加入如下内容来提供pymysql引擎的支持
	```python
	import pymysql
	pymysql.install_as_MySQLdb()
	```
3. 创建数据库：create database 数据库名 default charset utf8 ;

4. setting.py中的mysql相关配置

   ```shell
   DATABASES = {
       'default' : {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'mywebdb',  # 数据库名称,需要自己定义
           'USER': 'root',
           'PASSWORD': '123456',  # 管理员密码
           'HOST': '127.0.0.1',
           'PORT': 3306,
       }
   }
   ```

###### 2. 模型（Models）

- 模型是一个Python类，它是由django.db.models.Model派生出的子类
- 一个模型类代表数据库中的一张数据表
- 模型类中每一个类属性都代表数据库中的一个字段
- 模型是数据交互的接口，是表示和操作数据库的方法和方式

###### 3. ORM框架

> ORM（Object Relational Mapping）即对象关系映射。它是一种程序技术，允许使用类和对象对数据库进行操作，从而避免通过SQL语句操作数据库。
>
> ORM建立了**模型类和表**之间的对应关系，，允许我们通过**面向对象的方式**来操作数据库

- 作用：

  1. 建立模型类和表之间的对应关系，允许我们通过面向对象的方式来操作数据库；
  2. 根据设计的模型类生成数据库中的表格；
  3. 通过简单的配置就可以进行数据库的切换

- 优点：

  1. 只需要面向对象编程，不需要面向数据库编写代码

     > 对数据库的操作都转化成对类属性和方法的操作；
     >
     > 不用编写各种数据库的sql语句；

  2. 实现了数据模型与数据库的解耦，屏蔽了不同数据库操作上的差异

     > 不在关注用的是mysql/oracle...等数据库的内部细节；
     >
     > 通过简单的配置就可以轻松更换数据库，不需要修改代码

- 缺点：相比直接使用SQL语句操作数据库，性能上有损失

###### 4. 示例

1. 新建app

   ```
   python3 manage.py startapp bookstore
   ```

2. models.py中添加模型类

   ```shell
   # file : bookstore/models.py
   from django.db import models

   # Create your models here.
   class Book(models.Model):

       title = models.CharField("书名",max_length=50,default='', unique=True)
       #00000.00
       price = models.DecimalField("定价", max_digits=7,decimal_places=2, default=0.0)
       #新添字段时，记住加default值
       pub = models.CharField('出版社', max_length=200, default='')
       market_price = models.DecimalField('零售价', max_digits=7, decimal_places=2, default=0.0)
       
       class Mata:
       	db_table = "Book_massage" # 自定义数据库表名
       
       def __str__(self):
           return '%s_%s_%s_%s'%(self.title,self.price,self.pub,self.market_price)
   ```

3. 在setting.py中注册app

   ```shell
   # file : setting.py
   INSTALLED_APPS = [
       ...
       'bookstore',
   ]
   ```

4. 数据库迁移

   > 迁移是Django同步你对模型所做的更改（添加字段、删除模型等）到数据库的方式

   - 生成或更新迁移文件

     > 在每个应用下的models.py文件生成一个中间文件

     ```
     python3 manage.py makemigrations
     ```

   - 执行迁移脚本程序

     > 目的是将每个应用下的migrations.py目录中的中间文件同步到数据库

     ```
     python3 manage.py migrate
     ```

###### 5. 字段类型

1. BooleanField()
    - 数据库类型:tinyint(1)
    - 编程语言中:使用True或False来表示值
    - 在数据库中:使用1或0来表示具体的值
2. CharField()
    - 数据库类型:varchar
    - 注意:
        - 必须要指定max_length参数值
3. DateField()
    - 数据库类型:date
    - 作用:表示日期
    - 编程语言中:使用字符串来表示具体值
    - 参数:
        - DateField.auto_now: 每次保存对象时，自动设置该字段为当前时间(取值:True/False)。
        - DateField.auto_now_add: 当对象第一次被创建时自动设置当前时间(取值:True/False)。
        - DateField.default: 设置当前时间(取值:字符串格式时间如: '2019-6-1')。
        - 以上三个参数只能多选一
4. DateTimeField()
    - 数据库类型:datetime(6)
    - 作用:表示日期和时间
    - auto_now_add=True

5. DecimalField()
    - 数据库类型:decimal(x,y)
    - 编程语言中:使用小数表示该列的值
    - 在数据库中:使用小数
    - 参数:
        - DecimalField.max_digits: 位数总数，包括小数点后的位数。 该值必须大于等于decimal_places.
        - DecimalField.decimal_places: 小数点后的数字数量

    - 示例:
        ```
        money=models.DecimalField(
            max_digits=7,
            decimal_places=2,
            default=0.0
        )
        ```
6. FloatField()
    - 数据库类型:double
    - 编程语言中和数据库中都使用小数表示值
7. EmailField()
    - 数据库类型:varchar
    - 编程语言和数据库中使用字符串
8. IntegerField()
    - 数据库类型:int
    - 编程语言和数据库中使用整数
9. URLField()
    - 数据库类型:varchar(200)
    - 编程语言和数据库中使用字符串
10. ImageField()
  - 数据库类型:varchar(100)
  - 作用:在数据库中为了保存图片的路径
  - 编程语言和数据库中使用字符串
  - 示例:
      ```
      image=models.ImageField(
          upload_to="static/images"
      )
      ```
  - upload_to:指定图片的上传路径
      在后台上传时会自动的将文件保存在指定的目录下
11. TextField()
    - 数据库类型:longtext
    - 作用:表示不定长的字符数据

###### 6. 字段选项

> 指定创建的列的额外的信息；允许出现多个字段选项，用,隔开。

1. primary_key
    - 如果设置为True,表示该列为主键,如果指定一个字段为主键，则此数库表不会创建id字段
2. blank
    - 设置为True时，字段可以为空。设置为False时，字段是必须填写的。
3. null
    - 如果设置为True,表示该列值允许为空。
    - 默认为False,如果此选项为False建议加入default选项来设置默认值
4. default
    - 设置所在列的默认值,如果字段选项null=False建议添加此项
5. db_index
    - 如果设置为True,表示为该列增加索引
6. unique
    - 如果设置为True,表示该字段在数据库中的值必须是唯一(不能重复出现的)
7. db_column
    - 指定列的名称,如果不指定的话则采用属性名作为列名
8. verbose_name
    - 设置此字段在admin界面上的显示名称。
- 示例:
    ```python
    # 创建一个属性,表示用户名称,长度30个字符,必须是唯一的,不能为空,添加索引
    name = models.CharField(max_length=30, unique=True, null=False, db_index=True)
    ```

##### 数据库的基本操作

> 数据库的基本操作包括增删改查操作

###### 1. 管理器对象

> 每个继承子models.Model的模型类，都会有一个objects对象被同样继承下来，即管理器对象。
>
> 作用是实现数据库的增删改查操作

###### 2. 新增数据

> 创建数据中每一条记录就是创建一个数据对象

1. MyModel.objects.create(属性1=值1, 属性2=值1,…)
2. 创建 MyModel 实例对象,并调用 save() 进行保存

```python
obj = MyModel(属性=值,属性=值)
obj.属性=值
obj.save()
```

###### 3. 查询数据（table_name.objects.查询接口）

- 查询接口

  | 说明                               | 方法            |
  | ---------------------------------- | --------------- |
  | 查询全部记录，返回QuerySet查询对象 | all()           |
  | 查询符合条件的单一记录             | get(条件判断)   |
  | 查询符合条件的多条记录             | filter()        |
  | 查询符合条件之外的全部记录         | exclude()：排除 |

- all()方法：MyModel.objects.all()

  > 查询MyModel实体中所有的数据，返回QuerySet容器对象,内部存放 MyModel 实例
  >
  > 等同于：select * from table

  ```shell
  from bookstore import models

  books = models.Book.objects.all()
  for book in books:
  	print("书名", book.title, '出版社:', book.pub)
  ```

- get()方法：MyModel.objects.get(条件)

  > 返回满足条件的唯一一条数据，返回MyModel对象

  ```shell
  from bookstore import models
  book = models.Book.objects.get(id=1)
  	print(book.title)
  ```

- filter()方法：MyModel.objects.filter(字段__条件)

  1. `__exact` : 等值匹配 exact(准确的、精确的)
      ```python
      Author.objects.filter(id__exact=1)
      # 等同于select * from author where id = 1
      ```
  2. `__contains` : 包含指定值

      ```python
      Author.objects.filter(name__contains='w')
      # 等同于 select * from author where name like '%w%'
      ```
  3. `__startswith` : 以 XXX 开始
  4. `__endswith` : 以 XXX 结束
  5. `__gt` : 大于指定值
      ```python
      Author.objects.filer(age__gt=50)
      # 等同于 select * from author where age > 50
      ```
  6. `__gte` : 大于等于
  7. `__lt` : 小于
  8. `__lte` : 小于等于
  9. `__in` : 查找数据是否在指定范围内
      ```python
      Author.objects.filter(country__in=['中国','日本','韩国'])
      # 等同于 select * from author where country in ('中国','日本','韩国')
      ```
  10. `__range`: 查找数据是否在指定的区间范围内
    ```python
    # 查找年龄在某一区间内的所有作者
    Author.objects.filter(age__range=(35,50))
    # 等同于 SELECT ... WHERE Author BETWEEN 35 and 50;
    ```

- exclude()方法：MyModel.objects.exclude(条件)

  > 返回不包含此 `条件` 的 全部的数据集

  ```shell
  books = models.Book.objects.exclude(pub="清华大学出版社", price__gt=50)
  for book in books:
  	print(book)
  ```

###### 4. 修改数据

1. 修改单个实体的某个字段值的步骤

   1. 查：通过get()得到要修改的实体对象
   2. 改：通过`对象.属性` 的方式修改数据
   3. 保存：通过`对象.save()` 保存数据

   ```python
   from bookstore import models
   abook = models.Book.objects.get(id=10)
   abook.market_price = "10.5"
   abook.save()
   ```

2. 通过QuerySet批量修改对应的全部字段（MyModel.update(属性=值)）

   > 直接调用QuerySet的update(属性=值) 实现批量修改

   ```python
   # 将 id大于3的所有图书价格定为0元
   from bookstore import models
   books = models.Book.objects.filter(id__gt=3)
   books.update(price=0)
   # 将所有书的零售价定为100元
   books = Book.objects.all()
   books.update(market_price=100)
   ```

###### 5. 删除数据

> 删除单个MyModel对象或删除一个查询结果集(QuerySet)中的全部对象都是调用 delete()方法

1. 删除单个对象

   - 查找查询结果对应的一个数据对象
   - 调用这个数据对象的delete()方法实现删除

   ```python
   from bookstore import models
   book = models.Book.objects.get(id=1)
   book.delete()
   ```

2. 删除查询结果集

   - 查找查询的结果集中满足条件的全部QuerySet查询集合对象
   - 调用查询集合对象的delete()方法实现删除

   ```
   # 删除全部作者中，年龄大于65的全部信息
   auths = Author.objects.filter(age__gt=65)
   auths.delete()
   ```

##### admin后台数据管理

> django会收集所有已注册的模型类，为这些模型类提供管理界面供开发者使用

1. 创建后台管理账号

   ```
   python3 manage.py createsuperuser
   ```

2. 用注册的账号登录后台管理界面

   - 在终端启动django服务：python3 manage.py runserver 127.0.0.1:8000
   - 后台管理的登录地址：http://127.0.0.1:8000/admin

##### cookies和session

###### cookies

- cookies是保存在**客户端浏览器**上的存储空间，通常用来记录浏览器端自己的信息和当前连接的确认信息

- cookies在浏览器上是以**键-值对**的形式进行存储，键和值都是以**ASCII字符串**的形式存储

- cookies内部的数据会在每次访问此网址时都会携带到服务器端

- 在Django服务器端来设置浏览器的cookies必须通过HttpResponse对象来完成

- 添加、修改COOKIE

  ```
  HttpRespone.set_cookie(key, value='', max_age=None, expires=None)
  ```

  - key: cookie的名字
  - value: cookie的值
  - max_age: cookie存活时间，秒为单位
  - expires: 具体过期时间
  - 当不指定max_age和expires时，关闭浏览器时此数据失效

- 删除COOKIE

  ```python
  # HttpResponse.delete_cookie(key)

  responds = HttpResponse("已删除 my_var1")
  responds.delete_cookie('my_var1')
  ```

- django中的对象

  1. 使用相应对象HttpRsponse将cookie保存到客户端

  ```python
  from django.http import HttpResponse
  resp = HttpResponse()
  resp.set_cookie('cookies名', cookies值, 超期时间)
  ```

  2. 使用render对象将cookie保存到客户端

  ```python
  from django.shortcuts import render
  resp = render(request,'xxx.html',locals())
  resp.set_cookie('cookies名', cookies值, 超期时间)
  ```

  3. 获取cookie

     ```python
     # 通过 request.COOKIES 绑定的字典(dict) 获取客户端的 COOKIES数据
     value = request.COOKIES.get('cookies名', '没有值!')
     print("cookies名 = ", value)
     ```

###### session 会话控制

- 是在服务器上开辟一段空间用于保留浏览器和服务器交互时的重要数据

- session的作用

  - http协议是无状态的：每次请求都是一次新的请求，不会记得之前通信的状态
  - 实现**状态保持**的方式：在客户端或服务器端存储与会话有关的数据
  - 推荐使用sesison方式，因为所有数据存储在服务器端，数据更加安全

- session的实现

  - 使用 session 需要在浏览器客户端启动 cookie，且用在cookie中存储sessionid
  - 每个客户端都可以在服务器端有一个独立的Session

- 在django的settings.py中配置Session

  - 向 INSTALLED_APPS 列表中添加：

    ```
    INSTALLED_APPS = [
        # 启用 sessions 应用
        'django.contrib.sessions',
    ]
    ```

  - 向 MIDDLEWARE 列表中添加：

    ```
    MIDDLEWARE = [
        # 启用 Session 中间件
        'django.contrib.sessions.middleware.SessionMiddleware',
    ]
    ```

  - SESSION_COOKIE_AGE

    > 作用: 指定sessionid在cookies中的保存时长(默认是2周)，如下:
    >
    > `SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2`

  - SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    > 设置只要浏览器关闭时,session就失效(默认为False)

  - 当使用session时需要迁移数据库,否则会出现错误

    ```
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    ```

##### 缓存

> Django中提供多种缓存方式，如需使用需要在settings.py中进行配置
>
> 缓存是一类可以更快的读取数据的介质统称，也指其它可以**加快数据读取的存储方式**。一般用来存储临时数据，常用介质的是读取速度很快的内存redis等。

###### 1. 数据库缓存

> Django可以将其缓存的数据存储在您的数据库中

- settings.py

  ```shell
  CACHES = {
      'default': {
          'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
          'LOCATION': 'my_cache_table',   # 控制缓存保存在哪个表里
          'TIMEOUT': 300,  #缓存保存时间 单位秒，默认值为300, 
          'OPTIONS':{
              'MAX_ENTRIES': 300, #缓存最大数据条数
              'CULL_FREQUENCY': 2,#缓存条数达到最大值时 删除1/x的缓存数据
          }
      }
  }
  ```

- view.py

  ```python
  from django.views.decorators.cache import cache_page

  @cache_page(30)
  def test_cache(request):
      # time.sleep(3)
      t1 = time.time()
      return HttpResponse('t1 is %s'%(t1))
      # return render(request, 'test_cache.html', locals())
  ```

- 迁移缓存表

  ```
  python3 manage.py createcachetable
  ```

###### 2. 文件系统缓存

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',#这个是文件夹的路径
        #'LOCATION': 'c:\test\cache',#windows下示例
    }
}
```

###### 3. 本地内存缓存

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}
```

###### 4. Django中使用缓存

1. 在视图view中使用cache

   ```python
    from django.views.decorators.cache import cache_page

   @cache_page(30)  -> 单位s
   def my_view(request):
       ...
   ```

2. 在路由中使用

   ```python
   from django.views.decorators.cache import cache_page

   urlpatterns = [
       path('foo/', cache_page(60)(my_view)),
   ]
   ```

3. 在模板中使用

   ```python
   {% load cache %}
   {% cache 500 sidebar request.user.username %}
       .. sidebar for logged in user ..
   {% endcache %}
   ```

###### 5. 实例应用

1. settings.py添加配置

   ```shell
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           }
       },
       "verify_email": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/2",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           }
       },

       "carts": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/4",
           "TIMEOUT": None,
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
               "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
               # "SERIALIZER": "django_redis.serializers.json.JSONSerializer"
           }
       },

       "goods": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/5",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
               "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor"
           }
       },
       "goods_detail": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/6",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
               "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor"
           }
       },

   }
   ```

2. 在项目目录运行指令

   ```shell
   python3 managy.py createcachetable
   ```

3. django中对缓存表的使用

   > 使用**cache_page函数**，这个cache_page函数相当于**在执行视图函数之前**先看缓存里面有没有要查的数据，如果有直接读缓存，如果没有就继续往下走视图函数，视图函数走完，再往缓存里存储视图函数返回的数据

   1. 使用装饰器

      ```python
      from django.views.decorators.cache import cache_page

      @cache_page(30)  # 单位秒
      def test_cache(request):
      	...
      ```

   2. 在路由中修改

      ```python
      from django.views.decorators.cache import cache_page
      
      urlpatterns = [
        	url(r'foo/', cache_page(30)(test_cache)),
      ]
      ```

      

##### 中间件 Middleware

> 中间件是 **Django 请求/响应处理的钩子框架**。它是一个轻量级的、低级的“插件”系统，**用于全局改变 Django 的输入或输出**。
>
> 每个中间件组件负责做一些特定的功能。

###### 1. 中间件类

- 中间件类须继承自 `django.utils.deprecation.MiddlewareMixin`类
- 中间件类须实现下列五个方法中的一个或多个:
    - `def process_request(self, request):` 执行**路由之前**被调用，在每个请求上调用，返回None或HttpResponse对象 
    - `def process_view(self, request, callback, callback_args, callback_kwargs):` 调用**视图之前**被调用，在每个请求上调用，返回None或HttpResponse对象
    - `def process_response(self, request, response):` 所有**响应返回浏览器前**被调用，在每个请求上调用，返回HttpResponse对象
    - `def process_exception(self, request, exception):` 当处理过程中**抛出异常时**调用，返回一个HttpResponse对象
    - `def process_template_response(self, request, response):` 在**视图函数执行完毕且试图返回的对象中包含render方法时**被调用；该方法需要返回实现了render方法的响应对象
- 注： 中间件中的大多数方法在返回None时表示忽略当前操作进入下一项事件，当返回HttpResponese对象时表示此请求结束，直接返回给客户端

###### 2. 编写中间件类

```python
# file : middleware/mymiddleware.py
from django.http import HttpResponse, Http404
from django.utils.deprecation import MiddlewareMixin

class MyMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        print("执行路由之前 process_request 被调用")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("调用视图之前 process_view 被调用")

    def process_response(self, request, response):
        print("响应返回浏览器前 process_response 被调用")
        return response

    def process_exception(self, request, exception):
        print("抛出异常时 process_exception 被调用")

    def process_template_response(self, request, response):
        print("视图函数执行完毕并且视图返回的对象包含render方法时 process_template_response 被调用")
        return response
```

###### 3. 注册中间件

```
# file : settings.py
MIDDLEWARE = [
    ...
       ]
```

###### 4. 常用中间件配置

```shell
MIDDLEWARE = [
	# 做了一些安全处理的中间件。比如设置XSS防御的请求头，比如做了http协议转为https协议的工作等。
    'django.middleware.security.SecurityMiddleware', # 安全中间件，验证请求的整数
    
    # 会给request添加一个处理好的session对象。
    'django.contrib.sessions.middleware.SessionMiddleware', # session中间件
    
    'corsheaders.middleware.CorsMiddleware', 
    
    # 通用中间件，会处理一些URL，比如baidu.com会自动的处理成www.baidu.com。比如/blog/111会处理成/blog/111/自动加上反斜杠。
    'django.middleware.common.CommonMiddleware', # 通用中间件，验证请求的路径是否是格式化的
    
    # 保护中间件，在提交表单的时候会必须加入csrf_token，cookie中也会生成一个名叫csrftoken的值，也会在header中加入一个HTTP_X_CSRFTOKEN的值来放置CSRF攻击。SessionMiddleware必须出现在CsrfMiddleware之前。
    'django.middleware.csrf.CsrfViewMiddleware', # 用于跨站伪造请求
    
    # 会给request添加一个user对象的中间件。该中间件必须在sessionmiddleware后面。
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 验证用户是否为合法用户
    
    # 消息处理中间件。为了在多个模板中可以使用我们返回给模板的变量，并且简化操作。
    'django.contrib.messages.middleware.MessageMiddleware', # 消息中间件
    
    # 防止通过浏览器页面跨Frame出现clickjacking（欺骗点击）攻击出现。
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # 防点击劫持中间件
]
```

###### 5. 自定义中间件的开发

> 1. 定义一个中间件工厂函数（装饰器），然后返回一个可以被调用的中间件。
> 2. 中间件工厂函数需要接收一个可以调用的get_response对象。
> 3. 返回的中间件也是一个可以被调用的对象，并且像视图一样需要接受一个request对象参数，返回一个response对象。

- step1: 在子应用新建一个middleware.py文件用于定义中间件

- step2: 在该新建的.py文件中定义中间件

  ```python
  def mid1(get_response): # 接受响应对象
  	print('in midl) # 此处编写的代码仅在django第一次配置和初始化的时候执行一次
      def middleware(request):  
            print('1') # 此处编写的代码会在每个请求处理视图前被调用
            response = get_response(request) # 视图、响应对象
            print('2') # 此处编写的代码会在每个请求处理视图之后被调用
            return response
      return middleware
  ```

- step3: 在settings文件中将自定义的中间件注册。格式：“子应用名.中间件py文件名.外函数名”，即中间件的python路径

  ```shell
  MIDDLEWARE = [
    	'firstapp.middleware.midl'
  ]
  ```

###### 6. 中间件调用顺序

> 类似递归顺序：
>
> 如果中间件的位置并不在中间件列表的最后一位的话，此时response指向的就是下一个中间件；
>
> 如果中间件位于中间件列表中的最后以为，此时response指向的就是访问的视图

- 在请求视图被处理前：中间件由上至下依次执行
- 在请求视图被处理后：中间件由下至上依次执行

###### 7. 示例

- 添加过滤请求次数中间件

  ```python
  # file:mymiddleware.py
  from django.http import HttpResponse
  from django.utils.deprecation import MiddlewareMixin
  import re
  class MWare(MiddlewareMixin):
     count_dict = {} #创建用于统计次数的字典
     def process_request(self,request): # 执行路由之前被调用，在每个请求上调用，返回None或HttpResponse对象
        request_ip = request.META['REMOTE_ADDR'] #获取请求IP
        request_url = request.path_info #获取请求URL
        if re.match(r'^/test',request_url): #匹配请求是否以/test开头
              times = self.count_dict.get(request_ip,0) #查询当前IP的请求次数，默认为0
              self.count_dict[request_ip]= times + 1 #请求次数 + 1
              if times < 5: #如果请求次数＜5次，请求正常通过
                 return
              else: #如果请求次数＞5次，则返回HttpResponse，阻止请求
                 return HttpResponse("访问次数超过5次，请求失败")
        else: #如果不是以/test开头则直接正常通过
              return
  ```

- 注册中间件

  ```shell
  MIDDLEWARE = [
    	'middleware.mymiddleware.MWare'
  ]
  ```

###### 8. django请求流程图

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-CjB5ZZi7-1678526655145)(C:\Users\Administrator\Desktop\hanming\project\django请求流程.png)]



##### 跨站请求伪造保护 CSRF

- 跨站请求伪造攻击：用你的认证信息在你的网站上操作

  > 某些恶意网站上包含链接、表单按钮或者JavaScript，它们会利用登录过的用户在浏览器中的认证信息试图在你的网站上完成某些操作，这就是跨站请求伪造(CSRF，即Cross-Site Request Forgey)。

- **CSRF中间件**和**模板标签**提供对跨站请求伪造简单易用的防护。

- CSRF的作用：不让其它表单提交到此Django服务器

- 解决方案

  1. 取消csrf验证

     - 全局禁用：

       > settings.py 中 MIDDLEWARE 中的 django.middleware.csrf.CsrfViewMiddleware 的中间件。
       >
       > 对于需要保护的视图加装饰器@csrf_protect

     - 针对性禁用：

       > 在表单提交的对应视图函数上加上一个装饰器@csrf_exempt

       

  2. 通过验证csrf_token验证

     > 需要在表单中增加一个标签：
     >
     > {% csrf_token %}