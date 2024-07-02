[toc]

#### 项目开发事项

1. 开发模块目录：bk_power/src/api/bk_power/ecology

2. 序列化器目录：bk_power/ecology/serializers

3. 数据库模型类：bk_power/ecology/models

4. run/debug configurations

   - `D:/modou/bk_power/src/api/manage.py`

   - 执行命令

     ```python
     runserver 127.0.0.1:8000
     makemigrations
     migrate
     ```

   - Paths to ".env" file：src/api/bk_power/settings/run.env

5. 环境变量配置

   - 安装插件 EnvFile(file->settings->plugins)
   - 将run.env文件存放在\src\api\bk_power\settings 目录下，修改DB_PASSWORD=123456

6. 安装依赖

   ```shell
   pip install poetry
   # 初次直接执行
   poetry install
   pip install lib_tar目录下的.tar.gz
   ```

7. bk_power\settings\overlays\front.py配置静态文件

   ```python
   # dist静态文件存放目录：api/bk_power/dist
   STATICFILES_DIRS = (PROJECT_SOURCE_DIR / "api/bk_power/dist/static",)
   ```

8. 预防csrf跨域请求

   ```python
   # D:\modou\bk_power\src\api\bk_power\settings\django.py 目录下添加中间件
   MIDDLEWARE = [
       "bk_power.tests.csrf_middleware.NotUseCsrfTokenMiddlewareMixin",
   ]
   
   # csrf_middleware.py文件存放在bk_power/tests目录下
   ```

9. 注释\bk_power\ecology\apps.py下的代码

   ```python
   # from bk_power.ecology import signals  # noqa
   # if settings.BK_APP_CODE and settings.SECUREKEY_APM:
   #     BluekingInstrumentor().instrument()
   ```

10. 在viewsets下的每个文件夹下的__ini\_\_.py里添加如下命令

   ```python
   from .xxx import * # noqa
   from .yyy import * # noqa
   # 有多有个.py文件就添加多少个
   # 目的是可以跨目录导入，如：viewsets文件夹下有个knowledge_school文件夹，其下有两个.py文件，分别是__ini.py、knowledge_info.py，knowledge_info.py里有KnowledgeViewSet类，__ini.py文件里直接导入from .knowledge_info import *，viewsets.KnowledgeViewSet就可以直接访问到。
   ```

11. 项目权限管理（ecology\permissions\sys.py）

12. 项目合并注意事项

    - 上传代码的时候记得要先拉一下，免得冲突了

    - 每次commit的时候执行一下 pre-commit run --all-files

    - bk_power\settings\overlays\front.py

      ```
      STATICFILES_DIRS = (PROJECT_SOURCE_DIR / "api/bk_power/dist/static",)
      STATICFILES_DIRS = (PROJECT_SOURCE_DIR / "front/dist/static",)
      ```

    - bk_power\settings\django.py

      ```
      不提交：
      "bk_power.tests.csrf_middleware.NotUseCsrfTokenMiddlewareMixin"
      ```

    - 迁移文件备份

    - 不提交：bk_power\tests\csrf_middleware.py

    

#### 项目配置setting

###### 1. manage.py

```python
# 配置文件目录配置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bk_power.settings.overlays.prod")
```

###### 2. django.py（配置文件）??剖析每项配置和作用

- BASE_DIR
- SECRET_KEY
- DEBUG
- INSTALLED_APPS：
- MIDDLEWARE：中间件
- ROOT_URLCONF = "bk_power.urls"：路由根目录配置
- TEMPLATES：
- WSGI_APPLICATION
- TIME_ZONE
- 数据库信息配置
- AUTH_PASSWORD_VALIDATORS

###### 3. run.env环境变量配置文件

- 在哪里配置目录路径？api\bk_power\settings\run.env



#### 路由（bk_power\urls.py）

###### 1. 主路由

```python
from django.urls import include, re_path
# include: 路由分发
# re_path: 正则匹配路由

urlpatterns = [
	re_path(r"^", include("bk_power.ecology.urls")),
]
```

###### 2. 路由注册

```python
from rest_framework.routers import SimpleRouter
from bk_power.ecology import viewsets
router = SimpleRouter()

# http://127.0.0.1:8000/api/v1/knowledge_info/
# 注意：knowledge_list后不要加/，KnowledgeAPIView视图类中如果没有类属性queryset，则需要添加basename="xxx"
router.register(r"api/v1/knowledge_list", viewsets.KnowledgeAPIView)

urlpatterns = router.urls
```

###### 3. 路由解析

> http://127.0.0.1:8000/api/v1/knowledge_info/25/?page_size=20&page=1&code__contains=

- 25：单例查询
- page_size：单页条目
- page：页码
- code_contains：？
- 模糊过滤、搜索？

#### ORM模型

- makemigrations/migrate 如何找到models模型类？

###### 1. 自定义类

```python
from django.db import models

# 一个类对应一张表，类的属性对应表的字段，类名以大写开头，驼峰状；属性名都是小写，以_隔开。
class KnowledgeSchool(OperationInfoMixin):
    # models中有不同的类，对应表字段的不同类型，实例化参数对应字段的约束
    name = models.CharField(max_length=200, verbose_name='产品名称')
    knowledge_type = models.ForeignKey(to='KnowledgeType', on_delete=models.CASCADE, null=True)
    is_banner = models.BooleanField(verbose_name='是否banner展示', default=False)
    pdf_desc = models.TextField(verbose_name="PDF详情", blank=True, null=True)

    class Meta:
        unique_together = ("title", "update_date") # 两个字段组合唯一
        db_table = "knowledge_school" # 数据库名，规范：小写，以_隔开
        ordering = ["-is_top", "-updated_at"]
        verbose_name = "知识学堂库"
        verbose_name_plural = verbose_name
        
# django有几种字段类型，分别对应models中的哪个类，以及字段的约束类型有哪些，参数如何表示？
# 表的关联关系：一对一，一对多，多对多
# 表关联关系之间的联表查询
```

###### 2. 父类继承(OperationInfoMixin)

```python
class OperationInfoMixin(models.Model):
    """操作记录基础信息"""

    created_by = models.CharField(verbose_name="创建者", max_length=64, blank=True, db_index=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_by = models.CharField(verbose_name="更新者", max_length=64, blank=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        abstract = True # 虚拟表，在数据库不进行创建

    @classmethod
    def update_and_save(cls, queryset, **kwargs):
        updated_objects = []
        for obj in queryset:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.save()
            updated_objects.append(obj)
        return updated_objects
```

###### 3. 字段类型（属性名=models.字段类型(选项)）

> **AutoField**，主键，自动增长的IntegerField，通常不用指定，不指定时Django会自动创建属性名为id的自动增长属性。
>
> 不允许使用连续的下划线

- models.**CharField**(verbose_name="", help_text="", max_length=128, blank=True, null=True, choices=[('key', 'value'), (), ()] # 序列化器中使用source=get_xxx_display来显示

  > 字符串

- models.**IntegerField**(verbose_name="", help_text="", blank=True, null=True)

- models.**SmallIntegerField**(verbose_name="", help_text="", blank=True, null=True)

  > 小整数时一般会用到

- models.**FloatField**(verbose_name="", help_text="", blank=True, null=True)

  > 浮点数

- models.**JSONField**(verbose_name="", help_text="", default=list/dict)

- models.**TextField**(verbose_name="", help_text="", blank=True, null=True)

  > 大文本字段，一般超过4000个字符时使用。

- models.**DateTimeField**(verbose_name="创建时间", help_text="创建时间", auto_now_add=True, blank=True, null=True)

  > 参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为false。

- models.**DateTimeField**(verbose_name="更新时间", help_text="更新时间", auto_now=True)

  > 参数auto_now表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为false。

- models.**ForeignKey**(GameTestDevice, verbose_name="设备", help_text="设备", on_delete=models.CASCADE, blank=True, null=True) # on_delete有几种类型？

  > 建立一对多关系，ForeignKey在多的一边，及在子表中，可以使用source="xxx.yyy.zzz"，或者depth=n展开
  >
  > 自关联（把关联属性指向了自己）：models.ForeignKey('self', null=True, blank=True)

  - **on_delete解释：** 当子表中的某条数据删除后，关联的外键操作。

    1. SET_NULL：on_delete = models.SET_NULL

       > 置空模式，删除时，外键字段被设置为空，前提就是blank=True, null=True,定义该字段时，允许为空。

    2. CASCADE：on_delete = models.CASCADE

       > 级联删除模式：当关联表（父表）中的数据删除时，与其相对应的外键（子表）中的数据也删除。
       >
       > class Feedback(models.Model):
       >  user = models.ForeignKey(User, on_delete=models.CASCADE， null=True, blank=Tru)
       >
       > 当删除父表（user）时，此时关联的子表（feedback）中相应关联用户user_id的数据就会被删除。

    3. **on_delete = None：** 删除关联表的数据时，当前表与关联表的filed的行为。

    4. **on_delete = models.DO_NOTHING:** 你删你的，父亲（外键）不想管你

    5. **on_delete = models.PROTECT:** 保护模式，如采用这个方法，在删除关联数据时会抛出ProtectError错误

    6. **on_delete = models.SET_DEFAULT:** 设置默认值，删除子表字段时，外键字段设置为默认值，所以定义外键的时候注意加上一个默认值。

    7. **on_delete = models.SET（值）:** 删除关联数据时，自定义一个值，该值只能是对应指定的实体

- models.**BooleanField**(verbose_name="", help_text="", default=False, blank=True, null=True)

  > 布尔字段

- models.**URLField**(verbose_name="", help_text="", blank=True, null=True)

- models.**ImageField**(upload_to='type', verbose_name='商品图片')

  > 继承于FileField，对上传的内容进行校验，确保是有效的图片（jpg、png）

###### 选项

1. **verbose_name**：用于指定名称
2. **help_text**：
3. **null**：如果为True，表示允许为空，默认值是False。null是数据库范畴的概念。
4. **blank**：如果为True，则该字段允许为空白，默认值是False。blank是后台管理页面表单验证范畴的。
5. **default**：设置默认值。
6. **choices**：choices=status_choices，其中status_choices等于一个元祖。配置字段的choices后，在admin页面上就可以看到对应的选项展示。choice显示中文可以使用 source="get\_字段名_display()"
7. **unique**：如果为True, 这个字段在表中必须有唯一值，默认值是False。
8. **db_index**：若值为True, 则在表中会为此字段创建索引，默认值是False。
9. **db_column**：字段的名称，如果未指定，则使用我们定义的Field对应数据库中的字段名称。

###### 4. 查询操作

- 惰性执行：创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用。
- 缓存：使用同一个查询集，第一次使用时会发生数据库的查询，然后把结果缓存下来，再次使用这个查询集时会使用缓存的数据。

| 函数名                                                       | 功能                                                         | 返回值                                                       | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **get**<br/>UserProfile.objects.get(mobile='15830900798')    | 返回结果只有一条                                             | 返回值是一个模型类对象<UserProfile: zhengzishuo>             | 参数中写查询条件。<br />  如果查到多条数据，则抛异常MultipleObjectsReturned 查询不到数据，则抛异常：DoesNotExist |
| **all**<br/>UserProfile.objects.all()                        | 返回模型类对应表格中的所有数据                               | 返回值是QuerySet类型<QuerySet [<UserProfile: admin>, <UserProfile: zhengzishuo>]> | 查询集                                                       |
| **filter**<br/>UserProfile.objects.filter(mobile='15830900798')<br />可以传多个参数，条件之间代表且的关系。<br />参数名可以使用双下划线__表示外键，如：<br />PowerConsumption.objects.filter(game_competitor_id=id,                                                  device\_\_test_model=test_model)，device关联外键。 | 返回满足条件的所有数据                                       | 返回值是QuerySet类型<QuerySet [<UserProfile: zhengzishuo>]>  | 参数写查询条件<br />查不到返回None                           |
| **exclude**<br />UserProfile.objects.exclude(mobile='15830900798') | 返回不满足条件的所有数据                                     | 返回值是QuerySet类型<QuerySet [<UserProfile: admin>]>        | 参数写查询条件                                               |
| **order_by**<br />UserProfile.objects.exclude(mobile='15830900798').order_by('id') | 对查询结果进行排序                                           | 返回值是QuerySet类型                                         | 参数中写根据哪些字段进行排序id表示升序；-id表示降序。升序时可以不写，是默认。 |
| **values**<br />.UserProfile.objects.filter(mobile='15830900798').values('mobile') | 返回查询对象的值                                             | 返回值是QuerySet类型 <QuerySet [{'mobile': '15830900798'}]>  | 查看具体数值values : queryset类型的列表中是字典values_list : queryset类型的列表中是元组 |
| **first**<br />UserProfile.objects.exclude(mobile='15830900798').first() | 返回queryset中匹配到的第一个对象，如果没有匹配到对象则为None，如果queryset没有定义排序，则按主键自动排序 | 返回值是一个模型类对象<br/><UserProfile: admin>              |                                                              |
| **exists**<br />UserProfile.objects.filter(mobile='15830900798').exists() | 判断查询的数据是否存在，存在时返回True，否则返回False        | 返回值是一个布尔值<br />True                                 |                                                              |
| **aggregate**<br/>UserProfile.objects.all().aggregate(Count('id')) | 对查询结果进行聚合操作                                       | **返回值是一个字典** {'id__count': 5}                        | **使用前需先导入**聚合类**：** from django.db.models import Sum,Count,Max,Min,Avg |
| **count**<br/>UserProfile.objects.all().count()              | 统计满足条件数据的数目                                       | **返回值是一个数字**5                                        |                                                              |
| **distinct**<br />PowerConsumption.objects.filter(game_competitor_id=id,<br/>     	device__test_model=test_model).values_list('picture_level', flat=True).distinct() | 对查询的结果进行去重                                         |                                                              |                                                              |

###### filter模糊查询（模型类属性名__条件名=值）

1. 判断条件名contains, endswith

   ```python
   例：查询书名包含'传'的图书 contains
   BookInfo.objects.filter(btitle__contains='传')
   例：查询书名以'部'结尾的图书 endswith
   BookInfo.objects.filter(btitle__endswith='部')
   ```

2. 排除：exclude

   ```
   例：排除书名为'三国演义'的图书
   BookInfo.objects.exclude(title="三国演义")
   ```

3. 空查询 isnull

   ```python
   例：查询书名不为空的图书。isnull 
   BookInfo.objects.filter(btitle__isnull=False)
   ```

4. 范围查询 in

   ```python
   例：查询id为1或3或5的图书。
   BookInfo.objects.filter(id__in = [1,3,5])
   ```

5. 比较查询

   ```python
   大于gt
   小于lt
   大于等于 gte
   小于等于 lte
   例：查询id大于3的图书。
   BookInfo.objects.filter(id__gt=3)
   ```

6. 日期查询

   ```
   例：查询1980年发表的图书。
   BookInfo.objects.filter(bpub_date__year=1980)
   例：查询1980年1月1日后发表的图书。
   from datetime import date
   BookInfo.objects.filter(bpub_date__gt=date(1980,1,1))
   ```

###### F对象：用于类属性之间的比较

```
from django.db.models import F
例：查询图书阅读量大于评论量图书信息。
BookInfo.objects.filter(bread__gt=F('bcomment'))
例：查询图书阅读量大于2倍评论量图书信息。
BookInfo.objects.filter(bread__gt=F('bcomment')*2)
```

###### Q对象：用于查询时条件之间的逻辑关系

```
not and or，可以对Q对象进行&|~操作
from django.db.models import Q
例：查询id大于3且阅读量大于30的图书的信息。
BookInfo.objects.filter(id__gt=3, bread__gt=30)
BookInfo.objects.filter(Q(id__gt=3)&Q(bread__gt=30))
例：查询id大于3或者阅读量大于30的图书的信息。
BookInfo.objects.filter(Q(id__gt=3)|Q(bread__gt=30))
例：查询id不等于3图书的信息。
BookInfo.objects.filter(~Q(id=3))
```

###### 聚合操作：annotate、aggregate

>  aggregate聚合操作的返回值是字典
>
>  annotate进行聚合的原理是将QuerySet内的每个对象都进行注解，注解的信息直接存储为对象的一个新字段，因此其查询的返回值仍然是QuerySet。

```python
from django.db.models import Sum,Count,Max,Min,Avg

id = request.GET['id']
basic_performance = PowerConsumption.objects.filter(game_competitor_id=id)
queryset = basic_performance.values('device__test_model').annotate(
    max_power_consumption=Max('power_consumption'),
    min_power_consumption=Min('power_consumption')
)
# 获取不重复的 picture_level 值
for data in queryset:
    test_model = data['device__test_model']
    picture_levels = PowerConsumption.objects.filter(game_competitor_id=id,
     	device__test_model=test_model).values_list('picture_level', flat=True).distinct()
    data['picture_levels'] = list(picture_levels)
```

- Annotate方法与Filter方法联用

  ```
  # 先按爱好分组，再统计每组学生数量, 然后筛选出学生数量大于1的爱好。
  Hobby.objects.annotate(student_num=Count('student')).filter(student_num__gt=1)
  ```

- Annotate与order_by()联用

  ```
  # 先按爱好分组，再统计每组学生数量, 然后按每组学生数量大小对爱好排序。
  Hobby.objects.annotate(student_num=Count('student')).order_by('student_num')
  # 统计最受学生欢迎的5个爱好。
  Hobby.objects.annotate(student_num=Count('student')).order_by('-student_num')[:5]
  ```

- Annotate与values()联用

  ```
  # 按学生名字分组，统计每个学生的爱好数量。
  Student.objects.values('name').annotate(Count('hobbies'))
  # 按学生名字分组，统计每个学生的爱好数量。
  Student.objects.annotate(hobby_count=Count('hobbies')).values('name', 'hobby_count')
  ```

###### 5. 增加操作

1. **方法一，调用模块函数对象**

   ```python
   b = models.UserProfile()
   b.username = 'xiaoming'
   b.mobile = '15830900798'
   b.save()
   ```

2. **方法二，直接加**

   ```python
   models.UserProfile.objects.create(username='xiaohong',mobile=15830900797)
   ```

3. **批量增加**

   ```python
   object_list = [
       models.UserInfo(name='Alex',age=18),
       models.UserInfo(name='sss',age=20),
   ]
   
   models.UserInfo.objects.bulk_create(object_list,10) # 每次10个批量添加
   ```

###### 6. 删除操作

```python
models.Tb1.objects.filter(name='seven').delete() # 删除指定条件的数据
```

###### 7. 更新/修改操作

1. **方法一，直接加**

   ```python
   models.Tb1.objects.filter(name='seven').update(gender='0')  # 将指定条件的数据更新，均支持 **kwargs
   ```

2. **方法二，调用模块函数对象**

   ```python
   obj = models.Tb1.objects.filter(id=1).first()
   obj.c1 = '111'
   obj.save()  # 修改单条数据
   ```

3. update_or_create()方法的机制：如果数据库内没有该数据，那么新增，如果有，则更新，这就大大减少了我们的代码量，不用写两个方法。

   ```python
   def add_to_new_assets_zone(self):
       defaults = {
           'data': json.dumps(self.data),
           'username': self.data.get('username'),
           'password': self.data.get('password'),
       }
   models.UserProfile.objects.update_or_create(username='xiaohong', defaults=defaults)
   ```

4. 批量更新：bulk_update()

   ```python
   update_data = []
   for i in range(5)
       obj = models.Tb1.objects.filter(id=i).first()
       obj.c1 = '111'
       update_data.append(obj)
       
   models.objects.bulk_update(update_data, ['field1', 'field2', 'field3'])
   ```

###### 8. 模型关系

1. 一对多关系(ForeignKey)

   > models.ForeignKey(to=UserProfile, on_delete=models.CASCADE) ：将字段定义在多的一端。
   >
   > 应用场景：当一张表中创建一行数据时，有一个单选的下拉框（可以被重复选择）

2. 多对多关系(ManyToManyField)

   > models.ManyToManyField(to='UserInfo') ：将字段定义在任意一端。
   >
   > 应用场景：在某表中创建一行数据是，有一个可以多选的下拉框

3. 一对一关系(OneToOneField)

   > models.OneToOneField(to='UserInfo',on_delete=models.CASCADE)： 将字段定义在任意一端。
   >
   > 应用场景：在某表中创建一行数据时，有一个单选的下拉框（下拉框中的内容被用过一次就消失了）

###### 一对多关联查询

- 由一类（UserProfile）查询多类（Article）

  1. 方法一：一类的对象.多类名小写_set.all()

     ```python
     b = models.UserProfile.objects.get(username='admin')
     b.article_set.all()
     <QuerySet [<Article: 啊1>, <Article: 啦啦啦我是2>, <Article: 啦啦啦我是3>]>
     ```

  2. 方法二：多类名.objects.filter(关联属性\__一类属性名__条件名)

     ```
     models.Article.objects.filter(user__username='admin')
     <QuerySet [<Article: 啊1>, <Article: 啦啦啦我是2>, <Article: 啦啦啦我是3>]>
     ```

- 由多类（Article）查询一类（UserProfile）

  1. 方法一：多类的对象.主键

     ```
     h = models.Article.objects.get(title='啦啦啦我是3')
     h.user
     <UserProfile: admin>
     ```

  2. 方法二：一类名.objects.filter(多类名小写\__多类属性名__条件名)

     ```
     models.UserProfile.objects.filter(article__title='啦啦啦我是3')
     <QuerySet [<UserProfile: admin>]>
     ```

###### 多对多关系操作

- model代码：

  ```python
  class Author(models.Model):    
      first_name = models.CharField(max_length=30)    
      last_name = models.CharField(max_length=40)    
      email = models.EmailField()    
          
  class Book(models.Model):    
      title = models.CharField(max_length=200)    
      authors = models.ManyToManyField(Author) 
  ```

- 获取对象方法：

  - 从书籍出发获取作者

    ```python
    b = Book.objects.get(id=50)  
    b.authors.all()  
    b.authors.filter(first_name='Adam')  
    ```

  - 从作者出发获取书籍

    ```python
    a = Author.objects.get(id=1)  
    a.book_set.all()  
    ```

- 添加对象方法：

  ```python
  a = Author.objects.get(id=1)  
  b = Book.objects.get(id=50)  
  b.authors.add(a) 
  ```

- 删除对象对象方法：

  ```python
  a = Author.objects.get(id=1)  
  b = Book.objects.get(id=50)  
  b.authors.remove(a) 或者 b.authors.filter(id=1).delete()  
  ```

###### 自关联 - 自关联是一种特殊的一对多（把关联属性指向了自己）

应用场景：

```python
# 模型类
class xxx(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        db_table = "xxx"
        verbose_name = "xxx"
        verbose_name_plural = xxx

# 序列化器中添加自定义方法get_children
class xxxSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = EcologicalStandard
        fields = "__all__"
        depth = 1

    def get_children(self, obj):
        children = obj.children.all()
        serializer = xxxSerializer(children, many=True)
        return serializer.data
```

#### 视图

###### 1. 序列化器类

```python
from rest_framework import serializers

from bk_power.ecology.models import xxxx

# 基于Model自动生成字段 serializers.ModelSerializer
class xxxxSerializer(serializers.ModelSerializer):
    # required=True 表示该字段在添加或更新数据时不能为空；required=False表示数据可以为空，默认为True
    name = serializers.CharField(required=True, max_length=32)
    # 定义时间类型的输出格式
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # 定义日期类型的输出格式
    created_at = serializers.DateField(format='%Y-%m-%d')
    # 定义时间类型的输入格式
    created_at = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d'])
    
    # 字段级别的验证
    # validate_字段名， 对<field_name>字段进行验证，反序列化阶段使用
    from rest_framework.exceptions import ValidationError
    from rest_framework.exceptions import APIException
    def validate_title(self, value):
        if 'django' not in value.lower():
            # raise serializers.ValidationError("图书不是关于Django的")
            raise serializers.APIException("图书不是关于Django的")
        return value
    
    # 对象级别的验证
    # 要执行需要访问多个字段的任何其他验证，请添加一个.validate()方法到你的Serializer子类中。
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start'] > data['finish']:
            #raise serializers.ValidationError("finish must occur after start")
            raise serializers.APIException("finish must occur after start")
        return data
    
    # 数据库中相同时间里不能有重复的title
    def validate(self, data):
        # 排除当前id，编辑时也会提示内容重复
        instance_id = self.instance.id if self.instance else None
        if EcologicalDynamic.objects.filter(update_date=data['update_date'], title=data['title']).exclude(id=instance_id).exists():
            raise APIException("当前内容本月已存在，请勿重复提交")
            # raise serializers.ValidationError("当前内容本月已存在，请勿重复提交")
        return data
    
    # ForeignKey：基于source参数链表操作
    # 可以查看主键的外键所在表中的任意值，但是需要写多行，如果全返回用下面的深度连表
    administrator = serializers.CharField(source='administrator.username')
    # choice显示中文可以使用source字段 "get_字段名_display"
    
    # 基于SerializerMethodField+自定义一个钩子方法
    # 自定义方法可以跨表获取数据内容
    admin_username = serializers.SerializerMethodField()
    '''
    下面是自定义序列化字段（序列化阶段使用），序列化的属性值由方法来提供，
       方法的名字：固定为 get_属性名，
       方法的参数：self为序列化对象，obj为当前序列化的model的TicketRecord对象,名字随便写
       注意 : 建议自定义序列化字段名不要与model已有的属性名重名,否则会覆盖model已有字段的声明
       注意 : 自定义序列化字段要用SerializerMethodField()作为字段类型
    '''
    def get_admin_username(self, obj):
        ticket_id = obj.ticket_id
        tag_list = WorkflowAdmin.objects.filter(workflow__ticketrecord__ticket_id=ticket_id)
        for i in tag_list:
            admin_username = i.username
            return admin_username
        
    # to_internal_value方法，反序列化过程中，在校验name = serializers.CharField(required=True, max_length=32)之前，先对字段进行自定义处理数据
    def to_internal_value(self, data):
    if not data['fps']:
        data['fps'] = None
    if not data['peak']:
        data['peak'] = None
    if not data['cpu']:
        data['cpu'] = None
    if not data['gpu']:
        data['gpu'] = None
    if not data['device_id']:
        data['device_id'] = None
    if not data['test_case_id']:
        data['test_case_id'] = None
    if not data['game_competitor_id']:
        data['game_competitor_id'] = None
    return super().to_internal_value(data)
    
    class Meta:
        model = xxxx
        # fields = "__all__" 方法一：生成所有数据库字段
        fields = ['id', 'name'] # 方法二：自定义字段名
        # 深度自动化连表
        depth = 1  # 0 ~ 10
```

- CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)

- 有ForeignKey外键关联的字段

  ```python
  from rest_framework import serializers
  
  class XXXSerializer(serializers.ModelSerializer):
      device_id = serializers.CharField(required=False)
      
      class Meta:
      model = xxx
      fields = "__all__"
      depth = 1
      
  # 用户就可以在get请求时获取到device关联的详细信息，也能在发送post/put请求时，给device_id传递id值对数据进行更改。
  ```

- ManyToManyField多对多关联字段

  > 添加数据：以列表形式传值
  >
  > "game_type": [1,2,3]  更新后的游戏类型 ID 列表

  ```python
  game_type = models.ManyToManyField(GameType, blank=True)
  
  class XXXSerializer(serializers.ModelSerializer):
      # 存在的问题是序列化返回的数据也是列表存储的id值，而不是其关联对象的详细信息
      game_type = serializers.PrimaryKeyRelatedField(required=False, queryset=GameType.objects.all(), many=True)
  
      class Meta:
          model = XXX
          fields = "__all__"
  ```


###### 2. 分页类

```python
from rest_framework.pagination import PageNumberPagination

RETURN_ALL = "-1"


class Pagination(PageNumberPagination):
    """分页"""

    page_size = 10 # 单页条目
    page_size_query_param = "page_size" # URL配置参数名

    def get_page_size(self, request):
        if request.query_params.get(self.page_size_query_param) == RETURN_ALL:
            return None
        return super(Pagination, self).get_page_size(request)
    
# 视图中的使用
class ServerViewSet(viewsets.ModelViewSet):
    pagination_class = Pagination
    pagination_class.page_size = 2 # 自定义单页条目
```

- 常规分页

  ```python
  # 页码小于1时显示第一页
  if page < 1 or page_size > len(mylist):
      page = 1
  # 页码大于最大页码时，显示最后一页
  elif page > len(mylist) // page_size and len(mylist) // page_size == 0:
      page = len(mylist) // page_size
  # 页码大于最大页码时，显示最后一页
  elif page > len(mylist) // page_size and len(mylist) // page_size != 0:
      page = len(mylist) // page_size + 1
  ret_1 = mylist[(page - 1) * page_size:page * page_size]
  ```

  

###### 3. 过滤器类

- 安装django-filter模块：pip install django-filter

- 在配置文件settings.py中INSTALLED_APPS 添加应用django_filters

- 添加配置

  ```python
  # 在全局配置
  REST_FRAMEWORK = {
      ...
      'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
  }
  
  # 在视图类中导入
  import django_filters
  from rest_framework import serializers, viewsets
  from django_filters.rest_framework import DjangoFilterBackend
  
  class xxxSerializer(serializers.ModelSerializer):
      pass
  	class Meta:
          model = xxx
          fields = "__all__"
  
  class xxxFilter(django_filters.FilterSet):
      # 自定义某个字段匹配的规则
      created = django_filters.CharFilter(lookup_expr="icontains")
  	class Meta:
          model = xxx
          # 注意，如果某个字段的属性是JSONField，如：game_config_detail = models.JSONField(verbose_name="档位配置详情", help_text="档位配置详情", default=dict)，fields就不能是"__all__"，必须将该字段排除在外。
          fields = "__all__"
  
  class xxxViewSet(viewsets.ModelViewSet):
      filter_backends = [DjangoFilterBackend] # 在全局配置了就不需要添加
      filterset_class = xxxFilter
  ```

- lookup_expr：过滤器的查询表达式

  1. 精确匹配

     - `exact`: 精确匹配

     - `iexact`: 不区分大小写的精确匹配

  2. 模糊匹配

     - `contains`: 包含

     - `icontains`: 不区分大小写的包含
     - `startswith`: 以指定字符串开头
     - `endswith`: 以指定字符串结尾

  3. 数值比较

     - `gt`: 大于

     - `gte`: 大于等于

     - `lt`: 小于

     - `lte`: 小于等于

  4. 列表匹配

     - `in`: 在列表中
     - `icontains`: 不区分大小写的包含

  5. 空值匹配

     - `isnull`: 是否为空值

  6. 正则表达式匹配

     - `regex`: 匹配正则表达式

- 根据多个字段联合过滤（and的关系）

  > 可以联合field=v1,v2,v3使用，也可以field=v1, field=v2,field=v3 ???

  ```python
  # 自定义过滤器类
  # GET /your-models/?field1=value1&field2=value2
  class xxxlFilter(django_filters.FilterSet):
      # 定义多个字段进行过滤
      field1 = django_filters.CharFilter(lookup_expr='icontains')  # 例如，这里使用 icontains 进行模糊查询
      field2 = django_filters.NumberFilter()
  
      class Meta:
          model = YourModel
          fields = ['field1', 'field2', ...]  # 需要进行过滤的字段
  
  from django_filters.rest_framework import DjangoFilterBackend
  class xxxAPIView(generics.ListAPIView):
      queryset = YourModel.objects.all()
      serializer_class = YourModelSerializer
      filter_backends = [DjangoFilterBackend]
      filterset_class = YourModelFilter  # 使用自定义的过滤器类
      ordering_fields = '__all__'
  ```

- 根据多个字段联合过滤（or的关系）

  > 重写filter_queryset方法

  ```python
  def filter_queryset(self, request, queryset, view):
          name_prefix = request.query_params.get('name_prefix')
          min_age = request.query_params.get('min_age')
          max_age = request.query_params.get('max_age')
  
          q_objects = Q()
  
          if name_prefix:
              q_objects |= Q(name__startswith=name_prefix)
          if min_age:
              q_objects |= Q(age__gte=min_age)
          if max_age:
              q_objects |= Q(age__lte=max_age)
  
          queryset = queryset.filter(q_objects)
          return queryset
  ```

- 根据关键字keyword对全表进行过滤

  ```python
  from rest_framework.filters import SearchFilter
  
  class CustomSearchFilter(SearchFilter):
      search_param = "keyword"
  
  class GameViewSet(viewsets.ModelViewSet):
      queryset = Game.objects.all()
      serializer_class = GameSerializer
      
      # 根据keyword过滤搜索
      filter_backends = [CustomSearchFilter]
      search_fields = [i.name for i in GameTestCase._meta.fields]
  ```

  ```python
  from functools import reduce
  from operator import or_
  import django_filters
  from django.db.models import Q
  from mainapp.models import Issues
  
  class IssuesFilter(django_filters.FilterSet):
      keyword = django_filters.CharFilter(method="get_keyword")
  
      def key_word(self, keyword, lookup_expr="icontains"):
          # 获取模型的所有字段名
          field_names = ["description", "id", "follower"]
          # 创建Q对象列表，用于存储每个字段的模糊查询条件
          q_list = [Q(**{f'{field}__{lookup_expr}': keyword}) for field in field_names]
          # 使用reduce和or_将所有Q对象合并为一个大的Q对象，表示任意一个字段包含关键词即可
          combined_q = reduce(or_, q_list)
          return combined_q
  
      def get_keyword(self, queryset, name, value):
          # 从url获取参数列表
          keyword = self.request.query_params.get('keyword')
          return queryset.filter(self.key_word(keyword))
  ```

  

- 根据某个字段联合过滤（or的关系）

  > http://xxx:xx/xxx/?name=name1&name=name2&name=name3

  ```python
  import django_filters
  from django.db.models import Q
  
  class xxxFilter(django_filters.FilterSet):
      name = django_filters.CharFilter(method="get_name")
  
      def build_or_condition_query(self, field, values, lookup_expr="icontains"):
          """构造 "or" 查询条件，根据一个字段来筛选不同的值"""
          query = Q()
          query.connector = Q.OR # or关系
          [query.children.append((f"{field}__{lookup_expr}", value)) for value in values]
          return query
      
      def keyword(self, keyword, lookup_expr="icontains"):
          """根据表中不同字段筛选相同的值keyword"""
          # 获取模型的所有字段名
          field_names = [f.name for f in XXX._meta.get_fields() if not any([bool(f.name == "id"), bool(f.name == "file_name")])]
          # 创建Q对象列表，用于存储每个字段的模糊查询条件
          q_list = [Q(**{f'{field}__icontains': keyword}) for field in field_names]
          # 使用reduce和or_将所有Q对象合并为一个大的Q对象，表示任意一个字段包含关键词即可
          combined_q = reduce(or_, q_list)
          return combined_q
  
      def get_name(self, queryset, name, value):
          # 从url获取参数列表
          values = self.request.query_params.getlist('name')
          # 过滤条件为A and B，其中A和B里面都为or关系
          # 此处的QuerySet对象的filter()方法，可以构造各种方式的查询条件。
          return queryset.filter(self.build_or_condition_query(name, values) & self.keyword(keyword))
      
  class xxxViewSet(viewsets.ModelViewSet):
      queryset = xxx.objects.all()
      serializer_class = xxxSerializer
      filterset_class = xxxFilter
  ```

- 根据某个字段联合过滤（and的关系）

  > 和or的关系类似，区别在于：query.connector = Q.AND  # and关系

- 多对多查询

  ```python
  # 模型类
  class GameType(models.Model):
  	game_type = models.CharField(verbose_name="游戏类型", help_text="游戏类型", max_length=128, blank=True, null=True)
  
  class Game(models.Model):
  	game_name = models.CharField(verbose_name="游戏名称", help_text="游戏名称", max_length=128, blank=True, null=True)
  	type = models.ManyToManyField(GameType, blank=True)
  	
  # 序列化器，使用PrimaryKeyRelatedField
  class GameTestSerializer(serializers.ModelSerializer):
      type = serializers.PrimaryKeyRelatedField(queryset=GameType.objects.all(), many=True)
  
      class Meta:
          model = GameCompetitor
          fields = "__all__"
          
  # 过滤器
  import django_filters
  class GameFilter(django_filters.FilterSet):
      type = django_filters.ModelMultipleChoiceFilter(
          queryset=GameType.objects.all(), 
          field_name='game_type', # ？
          to_field_name='id' # 置顶根据哪个字段进行过滤？
      )
  
      class Meta:
          model = Game
          fields = ["type"]
          
  # 查询
  GET /games/?type=1&type=2&type=3
  # 添加数据
  "game_type": [1,2,3] # 更新后的游戏类型 ID 列表
  
  # 在 Django 中，多对多关联的字段在数据库查询返回的数据类型是一个 ManyRelatedManager 对象。要返回该字段和其他表关联的所有 ID 值：
  # 假设 game 是从数据库中查询得到的 Game 对象
  game = Game.objects.get(pk=1)
  # 获取与该游戏关联的所有类型的 ID 值列表
  type_ids = list(game.type.values_list('id', flat=True))
  ```

  

- 在一个字段中查询多个（如根据多个游戏类型进行查找，通过 URL 参数来传递多种游戏类型的值，用逗号分隔，指定lookup_expr为in）

  ```python
  import django_filters
  from .models import Game
  
  class GameFilter(django_filters.FilterSet):
      # 在GameFilter过滤器类中，定义一个CharFilter类型的字段，并指定lookup_expr为in
      game_type = django_filters.CharFilter(field_name='game_type', lookup_expr='in')
      
      # 添加外键表中字段到过滤器中，可进行模糊查询
      plan_name = filters.CharFilter(field_name='plan__title', lookup_expr='icontains')
      # exact精确匹配，添加choices过滤
      topic_type = filters.ChoiceFilter(field_name='topic_type', lookup_expr='exact', choices=models.Topic.TYPE)
      update_date = django_filters.CharFilter(method="get_update_date")
      
      
      # 自定义过滤字段
      def get_update_date(self, queryset, name, value):
      """按更新日期过滤"""
          try:
              year, month = value.split("-")
          except Exception:
              raise ValidationError("查询参数不是YY-MM格式")
          query = dict(update_date__year=year, update_date__month=month)
          return EcologicalDynamic.objects.filter(**query)
  
      class Meta:
          model = Game
          fields = ['game_type']
          
  from rest_framework import viewsets
  from .models import Game
  from .serializers import GameSerializer
  from .filters import GameFilter
  
  class GameViewSet(viewsets.ModelViewSet):
      queryset = Game.objects.all()
      serializer_class = GameSerializer
      filterset_class = GameFilter
      
  # 通过 URL 参数来传递多种游戏类型的值，用逗号分隔，例如：?game_type_in=RPG,Strategy,Action。
  
  # 自定义过滤方法
      def filter_queryset(self, queryset):
          game_types = self.request.query_params.get('game_type')
          if game_types:
              game_type_list = game_types.split(',')  # 将传递的字符串拆分成列表
              # 使用 ORM 的__contains查询，查找包含任一值的数据
              # for val in game_type_list:
              #     queryset = queryset.filter(game_type__contains=val)
              #     if queryset:
              #         return queryset
              queryset = queryset.filter(game_type__in=game_type_list)  # 使用__in操作符进行过滤
              return queryset
          return queryset
  ```


###### 4. 排序 ??

1. 在ordering字段指定了默认排序方式（按照创建时间逆序排序）：

   ```python
   ordering = ["-created_time"]
   ```

2. 也可以使用如下方式指定：

   ```python
   queryset = Server.objects.all().order_by('-created_time')
   
   # 根据多个字段排序，自定义某个字段排序规则
   queryset = self.filter_queryset(xxx.objects.all().order_by("module", "pipeline", Case(
               When(complexity__startswith='简', then=1),
               When(complexity__startswith='中', then=2),
               When(complexity__startswith='复', then=3),
               default=4,
           )))
   
   # 聚合、跨表查询字段信息
   queryset = (
               xxx.objects.filter(game_competitor_id=id)
               .values('device__asset_number', 'device__test_model')
               .annotate(
                   max_fps=Max('fps'),
                   min_fps=Min('fps'),
                   max_peak=Max('peak'),
                   min_peak=Min('peak'),
                   max_cpu=Max('cpu'),
                   min_cpu=Min('cpu'),
                   max_gpu=Max('gpu'),
                   min_gpu=Min('gpu'),
               )
           ).order_by("device__test_model")
   ```

3. 如果要自定义排序字段，需要指定**ordering**字段的内容：

   ```python
   ordering_fields = ["cpus", "ram", "disk", "product_date"]
   ```

4. 在模型类的Meta类中定义

   ```python
       class Meta:
           unique_together = ("title", "update_date")
           db_table = "ecological_dynamic"
           ordering = ["id"]
           verbose_name = "行业前沿动态"
           verbose_name_plural = verbose_name
   ```

###### 5. 权限类

1. 权限校验：CheckPermission
2. IsAuthenticated

```python
from rest_framework.permissions import BasePermission

class CheckPermission(BasePermission):
    """权限校验"""
	
    # 从视图类的属性中获取：resource_key = "sys/ecological_dynamic"
    def get_resource_key(self, view):
        try:
            return getattr(view, "resource_key")
        except AttributeError:
            raise AttributeError("引用了资源权限校验，但view层并未设置resource_key值")

    def pre_check(self, request, view, obj=None):
        # 用户登录校验
        if not bool(request.user and request.user.is_authenticated):
            return False

        if view.action is None:
            return True
        user = request.user.id

        resource_key = self.get_resource_key(view)
        # 权限豁免
        if view.action in getattr(view, "permission_exempt", []):
            return True

        # 可以定义其它action 映射
        action = ACTION_MAP.get(getattr(view, f"{view.action}_action", view.action))

        result = check_permission(user, action, resource_key, view, obj)
        if result:
            return True
        raise PermissionDenied("无操作权限，请向管理员申请")

    def has_permission(self, request, view: ViewSet) -> bool:

        return self.pre_check(request, view)

    def has_object_permission(self, request, view, obj) -> bool:

        return self.pre_check(request, view, obj)
```

###### 6. 视图集

1. BackendSetMixin父类

   ```python
   # bk_power\ecology\viewsets\filter\base.py
   
   import django_filters
   from django.db.models import Q
   from django_filters.rest_framework import DjangoFilterBackend
   from rest_framework.filters import OrderingFilter, SearchFilter
   
   
   class BkPowerFilter(django_filters.FilterSet):
       def build_or_condition_query(self, field, values, lookup_expr="icontains"):
           """构造 "or" 查询条件"""
           query = Q()
           query.connector = Q.OR
           [query.children.append((f"{field}__{lookup_expr}", value)) for value in values.split(",")]
           return query
   
   
   class CustomSearchFilter(SearchFilter):
       search_param = "keyword"
   
   
   class BaseBackendSetMixin:
       filter_backends = [DjangoFilterBackend, OrderingFilter, CustomSearchFilter]
       ordering_fields = NotImplemented
   ```

2. BackendSetMixin类

   ```python
   class BackendSetMixin(BaseBackendSetMixin):
       ordering_fields = ["update_date", "created_at"]
       search_fields = ["title", "desc", "scheme"]
   ```

3. PerformCreateWithUserMixin类

   ```python
   class PerformCreateWithUserMixin:
       """创建时添加用户信息"""
   
       def perform_create(self, serializer):
           user = self.request.user.username
           serializer.save(created_by=user, updated_by=user)
   ```

4. PerformUpdateWithUserMixin类

   ```python
   class PerformUpdateWithUserMixin:
       """更新用户"""
   
       def perform_update(self, serializer):
           user = self.request.user.username
           serializer.save(updated_by=user)
   ```

5. ModelViewSet类

   ```python
   class ModelViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
       """
       A viewset that provides default `create()`, `retrieve()`, `update()`,
       `partial_update()`, `destroy()` and `list()` actions.
       """
       pass
   
   
   ```

6. ModelViewSet父类（剖析增删改查查的每一步代码）

   ```python
   """
   新增数据或更新数据，都需要进行反序列化数据，都需要先调用is_valid()方法，然后再尝试去访问经过验证的数据或保存对象实例。如果发生任何验证错误，.errors属性将包含表示生成的错误消息的字典。
   """
   
   from rest_framework import status
   from rest_framework.response import Response
   from rest_framework.settings import api_settings
   
   # 新增数据类
   class CreateModelMixin:
       """
       Create a model instance.
       """
       def create(self, request, *args, **kwargs):
           serializer = self.get_serializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           self.perform_create(serializer)
           headers = self.get_success_headers(serializer.data)
           return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
   
       def perform_create(self, serializer):
           serializer.save()
   
       def get_success_headers(self, data):
           try:
               return {'Location': str(data[api_settings.URL_FIELD_NAME])}
           except (TypeError, KeyError):
               return {}
   
   # 查询类
   class ListModelMixin:
       """
       List a queryset.
       """
       def list(self, request, *args, **kwargs):
           queryset = self.filter_queryset(self.get_queryset())
   
           page = self.paginate_queryset(queryset)
           if page is not None:
               serializer = self.get_serializer(page, many=True)
               return self.get_paginated_response(serializer.data)
   
           serializer = self.get_serializer(queryset, many=True)
           return Response(serializer.data)
           
   # 查询单例类
   class RetrieveModelMixin:
       """
       Retrieve a model instance.
       """
       def retrieve(self, request, *args, **kwargs):
           instance = self.get_object()
           serializer = self.get_serializer(instance)
           return Response(serializer.data)
   
   # 更新数据类（单例更新）
   class UpdateModelMixin:
       """
       Update a model instance.
       """
       def update(self, request, *args, **kwargs):
           partial = kwargs.pop('partial', False)
           instance = self.get_object()
           serializer = self.get_serializer(instance, data=request.data, partial=partial)
           serializer.is_valid(raise_exception=True)
           self.perform_update(serializer)
   
           if getattr(instance, '_prefetched_objects_cache', None):
               # If 'prefetch_related' has been applied to a queryset, we need to
               # forcibly invalidate the prefetch cache on the instance.
               instance._prefetched_objects_cache = {}
   
           return Response(serializer.data)
   
       def perform_update(self, serializer):
           serializer.save()
   
       def partial_update(self, request, *args, **kwargs):
           kwargs['partial'] = True
           return self.update(request, *args, **kwargs)
   
   # 删除数据类（删除单例）
   class DestroyModelMixin:
       """
       Destroy a model instance.
       """
       def destroy(self, request, *args, **kwargs):
           instance = self.get_object()
           self.perform_destroy(instance)
           return Response(status=status.HTTP_204_NO_CONTENT)
   
       def perform_destroy(self, instance):
           instance.delete()
   ```

7. 主视图

   ```python
   from bk_power.ecology.viewsets.develop_progress.topics import BackendSetMixin
   from bk_power.common import viewset as common_view
   from bk_power.common.paginations import Pagination # 分页类
   from rest_framework import viewsets
   from bk_power.ecology.models import xxxx # 数据库模型类
   from bk_power.ecology.serializers import xxxxSerializer # 序列化器类
   from permission.permissions import CheckPermission # 权限类
   import django_filters
   
   class KnowledgeFilter(django_filters.FilterSet):
       platform = django_filters.CharFilter(field_name="platform", lookup_expr="icontains/in")
   
       class Meta:
           model = BasicPerformance
           fields = ["platform"]
   
   class xxxxViewSet(
       BackendSetMixin, # 配置默认search_fields、ordering_fields
       common_view.PerformCreateWithUserMixin, # 创建时添加用户信息
       common_view.PerformUpdateWithUserMixin, # 更新时更新用户
       viewsets.ModelViewSet,
   ):
       # queryset = xxxx.objects.all().order_by("-id") # 数据库查询集
       queryset = xxxx.objects.all() # 数据库查询集
       serializer_class = xxxxSerializer # 序列化器类
       
       pagination_class = Pagination # 分页类
       pagination_class.page_size = 5 # 自定义单页条目
       
       # filterset_class = KnowledgeFilter 自定义过滤类
       # exact表示完全匹配，in表示什么呢？
       filterset_fields = {
           'title': ["exact", "in"],
           "type": ["exact", "in"],
       } ？
       
       # 设置搜索的关键字
       search_fields = ('username', 'password') ？
       schema_tags = ["动态后台管理-项目进展"] ？
       resource_key = "sys/develop_progress" ？
       
       # 排序，默认升序，-是降序
       # ordering_fields = ["-is_top", "-updated_at"]
       ordering = ["-id"] ？
       
       # 权限配置
       permission_classes = [CheckPermission, IsAdminUser]?有几种类型的权限设置，分别如何设置？
       # bk_power\ecology\permissions\sys.py中添加：
       # ECOLOGICAL_DYNAMIC = EnumField("ecological_dynamic", "行业前沿动态")
       resource_key = "sys/ecological_dynamic" # 需要有配置了管理权限的用户才能进行配置
       
       from rest_framework.decorators import action #导入路由装饰器
       # permission_classes给该方法配置权限
       # 
       @action(detail=True/False, methods=["post"], permission_classes=[IsAdminUser])
       def xxxx(self, request):
           pass
       
       @inject_serializer(out=KnowledgeSerializer) # 这个装饰器的作用是什么？
       def list(self, request, *args, **kwargs): # 重写父类的查询方法
           # from rest_framework.response import Response 导入drf相应类
           # from rest_framework import status 导入状态码
           return Response(data=None, status=status.xxx)
   ```

#### 其他功能

###### 1. 图片上传

> 上传相关API：api/v1/upload
>
> ecology\viewsets\common_views.py 用来存放所有通用接口

- 本地测试url

  ```python
  import re, os, logging
  
  from rest_framework import status
  from rest_framework.exceptions import ValidationError
  from rest_framework.response import Response
  from django.conf import settings
  
  logger = logging.getLogger(__name__)
  
  
  def re_photo(photo_obj):
      """校验图片"""
      PHOTO_SIZE = 2 * 1024 * 1024
      # 校验格式
      photo_name = photo_obj.name
      # re.compile ??
      r_image = re.compile(r".*\.(jpg|png|jpeg)$")  # 正则匹配图片格式
      if not re.match(r_image, photo_name):
          raise ValidationError("请上传格式为jpg,jpeg,png图片")
      # 校验大小
      size = photo_obj.size // 1024
      if size > PHOTO_SIZE:
          raise ValidationError("请上传小于{}KB的图片".format(PHOTO_SIZE))
      return True
  
  
  def upload_photo_local(self, request):
      """本地测试 跳过cos上传图片"""
      photo_obj = request.data.get("file")
      re_photo(photo_obj)
      try:
          current_path = settings.STATIC_URL
          # 创建文件上传目录 upload
          upload_path = os.path.join(current_path, 'upload')
          if not os.path.exists(upload_path):
              os.makedirs(upload_path)
          file_path = os.path.join(upload_path, photo_obj.name)
          if not os.path.exists(file_path):
              with open(file_path, 'wb') as f:
                  for chunk in photo_obj.chunks():
                      f.write(chunk)
      except Exception as e:
          logger.exception("上传图片失败, 请求体: %s， 结果: %s", request.data, str(e))
          return Response("上传图片失败", status=status.HTTP_400_BAD_REQUEST)
      data = {"name": photo_obj.name, "url": file_path, "size": photo_obj.size / 1024 / 1024}
      return Response(data)
  ```

- 上传腾讯云

  ```
  post请求，参数名file
  http://127.0.0.1:8000/api/v1/upload/upload_photo/
  文件类型：jpg|png|jpeg
  ```

- 批量上传文件

  ```python
  post请求，参数名files
  http://127.0.0.1:8000/api/v1/upload/upload_files/
  文件校验：(pdf|ppt|pptx|doc|docx|xls|xlsx|zip|7z|rar|mp4|mov|png|jpg|jpeg)
  ```

###### 2. 模板的导入导出功能

1. 数据校验和导入

   ```python
   @action(methods=["post"], detail=False)
   def check_data(self, request, *args, **kwargs):
       if 'file' not in request.FILES:
           return Response({'error': 'No file received'}, status=400)
       file = request.FILES['file']
       data_frame = pd.read_excel(file, keep_default_na=False) # 将NaN的值清除
       records = data_frame.to_dict('records')
       # 校验数据
       errors = []
       datas = []
       for i, record in enumerate(records, 1):
           flag = 0
           if record["复杂度"] not in ["简单", "中等", "复杂"]:
               flag += 1
               errors.append(f'第{i}条数据校验未通过，复杂度必须是简单、中等、复杂中的一个')
           if not isinstance(record["最小"], int):
               flag += 1
               errors.append(f'第{i}条数据校验未通过，最小值必须是数字')
           if not isinstance(record["最大"], int):
               flag += 1
               errors.append(f'第{i}条数据校验未通过，最大值必须是数字')
           record = {
               "module": record["模块"],
               "pipeline": record["管线"],
               "complexity": record["复杂度"],
               "process": record["工序"],
               "min": record["最小"],
               "max": record["最大"],
               "count": record["合计"],
           }
           if flag == 0:
               datas.append(record)
       return Response(
           {"pass_num": len(datas), "error_num": len(records) - len(datas), "pass_data": datas, "error_data": errors})
   
   @action(detail=False, methods=["post"], permission_classes=[CheckPermission])
   def import_data(self, request, *args, **kwargs):
       try:
           d_list = request.data.get("pass_data")
           datas = []
           # 更新数据
           for i in d_list:
               obj = EcologicalStandard.objects.filter(module=i["module"],
                                                       pipeline=i["pipeline"],
                                                       complexity=i["complexity"],
                                                       process=i["process"]).first()
               if obj:
                   obj.min = i["min"]
                   obj.max = i["max"]
                   obj.count = i["count"]
                   obj.save()
               else:
                   datas.append(i)
           # 重复去重
           new_dict = {}
           for d in datas:
               key = (d['module'], d['pipeline'], d['complexity'], d['process'])
               new_dict[key] = d
           result = list(new_dict.values())
           # 导入数据
           self.my_model.objects.bulk_create([self.my_model(**record) for record in result])
           return Response({'code': 200, 'msg': 'Data imported successfully'})
       except Exception as e:
           return Response({"code": 400, "msg": e})
   ```

2. 数据导出

   ```python
   
   ```

###### 3. 父子表三级联动

- models.py

  ```python
  from django.db import models
  
  class Area(models.Model):
      """
      区域表
      """
  
      name = models.CharField(max_length=100, verbose_name='名称')
      # parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='son', null=True, verbose_name='父级')
      parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
  
      class Meta:
          db_table = 'tb_areas'
  
      def __str__(self):
          return self.name
  ```

- views.py

  ```python
  class AreaSerializer(serializers.ModelSerializer):
      """
      地址序列化器
      """
      children = serializers.SerializerMethodField()
  
      class Meta:
          model = Area
          fields = '__all__'
  
      def get_children(self, obj):
          children = obj.children.all()
          serializer = AreaSerializer(children, many=True)
          return serializer.data
  
  
  class ObtailAreaView(APIView):
      authentication_classes = []
  
      def get(self, request):
          # # 获取parent_id
          # parent_id = request.query_params.get('parent_id')
          # # 如果获取到父级的id,则获取省级下面的信息（市、区、县）
          # if parent_id:
          #     area = Area.objects.filter(pk=parent_id).first()
          #     areas = area.son
          # # 如果没有参数，通过参数所有的省
          # else:
          #     areas = Area.objects.filter(parent__isnull=True).all()
          # area_ser = AreaSerializer(areas, many=True)
          # # 返回结果
          # return Response({'code': 200, 'areaList': area_ser.data})
  
          provinces = Area.objects.filter(parent__isnull=True)  # 获取顶级地区（省份）
          serializer = AreaSerializer(provinces, many=True)
          return Response(serializer.data)
  ```

#### 数据库

###### 数据库迁移

> You are trying to add the field 'created_at' with 'auto_now_add=True' to basicperformance without a default; the database needs something to populate existing rows.
>
>     1) Provide a one-off default now (will be set on all existing rows)
>     2) Quit, and let me add a default in models.py
>
> Please enter the default value now, as valid Python
> You can accept the default 'timezone.now' by pressing 'Enter' or you can provide another value.
> The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
> Type 'exit' to exit this prompt
>
> 出现这个提示信息的原因是，定义了created_at这个字段按创建的时间进行写入，但是数据库中原本的数据中并没有这个字段，当你更新表结构添加了created_at这个字段后，原来的数据添加了created_at这个字段后，需要添加默认值，用户只需输入1按步骤1运行，然后数据timezone.now添加默认时间即可，多张表则需要输入多次。

###### SQL语句

- 判断并删除表

  ```sql
  DROP TABLE IF EXISTS `xxx`;
  ```

###### django配置数据库连接

- pip install django==3.2.19 版本太高需要匹配8.0以上的mysql版本

- pip install pymysql==1.1.0

- 主引用中`__init__.py`设置使用pymysql作为数据库驱动

  ```python
  import pymysql
  pymysql.install_as_MySQLdb()
  ```

- 创建模型类

  ```python
  class Student(models.Model):
      # 模型字段
      name = models.CharField(max_length=100,verbose_name="姓名")
      sex = models.BooleanField(default=1,verbose_name="性别")
      age = models.IntegerField(verbose_name="年龄")
      class_null = models.CharField(max_length=5,verbose_name="班级编号")
      description = models.TextField(max_length=1000,verbose_name="个性签名")
  
      class Meta:
          db_table="tb_student"
          verbose_name = "学生"
          verbose_name_plural = verbose_name
  ```

- 创建数据库

  ```mysql
  create database students charset=utf8;
  ```

- settings.py配置文件中设置mysql的账号密码

  ```python
  DATABASES = {
      # 'default': {
      #     'ENGINE': 'django.db.backends.sqlite3',
      #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      # },
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': "students",
          "HOST": "127.0.0.1",
          "PORT": 3306,
          "USER": "root",
          "PASSWORD":"123",
      },
  }
  ```

- 数据迁移

  ```python
  python manage.py makemigrations
  python manage.py migrate
  ```

- 数据库初始化：python manage.py loaddata init_db.json

  ```json
  [
  {
    "model": "hook.userinfo",
    "pk": 1,
    "fields": {
      "userName": "admin",
      "userNickName": "admin",
      "email": "123456@qq.com",
      "isEnabled": true
    }
  },
  {
    "model": "hook.userinfo",
    "pk": 3,
    "fields": {
      "userName": "test666",
      "userNickName": "test123",
      "email": "",
      "isEnabled": true
    }
  }
      ]
  ```

  

#### Serializer - 序列化器类

```
- 序列化
	- 序列化器的类
		def get_字段名():
			...
	- 路由 -> 视图 -> 去数据库获取对象或QuerySet -> 序列化器的类转换成列表、字典、有序字典 -> JSON处理
	ser = DepartSerializer(instance=对象)

- 数据校验
	- 序列化器的类
	- 路由 -> 视图 -> request.data -> 校验（序列化器的类） -> 操作（db, 序列化器的类）
	
		ser = DepartSerializer(data=request.data)
		ser.validated_data
		models.Depart.objects.create(**ser.validated_data)
		
		ser = DepartModelSerializer(data=request.data)
		ser.validated_data
		ser.save()
		
		1. 自定义 Serializer + 字段
		2. 自定义 Serializer + 字段（内置+正则）
		3. 自定义 Serializer + 字段（内置+正则） + 字段钩子 + 全局钩子
		4. 自定义 Serializer + extra_kwargs + save(多，pop;少，save参数)
		5. 自定义 Serializer + FK => 自动获取关联数据 depart  => depart_id
		6. 自定义 Serializer + M2M => 自动获取关联数据 ListField或DictField + 钩子
```

##### 定义序列化器

> 继承rest_framework.serializers.Serializer
>
> serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义
>
> serializer是独立于数据库之外的存在

###### 常用字段类型

1. **CharField**

   ```python
   title = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
   ```

2. **IntegerField**

   ```python
   serializers.IntegerField(max_value=None, min_value=None)
   ```

3. **SerializerMethodField**

4. **PrimaryKeyRelatedField**

5. **ListSerializer**

6. **MultipleChoiceField**

7. 

###### 选项参数

1. **source**
2. **required**：表明该字段在反序列化时必须输入，默认True
3. **read_only**：表明该字段仅用于序列化输出（只有在序列化时使用），默认False
4. **write_only**：表明该字段仅用于反序列化输入（只有在校验时使用），默认False
5. **default**：反序列化时使用的默认值
6. **allow_null**：表明该字段是否允许传入None，默认False
7. **validators**：该字段使用的验证器
8. **error_messages**：包含错误编号与错误信息的字典
9. **label**：用于HTML展示API页面时，显示的字段名称
10. **help_text**：用于HTML展示API页面时，显示的字段帮助提示信息
11. **max_length**：最大长度
12. **min_lenght**：最小长度：
13. **allow_blank**：是否允许为空
14. **allow_null**
15. **allow_empty**
16. **trim_whitespace**：是否截断空白字符
17. **max_value**：最小值
18. **min_value**：最大值
19. **instance**
20. **data**
21. **partial**
22. **context**
23. **initial**

###### extra_kwargs

```python
class Depart(models.Model)
	title = models.CharField(verbose_name="部门", max_length=32)
    order = models.IntegerField(verbose_name="顺序")
    count = models.IntegerField(verbose_name="人数")
    
class Tag(models.Model)
	caption = models.CharField(verbose_name="标签", max_length=32)
    
class UserInfo(models.Model)
	name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    gender = models.SmallIntegerField(verbose_name="性别", choices=((1, "男"), (2, "女")))
    depart = models.Foreignkey(verbose_name="部门", to="Depart", on_delete=models.CASCADE)
    ctime = models.DateTimeField(verbose_name="时间", auto_now_add=True)
    tags = models.ManyToManyField(verbose_name="标签", to="Tag")

# 应用场景：用户注册时填写姓名、密码等信息，但是不会将密码返回。
class DepartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Depart
        fields = ["id", "title", "order", "count"]
        extra_kwargs = {
            "id": {"read_only": True},	# 只有在序列化时才会使用
            "count": {"write_only": True}, # 只有在校验时才会使用
        }

```

- SerializerMethodField到底是如何实现的执行钩子方法

  ```python
  class BaseSerializer(Field):
      @property
      def data(self):
          self._data = self.to_representation(self.validated_data)
          return self._data
  
  class Serializer(BaseSerializer, metaclass=SerializerMetaclass):
      @property
      def data(self):
          ret = super().data
          return ReturnDict(ret, serializer=self)
  
      def to_representation(self, instance):
      ret = OrderedDict()
      # [CharField字段对象，SerializerMethodField字段对象(method_name)，] # 内部会执行bind方法
      fields = self._readable_fields # 找到所有的字段，筛选出可以读取（可序列化） => read_only + 啥都没有 <=> 没有写write_only => 字段对象
  
      for field in fields:
          attribute = field.get_attribute(instance)   # CharFile字段对象.get_attribute()  instance.xxx.xxx.xxx SerializerMethodField字段对象(method_name).xxx -> None
          ret[field.field_name] = field.to_representation(attribute)
  
      return ret
  
  
  class ModelSerializer(Serializer):
      pass
  
  
  class NbModelSerializer(serializers.ModelSerializer):
      gender = SerializerMethodField()                        # get_attribute     to_representation
      name = serializers.CharField(source='xxx.xxx.xxx')      # get_attribute     to_representation
      class Meta:
          model = models.NbUserInfo
          fields = ["id", "name", "age", "gender"]
          extra_kwargs = {
              "id": {"read_only": True}
          }
      def get_gender(self, obj):
          return obj.get_gender_display()
  
  ser = NbModelSerializer(instance=对象)
  ser.data
  
  ser = NbModelSerializer(data=request.data)
  if ser.is_valid():
      ser.save()
      ser.data
  
  
  class Field:
      def get_attribute(self, instance):
          # instance.字段名称.xxx.xxx.xxx
          return get_attribute(instance, self.source_attrs)
  
  class CharField(Field):
      pass
  
  
  
  
  
  class UusSerializer(serializers.ModelSerializer):
      v1 = serializers.SerializerMethodField() # 对象实例化后还没被调用
  
  class SerializerMethodField(Field):
      def __init__(self, method_name=None, **kwargs):
          self.method_name = method_name # None v1 = serializers.SerializerMethodField()
          kwargs['source'] = '*'
          kwargs['read_only'] = True
          super().__init__(**kwargs)
  
      def bind(self, field_name, parent):
          # The method name defaults to `get_{field_name}`.
          if self.method_name is None:
              self.method_name = 'get_{field_name}'.format(field_name=field_name) # get_gender
  
          super().bind(field_name, parent)
  
      def to_representation(self, value):
          method = getattr(self.parent, self.method_name)
          return method(value)
  
  class MyCharField(serializers.IntegerField):    # 注意这里继承的是IntegerField
      def __init__(self, method_name=None, **kwargs):
          self.method_name = method_name # None
          super().__init__(**kwargs)
          
      def bind(self, field_name, parent):
          if self.method_name is None:
              self.method_name = 'xget_(field_name)'.format(field_name=field_name) # xget_gender
          super().bind(field_name, parent)
          
      def get_attribute(self, instance):
          method = getattr(self.parent, self.method_name)
          return str(value)
      
      def to_representation(self, value):
          return str(value)
  
  序列化
      - 加载字段
      - 示例 ser=MyModelSerializer(...)
      - ser.data # 这一步才开始序列化
  ```

- 针对choices

  ```python
  # 针对choices，方式一：
  class UusSerializer(serializers.ModelSerializer):
      gender_info = serializers.CharField(source="get_gender_display", read_only=True)
      class Meta:
          model = models.UserInfo
          fields = ["id", "name", "age", "gender", "depart", "gender_info"]
          extra_kwargs = {
              "id": {"read_only": True},	# 只有在序列化时才会使用
              "gender": {"write_only": True}, # 只有在校验时才会使用
          }
          
  # 针对choices，方式二：
  class UusSerializer(serializers.ModelSerializer):
      v1 = serializers.SerializerMethodField()
      class Meta:
          model = models.UserInfo
          fields = ["id", "name", "age", "gender", "depart", "v1"]
          extra_kwargs = {
              "id": {"read_only": True},	# 只有在序列化时才会使用
              "gender": {"write_only": True}, # 只有在校验时才会使用
          }
      def get_v1(self, obj):
          return {"id": obj.gender, "text": obj.get_gender_display()}
      
  # 针对choices，方式三：将方式一和方式而结合
  # SerializerMethodField到底是如何实现的执行钩子方法？
  class MyCharField(serializers.IntegerField):
      def __init__(self, method_name=None, **kwargs):
          self.method_name = method_name # None
          super().__init__(**kwargs)
          
      def bind(self, field_name, parent):
          if self.method_name is None:
              self.method_name = 'xget_(field_name)'.format(field_name=field_name) # xget_gender
          super().bind(field_name, parent)
          
      def get_attribute(self, instance):
          method = getattr(self.parent, self.method_name)
          return str(value)
      
      def to_representation(self, value):
          return str(value)
      
  class UusSerializer(serializers.ModelSerializer):
      gender = MyCharField()
      class Meta:
          model = models.UserInfo
          fields = ["id", "name", "age", "gender", "depart"]
          extra_kwargs = {
              "id": {"read_only": True}
          }
      def get_gender(self, obj):
          return obj.get_gender_display()
      
  # 针对choices，方式四：将方式一和方式而结合
  # SerializerMethodField到底是如何实现的执行钩子方法？
  from collections import OrderedDict
  from rest_framework.fields import SkipField
  from rest_framework.relations import PKOnlyObject
  class UusSerializer(serializers.ModelSerializer):
      class Meta:
          model = models.UserInfo
          fields = ["id", "name", "age", "gender", "depart"]
          extra_kwargs = {
              "id": {"read_only": True}
          }
          
      def to_representation(self, instance):
          ret = OrderedDict()
          fields = self._readable_fields
  
          for field in fields:
              # 判断钩子是否存在  getattr(self, nb_field.field_name)
              if hasattr(self, 'nb_%s' % field.field_name):
                  value = getattr(self, 'nb_%s' % field.field_name)(instance)
                  ret[field.field_name] = value
              else:
                  try:
                      attribute = field.get_attribute(instance)
                  except SkipField:
                      continue
                  check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
                  if check_for_none is None:
                      ret[field.field_name] = None
                  else:
                      ret[field.field_name] = field.to_representation(attribute)
              return ret
          
      def nb_gender(self, obj):
          return obj.get_gender_display()
      
  # 通过继承简化方式四：
  # ext.hook.py
  from collections import OrderedDict
  from rest_framework.fields import SkipField
  from rest_framework.relations import PKOnlyObject
  class HookSerializer
  	def to_representation(self, instance):
          ret = OrderedDict()
          fields = self._readable_fields
  
          for field in fields:
              # 判断钩子是否存在  getattr(self, nb_field.field_name)
              if hasattr(self, 'nb_%s' % field.field_name):
                  value = getattr(self, 'nb_%s' % field.field_name)(instance)
                  ret[field.field_name] = value
              else:
                  try:
                      attribute = field.get_attribute(instance)
                  except SkipField:
                      continue
                  check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
                  if check_for_none is None:
                      ret[field.field_name] = None
                  else:
                      ret[field.field_name] = field.to_representation(attribute)
          return ret
  
  # 序列化器中继承使用
  from ext.hook import NbHookSerializer
  class UusSerializer(NbHookSerializer, serializers.ModelSerializer):
      class Meta:
          model = models.UserInfo
          fields = ["id", "name", "age", "gender", "depart"]
          extra_kwargs = {
              "id": {"read_only": True}
          }
  
      def nb_gender(self, obj):
          return obj.get_gender_display()
  ```

- 针对Foreignkey

  ```python
  # 针对Foreignkey，方式一：
  class UusSerializer(serializers.ModelSerializer):
      v1 = serializers.CharField(source="depart.title", read_only=True)
      class Meta:
          model = models.UserInfo
          fields = ["id", "name", "age", "gender", "depart", "v1"]
          extra_kwargs = {
              "id": {"read_only": True},	# 只有在序列化时才会使用
              "gender": {"write_only": True}, # 只有在校验时才会使用
          }
          
  # 针对Foreignkey，方式二：
  class P1ModelSerializer(serializers.ModelSerializer):
      class Meta:
          model = models.Depart
          fields = "__all__"
  
  class UusSerializer(serializers.ModelSerializer):
      v1 = P1ModelSerializer(source="depart", read_only=True)
      class Meta:
          model = models.UserInfo
          fields = ["id", "name", "age", "gender", "depart", "v1"]
          extra_kwargs = {
              "id": {"read_only": True},	# 只有在序列化时才会使用
              "gender": {"write_only": True}, # 只有在校验时才会使用
          }
          
  # 针对Foreignkey，方式三：
  class UusSerializer(serializers.ModelSerializer):
      depart_id = serializers.IntegerField()
      class Meta:
          model = models.UserInfo
          fields = ["name", "age", "gender", "depart_id"]
  ```

- ManyToManyField

  ```python
  class UusSerializer(serializers.ModelSerializer):
      tags = serializers.ListField()
      class Meta:
          model = models.UserInfo
          fields = ["name", "age", "gender", "tags"]
          
      def validate_tags(self, value):
          queryset = models.Tag.objects.filter(id__in=value)
          return queryset
  ```

  

##### 创建Serializer对象

```python
Serializer(instance=None, data=empty, **kwarg)
```

- 用于序列化时，将模型类对象传入**instance**参数

- 用于反序列化时，将要被反序列化的数据传入**data**参数

- 除了instance和data参数外，在构造Serializer对象时，还可通过**context**参数额外添加数据，如

  ```python
  # 通过context参数附加的数据，可以通过Serializer对象的context属性获取。
  
  serializer = AccountSerializer(account, context={'request': request})
  ```

- 注意事项

  - 使用序列化器的时候一定要注意，序列化器声明了以后，不会自动执行，需要我们在视图中进行调用才可以。
  - 序列化器无法直接接收数据，需要我们在视图中创建序列化器对象时把使用的数据传递过来。
  - 序列化器的字段声明类似于我们前面使用过的表单系统。
  - 开发restful api时，序列化器会帮我们把模型数据转换成字典.
  - drf提供的视图会帮我们把字典转换成json,或者把客户端发送过来的数据转换字典.

##### 序列化

> 处理服务器响应时，使用序列化器可以完成对数据的序列化。
>
> 通过ORM从数据库获取到的 QuerySet 或 对象 均可以被序列化为 json 格式数据。

1. 序列化基本字段

   - 序列化QuerySet对象(many=True)

     ```python
     data_object = modes.UserInfo.objects.all()
     ser = UserModelSerializer(instance=data_object,many=True)
     ```

   - 序列化单一对象(many=False)

     ```python
     data_object = modes.UserInfo.objects.filter(id=2).first()
     ser = UserModelSerializer(instance=data_object,many=False)
     ser = UserModelSerializer(instance=data_object) # 默认many=False
     ```

2. 自定义字段

3. 序列化类的嵌套

   - FK
   - m2m

##### 反序列化 - 数据校验

> 处理客户端请求时，使用序列化器可以完成对数据的反序列化。

#### Django中static静态文件的设置

> django在DEBUG设为True和False的情况下读取的路径和方式有所区别

###### 第一步

> 由于当DEBUG为False的时候Django读取的STATIC_ROOT的值，而为True的时候读取的是STATICFILES_DIRS的值，所以在这里做一个判断。
>
> 在Settings.py的STATIC_URL = '/static/'后加入如下代码：

```python
STATIC_URL = '/static/'
if DEBUG == False: 
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
    STATICFILES_DIRS = [
	    os.path.join(BASE_DIR,"static")
    ]
```

###### 第二步

> 在URLS.py下添加如下代码：

```python
from django.views import static
from django.conf import settings 
from django.urls import path, re_path
 
urlpatterns = [
    path('admin/', admin.site.urls),
    
    re_path(r'^static/(?P<path>.*)$', static.serve,
      {'document_root': settings.STATIC_ROOT}, name='static'),
]
```

#### 用户模块管理：注册/登录/登出

###### settings.py

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:16379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            "PASSWORD": "123456"
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'Report.utils.authentication.CheckCache',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'Report.utils.authentication.NotAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": ["Report.utils.permission.AdminPermission", ],
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # JWT有效期
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'Report.utils.payload.jwt_response_payload_handler',
    'JWT_AUTH_HEADER_PREFIX': "bearer"
}
```

###### urls.py

```python
from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from Report import viewsets

router = SimpleRouter()

urlpatterns = [
    # 注册接口
    url(r"v1/register", viewsets.RegisterViewSet.as_view()),
    # JWT登录
    url(r"v1/login", obtain_jwt_token),  # 内部认证代码还是django的，主要作用是登录成功生成token
]
# 用户管理接口
router.register(r"v1/user", viewsets.UserViewSet)
urlpatterns += router.urls
```

###### utils

- authentication.py

  ```python
  from rest_framework.authentication import BaseAuthentication
  from rest_framework.exceptions import AuthenticationFailed
  from django.core.cache import cache
  
  class NotAuthentication(BaseAuthentication):
      def authenticate(self, request):
          raise AuthenticationFailed({"code": 401, "msg": "认证失败"})
      def authenticate_header(self, request):
          return 'Token'
  
  # 检查redis缓存中的token
  class CheckCache(BaseAuthentication):
      def authenticate(self, request):
          auth = request.META.get('HTTP_AUTHORIZATION', None)
          if not auth:
              raise AuthenticationFailed({"code": 401, "msg": "认证失败，没有token"})
          else:
              token = auth.split()[1]
              result = cache.get(f'{token}', None)
              if not result:
                  raise AuthenticationFailed({"code": 401, "msg": "认证失败，用户已经退出，请重新登录"})
              else:
                  return None
      def authenticate_header(self, request):
          return 'Token'
  ```

- permission.py

  ```python
  from rest_framework.permissions import BasePermission
  
  class AdminPermission(BasePermission):
      message = {"code": 403, 'data': "无权访问"}
      def has_permission(self, request, view):
          if request.user.is_superuser: # 校验是否为超级用户
              return True
          return False
      def has_object_permission(self, request, view, obj):
          return True
  ```

- payload.py

  ```python
  from django.core.cache import cache
  
  def jwt_response_payload_handler(token, user=None, request=None):
      """重写JWT登录视图的构造相应数据函数，多追加user_id和username"""
      cache.set(f'{token}', 1)  # 每次用户登录时都会将token缓存到redis
      return {
          'token': token,
          "user_id": user.id,
          "username": user.username,
          "is_superuser": user.is_superuser
      }
  ```

###### register.py-注册视图

```python
from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class RegisterSerializers(serializers.ModelSerializer):
    confirm = serializers.CharField(label="确认密码", write_only=True)
    token = serializers.CharField(label="token", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "confirm", "token", "is_superuser", "is_active"]
        # fields = "__all__"
        extra_kwargs = {  # 修改字段选项
            "id": {"read_only": True},
            "username": {
                'min_length': 3,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '仅允许3-20个字符的用户',
                    'max_length': '仅允许3-20个字符的用户',
                }
            },
            "password": {
                "write_only": True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '仅允许8-20个字符的用户',
                    'max_length': '仅允许8-20个字符的用户',
                }
            }
        }

    def validate(self, attrs):
        """校验密码两个是否相同"""
        obj = User.objects.filter(username=attrs['username']).first()
        if obj:
            raise serializers.ValidationError('用户名已存在')
        if attrs['password'] != attrs['confirm']:
            raise serializers.ValidationError('两个密码不一致')
        return attrs

    def create(self, validated_data):
        # 把不需要存储的confirm从字段中移除
        del validated_data['confirm']
        # 把密码先取出来
        password = validated_data.pop('password')
        # 创建用户模型对象，给模型中的username,role属性赋值
        user = User(**validated_data)
        user.set_password(password)  # 把密码加密后再赋值给user的password属性
        user.save()  # 存储到数据库

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt中的叫jwt_payload_handler的函数（生成payload）
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 函数引用
        payload = jwt_payload_handler(user)  # 根据user生成用户相关的载荷
        token = jwt_encode_handler(payload)  # 传入载荷生成完整的jwt
        user.token = token

        return user

    # def validate_mobile(self, value):
    #     """单独校验手机号"""
    #     if not re.match(r'1[3-9]\d{9}', value):
    #         raise serializers.ValidationError('手机号格式错误')
    #     return value

class RegisterViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers
    authentication_classes = []
    permission_classes = []
```

###### user.py-用户管理、登出视图、密码修改

```python
import django_filters
from rest_framework import viewsets, serializers
from Report.utils.pagination import Pagination
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_superuser", "is_active", "date_joined"]
        # depth = 1

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = "__all__"

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = Pagination
    filterset_class = UserFilter
    
    # 密码修改
    @action(methods=["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        username = request.user.username
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if old_password == new_password:
            return Response({"code": 401, "msg": "旧密码和旧密码不能相同，请重新输入！"})
        user = User.objects.filter(username=username).first()
        if user.check_password(old_password):
            user.set_password(str(new_password))  # 把密码加密后再赋值给user的password属性
            user.save()  # 存储到数据库
        else:
            return Response({"code": 401, "msg": "旧密码不正确，请重新输入正确的密码！"})

        return Response({"code": 201, "msg": "set password successful"})

    @action(methods=["get"], detail=False)
    def logout(self, request, *args, **kwargs):
        # 获取当前用户的 token
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        token = auth.split()[1]
        # 删除缓存
        cache.delete(f'{token}')
        return Response({'detail': '退出登录成功'})
```

###### docker desktop安装redis

- 拉取redis镜像

  ```
  docker pull redis:latest
  ```

- 创建redis配置文件，为挂载操作做准备

  >  在D盘创建2个文件夹：conf、data
  >  conf目录用于挂载配置文件
  >  data目录用于存放数据持久化文件

  - 在conf文件夹新建redis.conf文件

    ```
    #用守护线程的方式启动 后台运行
    daemonize no 
    #给redis设置密码
    # requirepass 123456 
    #redis持久化　　默认是no
    appendonly yes
    #防止出现远程主机强迫关闭了一个现有的连接的错误 默认是300
    tcp-keepalive 300 
    ```

- 构建并启动redis容器

  > –name=“容器新名字”：为容器指定一个名称
  > -p: 指定端口映射，格式为：主机(宿主)端口:容器端口
  > -d: 后台运行容器，并返回容器ID
  > -v /D/docker/redis/conf/redis.conf:/etc/redis/redis_6379.conf 把宿主机配置好的redis.conf放到容器内的这个位置中
  > -v /D/docker/redis/data:/data/ 把redis持久化的数据在宿主机内显示，做数据备份
  > –net=host

  ```
  # --appendonly yes 可不添加
  
  docker run --name redis -p 16379:6379 -v /D/docker/redis/conf/redis.conf:/etc/redis/redis_6379.conf -v /D/docker/redis/data:/data/ -d redis:latest redis-server /etc/redis/redis_6379.conf --appendonly yes
  ```

###### JWT登录模块源码解析

> from rest_framework_jwt.views import obtain_jwt_token

- views.py

  ```python
  obtain_jwt_token = ObtainJSONWebToken.as_view()
  
  class ObtainJSONWebToken(JSONWebTokenAPIView):
      serializer_class = JSONWebTokenSerializer
  ```

- JSONWebTokenAPIView

  ```python
  class JSONWebTokenAPIView(APIView):
      """
      Base API View that various JWT interactions inherit from.
      """
      permission_classes = ()
      authentication_classes = ()
  
      def get_serializer_context(self):
          """
          Extra context provided to the serializer class.
          """
          return {
              'request': self.request,
              'view': self,
          }
  
      def get_serializer_class(self):
          """
          Return the class to use for the serializer.
          Defaults to using `self.serializer_class`.
          You may want to override this if you need to provide different
          serializations depending on the incoming request.
          (Eg. admins get full serialization, others get basic serialization)
          """
          assert self.serializer_class is not None, (
              "'%s' should either include a `serializer_class` attribute, "
              "or override the `get_serializer_class()` method."
              % self.__class__.__name__)
          return self.serializer_class
  
      def get_serializer(self, *args, **kwargs):
          """
          Return the serializer instance that should be used for validating and
          deserializing input, and for serializing output.
          """
          serializer_class = self.get_serializer_class()
          kwargs['context'] = self.get_serializer_context()
          return serializer_class(*args, **kwargs)
  
      def post(self, request, *args, **kwargs):
          serializer = self.get_serializer(data=request.data)
  
          if serializer.is_valid():
              user = serializer.object.get('user') or request.user
              token = serializer.object.get('token')
              response_data = jwt_response_payload_handler(token, user, request)
              response = Response(response_data)
              if api_settings.JWT_AUTH_COOKIE:
                  expiration = (datetime.utcnow() +
                                api_settings.JWT_EXPIRATION_DELTA)
                  response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                      token,
                                      expires=expiration,
                                      httponly=True)
              return response
  
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  ```

- JSONWebTokenSerializer

  ```python
  class JSONWebTokenSerializer(Serializer):
      """
      Serializer class used to validate a username and password.
  
      'username' is identified by the custom UserModel.USERNAME_FIELD.
  
      Returns a JSON Web Token that can be used to authenticate later calls.
      """
      def __init__(self, *args, **kwargs):
          """
          Dynamically add the USERNAME_FIELD to self.fields.
          """
          super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)
  
          self.fields[self.username_field] = serializers.CharField()
          self.fields['password'] = PasswordField(write_only=True)
  
      @property
      def username_field(self):
          return get_username_field()
  
      def validate(self, attrs):
          credentials = {
              self.username_field: attrs.get(self.username_field),
              'password': attrs.get('password')
          }
  
          if all(credentials.values()):
              # 调用django的用户验证方法
              user = authenticate(**credentials)
  
              if user:
                  if not user.is_active:
                      msg = _('User account is disabled.')
                      raise serializers.ValidationError(msg)
  
                  payload = jwt_payload_handler(user)
  
                  return {
                      'token': jwt_encode_handler(payload),
                      'user': user
                  }
              else:
                  msg = _('Unable to log in with provided credentials.')
                  raise serializers.ValidationError(msg)
          else:
              msg = _('Must include "{username_field}" and "password".')
              msg = msg.format(username_field=self.username_field)
              raise serializers.ValidationError(msg)
  ```

###### 用户认证模块源码解析

> rest_framework_jwt.authentication.JSONWebTokenAuthentication

- JSONWebTokenAuthentication

  ```python
  class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
      www_authenticate_realm = 'api'
  
      def get_jwt_value(self, request):
          auth = get_authorization_header(request).split()
          auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
  
          if not auth:
              if api_settings.JWT_AUTH_COOKIE:
                  return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
              return None
  
          if smart_text(auth[0].lower()) != auth_header_prefix:
              return None
  
          if len(auth) == 1:
              msg = _('Invalid Authorization header. No credentials provided.')
              raise exceptions.AuthenticationFailed(msg)
          elif len(auth) > 2:
              msg = _('Invalid Authorization header. Credentials string '
                      'should not contain spaces.')
              raise exceptions.AuthenticationFailed(msg)
  
          return auth[1]
  
      def authenticate_header(self, request):
          return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)
  ```

- BaseJSONWebTokenAuthentication

  ```python
  class BaseJSONWebTokenAuthentication(BaseAuthentication):
  
      def authenticate(self, request):
          jwt_value = self.get_jwt_value(request)
          if jwt_value is None:
              return None
  
          try:
              payload = jwt_decode_handler(jwt_value)
          except jwt.ExpiredSignature:
              msg = _('Signature has expired.')
              raise exceptions.AuthenticationFailed(msg)
          except jwt.DecodeError:
              msg = _('Error decoding signature.')
              raise exceptions.AuthenticationFailed(msg)
          except jwt.InvalidTokenError:
              raise exceptions.AuthenticationFailed()
  
          user = self.authenticate_credentials(payload)
  
          return (user, jwt_value)
  
      def authenticate_credentials(self, payload):
          User = get_user_model()
          username = jwt_get_username_from_payload(payload)
  
          if not username:
              msg = _('Invalid payload.')
              raise exceptions.AuthenticationFailed(msg)
  
          try:
              user = User.objects.get_by_natural_key(username)
          except User.DoesNotExist:
              msg = _('Invalid signature.')
              raise exceptions.AuthenticationFailed(msg)
  
          if not user.is_active:
              msg = _('User account is disabled.')
              raise exceptions.AuthenticationFailed(msg)
  
          return user
  ```

#### 部署前端项目

1. 将dist前端打包后的文件放置在/media目录下，并重命名为html；

2. 在settings.py中添加配置

   ```
   MEDIA_ROOT = os.path.join(BASE_DIR, r'Report\media\html\assets')
   MEDIA = os.path.join(BASE_DIR, r'Report\media\html\index.html')
   ```

3. 在urls.py中添加接口

   ```python
   import mimetypes
   from pathlib import Path
   from django.http import FileResponse
   from django.utils.http import http_date
   
   def serve1(request, path, document_root=None, show_indexes=False):
       fullpath = Path(document_root)
       statobj = fullpath.stat()
       content_type, encoding = mimetypes.guess_type(str(fullpath))
       content_type = content_type or "application/octet-stream"
       response = FileResponse(fullpath.open("rb"), content_type=content_type)
       response.headers["Last-Modified"] = http_date(statobj.st_mtime)
       if encoding:
           response.headers["Content-Encoding"] = encoding
       return response
   
   urlpatterns = [
       re_path(r'^assets/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
       re_path('(?P<path>.*)$', serve1, {'document_root': settings.MEDIA})
   ]
   ```



#### 注意事项

1. 多找几个一对一、一对多、多对多的案例练习
2. 多练习聚合操作annotate、aggregate
3. 熟练掌握pandas数据处理

```python
from blue_krill.web.drf_utils import inject_serializer

@inject_serializer(body_in=xxx, out=xxx)

# settings.py
# drf crown
DRF_CROWN_DEFAULT_CONFIG = {"remain_request": True}
```

- jq安装

  ```
  - 如果要在Windows上顺利的使用jq，需要先安装chocolatey。
  - 以管理员身份待开cmd窗口，输入@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"，回车。
  - 接着输入choco install jq -y
  ```

