[toc]

#### Django

##### django基礎命令

- 創建項目的指令

  ```shell
  django-admin startproject project_name
  ```

- 創建應用

  ```
  python manage.py startapp app_name
  ```

- 數據庫的遷移

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

- 創建超級用戶

  ```
  python manage.py ceatesuperuser
  ```

- 啟動服務

  ```
  python manage.py runserver
  ```

##### django基礎配置

- 配置服務廣播

  ```
  # setting.py
  ALLOWED_HOSTS = ['*']
  shell: python manage.py runserver ip:port
  ```

- 

##### django操作mysql數據庫

- 在settings文件中修改数据库配置

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'zbj',# 数据库名
          'USER': 'root',
          'PASSWORD': '123456',
          'HOST': '10.8.157.39',# 主机
          'PORT': '3306',
      }
  }
  ```

- 在项目目录下的`__init__.py`文件中添加：

  ```python
  import pymysql
  pymysql.install_as_MySQLdb()
  ```

- 数据库设置好之后，在终端输入：

  ```python
  python manage.py inspectdb > app/models.py # 文件位置自己定義
  python manage.py inspectdb --database develop > myapp/models.py # 指定數據庫
  ```

- 默认生成的models类中，默认是无法对数据库操作的,将`managed`改为`False`:

  ```python
  class Meta:
          managed = False # 改为False
          db_table = 'works'
  ```

- 最后直接迁移即可对数据库进行操作

  ```python
  python manage.py migrate
  ```

##### 項目問題及解決

- 解决 pycharm 编辑器Django项目中objects标黄问题

  > 在模型類定義語句裡面加上一句：objects = models.Manager()

- 

##### 數據庫的增刪改查

- all/get/filter的區別
  - all返回的是QuerySet对象，程序并没有真的在数据库中执行SQL语句查询数据，但支持迭代，使用for循环可以获取数据。
  - get返回的是Model对象，类型为列表，说明使用get方法会直接执行sql语句获取数据
  - filter和all类似，但支持更强大的查询功能

#### Django 獲取數據

##### 基本操作

```python
# 获取所有数据，对应SQL：select * from User
User.objects.all()
# 匹配，对应SQL：select * from User where name = 'Pala'
User.objects.filter(name='Pala')
# 不匹配，对应SQL：select * from User where name != 'Pala'
User.objects.exclude(name='Pala')
# 获取单条数据（有且仅有一条，id唯一），对应SQL：select * from User where id = 724
User.objects.get(id=123)
常用操作
# 获取总数，对应SQL：select count(1) from User
User.objects.count()
# 获取总数，对应SQL：select count(1) from User where name = 'Pala'
User.objects.filter(name='Pala').count()
# 大于，>，对应SQL：select * from User where id > 724
User.objects.filter(id__gt=724)
# 大于等于，>=，对应SQL：select * from User where id >= 724
User.objects.filter(id__gte=724)
# 小于，<，对应SQL：select * from User where id < 724
User.objects.filter(id__lt=724)
# 小于等于，<=，对应SQL：select * from User where id <= 724
User.objects.filter(id__lte=724)
# 同时大于和小于， 1 < id < 10，对应SQL：select * from User where id > 1 and id < 10
User.objects.filter(id__gt=1, id__lt=10)
# 包含，in，对应SQL：select * from User where id in (11,22,33)
User.objects.filter(id__in=[11, 22, 33])
# 不包含，not in，对应SQL：select * from User where id not in (11,22,33)
User.objects.exclude(id__in=[11, 22, 33])
# 为空：isnull=True，对应SQL：select * from User where pub_date is null
User.objects.filter(pub_date__isnull=True)
# 不为空：isnull=False，对应SQL：select * from User where pub_date is not null
User.objects.filter(pub_date__isnull=True)
# 匹配，like，大小写敏感，对应SQL：select * from User where name like '%sre%'，SQL中大小写不敏感
User.objects.filter(name__contains="sre")
# 匹配，like，大小写不敏感，对应SQL：select * from User where name like '%sre%'，SQL中大小写不敏感
User.objects.filter(name__icontains="sre")
# 不匹配，大小写敏感，对应SQL：select * from User where name not like '%sre%'，SQL中大小写不敏感
User.objects.exclude(name__contains="sre")
# 不匹配，大小写不敏感，对应SQL：select * from User where name not like '%sre%'，SQL中大小写不敏感
User.objects.exclude(name__icontains="sre")
# 范围，between and，对应SQL：select * from User where id between 3 and 8
User.objects.filter(id__range=[3, 8])
# 以什么开头，大小写敏感，对应SQL：select * from User where name like 'sh%'，SQL中大小写不敏感
User.objects.filter(name__startswith='sre')
# 以什么开头，大小写不敏感，对应SQL：select * from User where name like 'sh%'，SQL中大小写不敏感
User.objects.filter(name__istartswith='sre')
# 以什么结尾，大小写敏感，对应SQL：select * from User where name like '%sre'，SQL中大小写不敏感
User.objects.filter(name__endswith='sre')
# 以什么结尾，大小写不敏感，对应SQL：select * from User where name like '%sre'，SQL中大小写不敏感
User.objects.filter(name__iendswith='sre')
# 排序，order by，正序，对应SQL：select * from User where name = 'Pala' order by id
User.objects.filter(name='Pala').order_by('id')
# 多级排序，order by，先按name进行正序排列，如果name一致则再按照id倒叙排列
User.objects.filter(name='Pala').order_by('name','-id')
# 排序，order by，倒序，对应SQL：select * from User where name = 'Pala' order by id desc
User.objects.filter(name='Pala').order_by('-id')
```

##### 進階操作

```python
# limit，对应SQL：select * from User limit 3;
User.objects.all()[:3]
# limit，取第三条以后的数据，没有对应的SQL，
# 类似的如：select * from User limit 3,10000000，从第3条开始取数据，取10000000条（10000000大于表中数据条数）
User.objects.all()[3:]
# offset，取出结果的第10-20条数据（不包含10，包含20）,也没有对应SQL，参考上边的SQL写法
User.objects.all()[10:20]
# 分组，group by，对应SQL：select username,count(1) from User group by username;
from django.db.models import Count
User.objects.values_list('username').annotate(Count('id'))
# 去重distinct，对应SQL：select distinct(username) from User
User.objects.values('username').distinct().count()
# filter多列、查询多列，对应SQL：select username,fullname from accounts_user
User.objects.values_list('username', 'fullname')
# filter单列、查询单列，正常values_list给出的结果是个列表，
# 里边里边的每条数据对应一个元组，当只查询一列时，可以使用flat标签去掉元组，
# 将每条数据的结果以字符串的形式存储在列表中，从而避免解析元组的麻烦
User.objects.values_list('username', flat=True)
# int字段取最大值、最小值、综合、平均数
from django.db.models import Sum,Count,Max,Min,Avg
User.objects.aggregate(Count(‘id’))
User.objects.aggregate(Sum(‘age’))
时间查询
# 匹配日期，date
User.objects.filter(create_time__date=datetime.date(2018, 8, 1))
User.objects.filter(create_time__date__gt=datetime.date(2018, 8, 2))
# 匹配年，year
User.objects.filter(create_time__year=2018)
User.objects.filter(create_time__year__gte=2018)
# 匹配月，month
User.objects.filter(create_time__month__gt=7)
User.objects.filter(create_time__month__gte=7)
# 匹配日，day
User.objects.filter(create_time__day=8)
User.objects.filter(create_time__day__gte=8)
# 匹配周，week_day
 User.objects.filter(create_time__week_day=2)
User.objects.filter(create_time__week_day__gte=2)
# 匹配时，hour
User.objects.filter(create_time__hour=9)
User.objects.filter(create_time__hour__gte=9)
# 匹配分，minute
User.objects.filter(create_time__minute=15)
User.objects.filter(create_time__minute_gt=15)
# 匹配秒，second
User.objects.filter(create_time__second=15)
User.objects.filter(create_time__second__gte=15)
# 按天统计归档
today = datetime.date.today()
select = {'day': connection.ops.date_trunc_sql('day', 'create_time')}
deploy_date_count = Task.objects.filter(
    create_time__range=(today - datetime.timedelta(days=7), today)
).extra(select=select).values('day').annotate(number=Count('id'))
```

##### Q的使用

> Q对象可以对关键字参数进行封装，从而更好的应用多个查询，可以组合&(and)、|(or)、~(not)操作符。

```python
from django.db.models import Q

User.objects.filter(Q(role__startswith='sre_'), Q(name='Tom') | Q(name='Pala'))
# 转换成SQL语句如下：
select * from User where role like 'sre_%' and (name='Tom' or name='Pala')
# 通常更多的时候我们用Q来做搜索逻辑，比如前台搜索框输入一个字符，后台去数据库中检索标题或内容中是否包含
_s = request.GET.get('search')

_t = Blog.objects.all()
if _s:
    _t = _t.filter(
        Q(title__icontains=_s) |
        Q(content__icontains=_s)
    )
```

##### 外键：ForeignKey

```python
# 表的结构：
class Role(models.Model):
    name = models.CharField(max_length=16, unique=True)
class User(models.Model):
    username = models.EmailField(max_length=255, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
# 正向查询：
# 查询用户的角色名
_t = User.objects.get(username='Pala')
_t.role.name
# 反向查询
# 查询用户的角色名
_t = User.objects.get(username='Pala')
_t.role.name
# 第二种反向查询：
_t = Role.objects.get(name='Role03')
# 这种方法比上一种_set的方法查询速度要快
User.objects.filter(role=_t)
# 第三种反向查询：
# 如果外键字段有related_name属性，例如models如下：
class User(models.Model):
    username = models.EmailField(max_length=255, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,related_name='roleUsers')
# 那么可以直接用related_name属性取到某角色的所有用户
_t = Role.objects.get(name = 'Role03')
_t.roleUsers.all()
```

##### M2M：ManyToManyField

```python
# 表结构：
class Group(models.Model):
    name = models.CharField(max_length=16, unique=True)
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    groups = models.ManyToManyField(Group, related_name='groupUsers')
# 正向查询:
# 查询用户隶属组
_t = User.objects.get(username = 'Pala')
_t.groups.all()
# 反向查询：
# 查询组包含用户
_t = Group.objects.get(name = 'groupC')
_t.user_set.all()
# 同样M2M字段如果有related_name属性，那么可以直接用下边的方式反查
_t = Group.objects.get(name = 'groupC')
_t.groupUsers.all()
```

##### get_object_or_404

```python
# 正常如果我们要去数据库里搜索某一条数据时，通常使用下边的方法：
_t = User.objects.get(id=734)

# 为了程序兼容和异常判断，我们可以使用下边两种方式:
# 方式一：get改为filter
_t = User.objects.filter(id=724)
# 方式二：使用get_object_or_404
from django.shortcuts import get_object_or_404
_t = get_object_or_404(User, id=724)
# get_object_or_404方法，它会先调用django的get方法，如果查询的对象不存在的话，则抛出一个Http404的异常
# 实现方法类似于下边这样：
from django.http import Http404
try:
    _t = User.objects.get(id=724)
except User.DoesNotExist:
    raise Http404
```

##### get_or_create

> 查找一个对象如果不存在则创建

```python
object, created = User.objects.get_or_create(username='Pala')

try:
    object = User.objects.get(username='Pala')
    created = False
exception User.DoesNoExist:
    object = User(username='Pala')
    object.save()
    created = True
returen object, created
```

##### 执行原生SQL

```python
# Django中能用ORM的就用它ORM吧，不建议执行原生SQL，可能会有一些安全问题，如果实在是SQL太复杂ORM实现不了，那就看看下边执行原生SQL的方法，跟直接使用pymysql基本一致了
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('select * from accounts_User')
    row = cursor.fetchall()
return row
```

##### 連接數據庫的引擎

- MySQLdb

```python
# 適用於python2
# render_to_response 返回模板層
from django.shortcuts import render_to_response
import MySQLdb
 
def book_list(request):
    db = MySQLdb.connect(user='me', db='mydb', passwd='secret', host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT name FROM books ORDER BY name')
    names = [row[0] for row in cursor.fetchall()]
    db.close()
    return render_to_response('book_list.html', {'names': names})
```

- pymysql

```python
# python3一般使用pymysql
# 在app的__init__.py文件中加入
import pymysql
pymysql.install_as_MySQLdb()
# 如果出現bug，則在__init__.py里加上一句以指定版本
pymysql.version_info = (1, 4, 13, "final", 0)
```

- sqlalchemy

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

remote_engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(db_config['host'],db_config['port'],project,db_config['user'],db_config['pwd']))
Session = sessionmaker(bind=remote_engine)
session = Session()
sql = '...'
result = session.execute(sql).fetchall()
```

---



##### Django連接多個數據庫，及多表查詢解決方案

- 在django框架的setting中，有DATABASES设置，在这里配置你要连接的数据库，默认defualt, 另外一个develop你可以自己定义。

- 创建数据库路由文件，在settiing.py 的同级文件下添加database_router.py 文件，内容如下

  ```python
  from django.conf import settings
  DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING
  
  class DatabaseAppsRouter(object):
    
      def db_for_read(self, model, **hints):
          """"Point all read operations to the specific database."""
          if model._meta.app_label in DATABASE_MAPPING:
              return DATABASE_MAPPING[model._meta.app_label]
          return None
  
      def db_for_write(self, model, **hints):
          if model._meta.app_label in DATABASE_MAPPING:
              return DATABASE_MAPPING[model._meta.app_label]
          return None
  
      def allow_relation(self, obj1, obj2, **hints):
          db_obj1 = DATABASE_MAPPING.get(obj1._meta.app_label)
          db_obj2 = DATABASE_MAPPING.get(obj2._meta.app_label)
          if db_obj1 and db_obj2:
              if db_obj1 == db_obj2:
                  return True
              else:
                  return False
          return None
  
      def allow_syncdb(self, db, model):
          if db in DATABASE_MAPPING.values():
              return DATABASE_MAPPING.get(model._meta.app_label) == db
          elif model._meta.app_label in DATABASE_MAPPING:
              return False
          return None
  
      def allow_migrate(self, db, app_label, model=None, **hints):
          if db in DATABASE_MAPPING.values():
              return DATABASE_MAPPING.get(app_label) == db
          elif app_label in DATABASE_MAPPING:
              return False
          return None
  
      def allow_syncdb(self, db, model):
          if db in DATABASE_MAPPING.values():
              return DATABASE_MAPPING.get(model._meta.app_label) == db
          elif model._meta.app_label in DATABASE_MAPPING:
              return False
          return None
  
      def allow_migrate(self, db, app_label, model_name=None, **hints):
          # print db, app_label, model_name, hints
          if db in DATABASE_MAPPING.values():
              return DATABASE_MAPPING.get(app_label) == db
          elif app_label in DATABASE_MAPPING:
              return False
          return None
  
  ```

- 在setting文件中配置数据库路由和app映射, 模型调用时候会自动匹配数据库
  DjangoAdmin为所创建项目名称

  ```python
  DATABASE_ROUTERS = ['DjangoAdmin.database_router.DatabaseAppsRouter']
  DATABASE_APPS_MAPPING = {
      'system': 'default',  # app system 对应数据库 default
      'home': 'develop', # app home 对应数据库 develop
  }
  ```

- 查詢關聯數據

  ```python
  # 生成本地models, 文件位置自己配
  python manage.py inspectdb --database develop > myapp/models.py
  
  # 用原生sql查詢數據
  from django.db import connections
  
  def post(self, request):
     u_list = Teachers.objects.order_by('-id').values()
     temp_ary = []
     with connections['develop'].cursor() as cursor:
     	for obj in u_list:
         	_sql = "select * from category where id = "+ str(obj['category _id']) +" limit 1"
         		cursor.execute(_sql)
         		db_datas = cursor.fetchall()
         		#查询出来是一个元组，根据你的需求获取第几个字段值
     			obj['cate_name'] = db_datas[0][2]
     			temp_list.append(obj)
     return temp_list
  ```

##### django定時任務

- 基礎命令

  ```python
  # 啟動應用
  python manage.py runserver 127.0.0.1:000 # setting.py 配置ALLOWED_HOSTS = ["*"]
  # 啟動worker
  celery -A celerytest worker -l info
  # 發佈任務
  celery -A celerytest beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --pidfile=
  # 啟動flower
  celery -A celerytest flower -address=127.0.0.1 -port=0000
  ```

- celery.py

  ```python
  '''
  通过from future import absolute_import来声明使用绝对引用，这样是为了下面的from celery import Celery引用的是系统celery模块，而不是我们自己创建的celery.py
  '''
  from __future__ import absolute_import, unicode_literals
  from celery import Celery
  import os
  import celerytest.celeryconfig
  
  # from django.utils import timezone
  
  # 为celery指定DJANGO_SETTINGS_MODULE环境变量
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerytest.settings')
  # 创建celery的实例app，要在指定DJANGO_SETTINGS_MODULE环境变量之后
  app = Celery('views')
  # app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
  app.config_from_object('celerytest.celeryconfig',
                         namespace='CELERY')  # 命名空间 namespace='CELERY'定义所有与celery相关的配置的键名要以'CELERY_'为前缀
  # app.now = timezone.now
  
  # Load task modules from all registered Django app configs.
  # 使用app.autodiscover_tasks()来自动发现django应用中的所有tasks模块
  # app.autodiscover_tasks()
  ```

- celeryconfig.py

  ```python
  # from datetime import timedelta
  # from kombu import Exchange, Queue
  # 关闭时区
  # enable_utc = False
  timezone = 'Asia/Shanghai'
  # DJANGO_CELERY_BEAT_TZ_AWARE = False
  broker_url = 'redis://127.0.0.1:6379/1'
  # 指定任务接受的序列化类型
  accept_content = ['json']
  result_backend = 'redis://127.0.0.1:6379/2'
  # 指定任务序列化方式
  task_serializer = 'json'
  # 指定结果序列化的方式
  result_serializer = 'json'
  # 任务过期时间,celery任务执行结果的超时时间
  # CELERY_TASK_RESULT_EXPIRES = 60 * 30
  # 默认队列，如果一个消息不符合其他的队列就会放在默认队列里面
  task_default_queue = 'default'  # 更改默认队列的名称
  task_default_exchange = 'default'
  task_default_routing_key = 'default'
  
  # 异步任务
  imports = ('my_test.views',
             # 'demo.task2',
             )
  
  # 以下代码为写死的定时任务，如果不需要动态添加任务等操作，将以下代码释放来用即可
  # # 设置详细的队列
  # task_queues = {
  #     Queue('default', exchange=Exchange('default'), routing_key='default'),
  #     Queue('priority_high', exchange=Exchange('priority_high', type='direct'), routing_key='priority_high'),
  #     Queue('priority_low', exchange=Exchange('priority_low'), routing_key='priority_low'),
  # }
  
  # # 任务进队列
  # task_routes = {
  #     'demo.tasks.*': {'queue': 'priority_high', 'routing_key': 'priority_high'},
  #     'demo.task2.*': {'queue': 'priority_low', 'routing_key': 'priority_low'},
  # }
  
  
  # 启用celery的定时任务需要设置celerybeat_schedule,celery的定时任务都由celery beat来进行调度。
  # CELERY_CELERYBEAT_SCHEDULE = {
  #     'add-every-30-seconds': {
  #          'task': 'com.fingard.tasks.ebank.control.EBankTask.start',
  #          'schedule': timedelta(seconds=10),       # 每 30 秒执行一次
  #          'args': ('PSB', 5, 8)                    # 任务函数参数
  #     }
  # }
  #
  ```

##### django郵件的配置

- settings.py

  ```python
  # send e-mail
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  #email后端
  EMAIL_USE_TLS = False   #是否使用TLS安全传输协议
  EMAIL_USE_SSL = True    #是否使用SSL加密，qq企业邮箱要求使用
  EMAIL_HOST = 'smtp.exmail.qq.com'   #发送邮件的邮箱 的 SMTP服务器，这里用了qq企业邮箱
  EMAIL_PORT = 465     #发件箱的SMTP服务器端口
  EMAIL_HOST_USER = 'charleschen@xmdaren.com'    #发送邮件的邮箱地址
  EMAIL_HOST_PASSWORD = '*********'         #发送邮件的邮箱密码
  ```

- views.py

  ```python
  from django.core.mail import send_mail  
  # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
  send_mail('Subject here', 'Here is the message.', 'charleschen@xmdaren.com',
      ['to@example.com'], fail_silently=False)
  ```