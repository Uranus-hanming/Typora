[toc]

# day15 drf-下篇

上节内容：前后端分离概述、纯净项目、request对象、认证、权限、限流、版本、解析器、序列化器等。

本节内容：

- **序列化器**，将ORM获取的数据库QuerySet或数据对象**序列化**成JSON格式 + **请求数据格式校验**。（最重要）
- 分页，对ORM中获取的数据进行分页处理，分批返回给用户。
- 视图，drf中提供了APIView+其他视图类让我们来继承。
- 路由，配合视图快速生成增删改查相关的路由+视图关系。
- 条件筛选，编写API搜索。





























## 1.博客系统（案例）

开发一个博客系统，包含：博客列表、详细、登录、注册、**评论、点赞、发布博客**。



### 1.1 表结构

```python
from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True,db_index=True)


class Blog(models.Model):
    category_choices = ((1, "云计算"), (2, "Python全栈"), (3, "Go开发"))
    category = models.IntegerField(verbose_name="分类", choices=category_choices)

    image = models.CharField(verbose_name="封面", max_length=255)
    title = models.CharField(verbose_name="标题", max_length=32)
    summary = models.CharField(verbose_name="简介", max_length=256)
    text = models.TextField(verbose_name="博文")
    ctime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    creator = models.ForeignKey(verbose_name="创建者", to="UserInfo", on_delete=models.CASCADE)

    comment_count = models.PositiveIntegerField(verbose_name="评论数", default=0)
    favor_count = models.PositiveIntegerField(verbose_name="赞数", default=0)


class Favor(models.Model):
    """ 赞 """
    blog = models.ForeignKey(verbose_name="博客", to="Blog", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog', 'user'], name='uni_favor_blog_user')
        ]


class Comment(models.Model):
    """ 评论表 """
    blog = models.ForeignKey(verbose_name="博客", to="Blog", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)

    content = models.CharField(verbose_name="内容", max_length=150)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
```



### 1.2 功能

- 博客列表

  ```
  路由 + 视图（时间倒序排序） + 序列化
  ```

- 博客详细

  ```
  路由（PK） + 新视图或原视图 + 序列化
  ```

- 评论列表

  ```
  在URL上通过GET方式传入博客ID，根据博客ID获取相关评论。
  
  提示：请求可以单独，也可以在博客详细的请求中返回。
  ```

- 注册

  ```
  输入用户信息+重复密码进行注册
  ```

- 登录

  ```
  登录成功，生成TOKEN+失效日期，返回。
  ```

- 创建评论（需登录）

  ```
  在URL上通过GET方式传入博客ID + 请求体中评论信息 发送到后端API
  - 认证组件，request.user
  - 构造参数保存
  ```

- 点赞（需登录）

  ```
  - 赞过不能再赞
  - 结合事务实现添加赞 + 赞数量更新。
  ```

- 新建博文（需登录）

  





























## 2.分页

在查看数据列表的API中，如果 数据量 比较大，肯定不能把所有的数据都展示给用户，而需要通过分页展示。

在drf中为我们提供了一些分页先关类：

```
BasePagination，基类
PageNumberPagination(BasePagination)	支持 /accounts/?page=4&page_size=100 格式的分页
LimitOffsetPagination(BasePagination)	支持 ?offset=100&limit=10 格式的分页
```



### 2.1 PageNumberPagination



![请添加图片描述](https://img-blog.csdnimg.cn/direct/0976e999a25c486fb3b80eeec5730dd5.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/4eb1f527bb5b47c5bdf4b3463c2e0e64.png)




### 2.2 LimitOffsetPagination

![请添加图片描述](https://img-blog.csdnimg.cn/direct/07033bf354b14ce29a1bbbc08d45cf7c.png)


注意：limitOffset的形式一般会结合上一次的商品ID，查询小于此ID的商品，实现 滚动下来分析。



应用：

- 博客列表，使用LimitOffsetPagination
- 评论列表，使用PageNumberPagination





## 3.视图



### 3.1 APIView

- View，django
- APIView，drf，在请求到来时，新增了：免除csrf、请求封装、版本、认证、权限、限流的功能。

```python
class GenericAPIView(APIView):
    pass # 10功能

class GenericViewSet(xxxx.View-2个功能, GenericAPIView):
    pass # 5功能能

class UserView(GenericViewSet):
    def get(self,request):
        pass
```

`APIView`是drf中 “顶层” 的视图类，在他的内部主要实现drf基础的组件的使用，例如：版本、认证、权限、限流等。

```python
# urls.py

from django.urls import path, re_path, include
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view()),
    path('api/users/<int:pk>/', views.UserDetailView.as_view()),
]
```

```python
# views.py

from rest_framework.views import APIView
from rest_framework.response import Response

class UserView(APIView):
    
    # 认证、权限、限流等
    
    def get(self, request):
		# 业务逻辑：查看列表
        return Response({"code": 0, 'data': "..."})

    def post(self, request):
        # 业务逻辑：新建
        return Response({'code': 0, 'data': "..."})
    
class UserDetailView(APIView):
    
	# 认证、权限、限流等
        
    def get(self, request,pk):
		# 业务逻辑：查看某个数据的详细
        return Response({"code": 0, 'data': "..."})

    def put(self, request,pk):
        # 业务逻辑：全部修改
        return Response({'code': 0, 'data': "..."})
    
    def patch(self, request,pk):
        # 业务逻辑：局部修改
        return Response({'code': 0, 'data': "..."})
    
    def delete(self, request,pk):
        # 业务逻辑：删除
        return Response({'code': 0, 'data': "..."})
```



### 3.2 GenericAPIView

`GenericAPIView` 继承APIView，在APIView的基础上又增加了一些功能。例如：`get_queryset`、`get_object`等。

实际在开发中一般不会直接继承它，他更多的是担任 `中间人`的角色，为子类提供公共功能。

```python
# urls.py

from django.urls import path, re_path, include
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view()),
    path('api/users/<int:pk>/', views.UserDetailView.as_view()),
]
```

```python
# views.py

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class UserView(GenericAPIView):
    queryset = models.UserInfo.objects.filter(status=True)
    serializer_class = 序列化类
    
    def get(self, request):
        queryset = self.get_queryset()
        ser = self.get_serializer(intance=queryset,many=True)
        print(ser.data)
        return Response({"code": 0, 'data': "..."})    
```



注意：最大的意义，将数据库查询、序列化类提取到类变量中，后期再提供公共的get/post/put/delete等方法，让开发者只定义类变量，自动实现增删改查。



### 3.3 GenericViewSet

![请添加图片描述](https://img-blog.csdnimg.cn/direct/5e298e7cdae14919801cac35d580c0b1.png)


`GenericViewSet`类中没有定义任何代码，他就是继承 `ViewSetMixin` 和 `GenericAPIView`，也就说他的功能就是将继承的两个类的功能继承到一起。

- `GenericAPIView`，将数据库查询、序列化类的定义提取到类变量中，便于后期处理。
- `ViewSetMixin`，将 get/post/put/delete 等方法映射到 list、create、retrieve、update、partial_update、destroy方法中，让视图不再需要两个类。

```python
# urls.py

from django.urls import path, re_path, include
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view({"get":"list","post":"create"})),
    path('api/users/<int:pk>/', views.UserView.as_view({"get":"retrieve","put":"update","patch":"partial_update","delete":"destory"})),
]
```

```python
# views.py

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

    
class UserView(GenericViewSet):
    
	# 认证、权限、限流等
    queryset = models.UserInfo.objects.filter(status=True)
    serializer_class = 序列化类
    
    def list(self, request):
		# 业务逻辑：查看列表
        queryset = self.get_queryset()
        ser = self.get_serializer(intance=queryset,many=True)
        print(ser.data)
        return Response({"code": 0, 'data': "..."})

    def create(self, request):
        # 业务逻辑：新建
        return Response({'code': 0, 'data': "..."})
    
    def retrieve(self, request,pk):
		# 业务逻辑：查看某个数据的详细
        return Response({"code": 0, 'data': "..."})

    def update(self, request,pk):
        # 业务逻辑：全部修改
        return Response({'code': 0, 'data': "..."})
    
    def partial_update(self, request,pk):
        # 业务逻辑：局部修改
        return Response({'code': 0, 'data': "..."})
    
    def destory(self, request,pk):
        # 业务逻辑：删除
        return Response({'code': 0, 'data': "..."})
```



注意：开发中一般也很少直接去继承他，因为他也属于是 `中间人`类，在原来 `GenericAPIView` 基础上又增加了一个映射而已。



### 3.4 五大类

在drf的为我们提供好了5个用于做 增、删、改（含局部修改）、查列表、查单个数据的5个类（需结合 `GenericViewSet` 使用）。

```python
# urls.py

from django.urls import path, re_path, include
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view({"get":"list","post":"create"})),
    path('api/users/<int:pk>/', views.UserView.as_view({"get":"retrieve","put":"update","patch":"partial_update","delete":"destroy"})),
]
```

```python
# views.py

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
    DestroyModelMixin, ListModelMixin
)

class UserView(CreateModelMixin,RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,ListModelMixin,GenericViewSet):
    
	# 认证、权限、限流等
    queryset = models.UserInfo.objects.filter(status=True)
    serializer_class = 序列化类
```



在这个5个类中已帮我们写好了 `list`、`create`、`retrieve`、`update`、`partial_update`、`destory` 方法，我们只需要在根据写 类变量：queryset、serializer_class即可。

**示例1：**

![请添加图片描述](https://img-blog.csdnimg.cn/direct/c0db4afdd8b649508f0fe43a6a36446b.png)


```python
# urls.py

from django.urls import path
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view({"get": "list"})),
    path('api/users/<int:pk>/', views.UserView.as_view({"get": "retrieve"})),
]
```

```python
# views.py

from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )
    extra = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["username", "age", "email", "level_text", "extra"]

    def get_extra(self, obj):
        return 666


class UserView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerializer
```



**示例2：**

![请添加图片描述](https://img-blog.csdnimg.cn/direct/f58dc392249c413584280d458be49405.png)


```python
# urls.py

from django.urls import path
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view({"get": "list", "post": "create"})),
    path('api/users/<int:pk>/', views.UserView.as_view({"get": "retrieve"})),
]
```

```python
# views.py

from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )
    extra = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["username", "age", "email", "level_text", "extra"]

    def get_extra(self, obj):
        return 666


class UserView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        """ 序列化：对请求的数据校验成功后，执行保存。"""
        serializer.save(depart_id=1, password="123")
```





**示例3：**

```python
# urls.py

from django.urls import path
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view(
        {"get": "list", "post": "create"}
    )),
    path('api/users/<int:pk>/', views.UserView.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
]

```

```python
# views.py

from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )
    extra = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["username", "age", "email", "level_text", "extra"]

    def get_extra(self, obj):
        return 666


class UserView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               GenericViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        """ 序列化：对请求的数据校验成功后，执行保存。"""
        serializer.save(depart_id=1, password="123")
	
	def perform_update(self, serializer):
        serializer.save()
        
    def perform_destroy(self, instance):
        instance.delete()
```



**示例4：**

```python
# urls.py

from django.urls import path
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view(
        {"get": "list", "post": "create"}
    )),
    path('api/users/<int:pk>/', views.UserView.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
]

```

```python
# views.py
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )
    extra = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["username", "age", "email", "level_text", "extra"]

    def get_extra(self, obj):
        return 666


class UserView(ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        """ 序列化：对请求的数据校验成功后，执行保存。"""
        serializer.save(depart_id=1, password="123")
```



在开发过程中使用 `五大类` 或 `ModelViewSet` 是比较常见的，并且如果他们内部的某些功能不够用，还可以进行重新某些方法进行扩展。



问题：drf中提供了这么多视图，以后那个用的比较多？

- 接口与数据库操作无关，直接继承APIView

- 接口背后需要对数据库进行操作，一般：`ModelViewSet` 或 `CreateModelMixin、ListModelMixin...`

  ```
  - 利用钩子自定义功能。
  - 重写某个写方法，实现更加完善的功能。
  ```

- 根据自己公司的习惯，自定义 ：`ModelViewSet` 或 `CreateModelMixin、ListModelMixin...`



### 3.5 额外的

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class XXXModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"

        
class XXXView(ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = XXXModelSerializer

    # @action(detail=False, methods=['get'], url_path="yyy/(?P<xx>\d+)/xxx")
    # def get_password(self, request, xx, pk=None):
    #     print(xx)
    #     return Response("...")

    # @action(detail=True, methods=['get'], url_path="yyy/(?P<xx>\d+)/xxx")
    # def set_password(self, request, xx, pk=None):
    #     print(xx)
    #     return Response("...")

```







### 补充：权限

在之前定义权限类时，类中可以定义两个方法：`has_permission` 和 `has_object_permission` 

- `has_permission` ，在请求进入视图之前就会执行。
- `has_object_permission`，当视图中调用 `self.get_object`时就会被调用（删除、更新、查看某个对象时都会调用），一般用于检查对某个对象是否具有权限进行操作。

```python
class PermissionA(BasePermission):
    message = {"code": 1003, 'data': "无权访问"}

    def has_permission(self, request, view):
        exists = request.user.roles.filter(title="员工").exists()
        if exists:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True
```



所以，让我们在编写视图类时，如果是直接获取间接继承了 GenericAPIView，同时内部调用 `get_object`方法，这样在权限中通过 `has_object_permission` 就可以进行权限的处理。



## 4. 路由

在之前进行drf开发时，对于路由我们一般进行两种配置：

- 视图继承APIView

  ```python
  from django.urls import path
  from app01 import views
  
  urlpatterns = [
      path('api/users/', views.UserView.as_view()),
  ]
  ```

- 视图继承 `ViewSetMixin`（GenericViewSet、ModelViewSet）

  ```python
  from django.urls import path, re_path, include
  from app01 import views
  
  urlpatterns = [
      path('api/users/', views.UserView.as_view({"get":"list","post":"create"})),
      path('api/users/<int:pk>/', views.UserView.as_view({"get":"retrieve","put":"update","patch":"partial_update","delete":"destory"})),
  ]
  ```

  对于这种形式的路由，drf中提供了更简便的方式：

  ```python
  from rest_framework import routers
  from app01 import views
  
  router = routers.SimpleRouter()
  router.register(r'api/users', views.UserView)
  
  urlpatterns = [
      # 其他URL
      # path('xxxx/', xxxx.as_view()),
  ]
  
  urlpatterns += router.urls
  ```

  

  也可以利用include，给URL加前缀：

  ```python
  from django.urls import path, include
  from rest_framework import routers
  from app01 import views
  
  router = routers.SimpleRouter()
  router.register(r'users', views.UserView)
  
  urlpatterns = [
      path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
      # 其他URL
      # path('forgot-password/', ForgotPasswordFormView.as_view()),
  ]
  ```





## 5. 条件搜索

如果某个API需要传递一些条件进行搜索，其实就在是URL后面通过GET传参即可，例如：

```
/api/users?age=19&category=12
```

在drf中也有相应组件可以支持条件搜索。

### 5.1 自定义Filter

![请添加图片描述](https://img-blog.csdnimg.cn/direct/74df95235065454493bc889d25743368.png)


```python
# urls.py

from django.urls import path
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view(
        {"get": "list", "post": "create"}
    )),
    path('api/users/<int:pk>/', views.UserView.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
    )),
]
```

```python
# views.py

from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import BaseFilterBackend
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )
    extra = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["username", "age", "email", "level_text", "extra"]

    def get_extra(self, obj):
        return 666


class Filter1(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        age = request.query_params.get('age')
        if not age:
            return queryset
        return queryset.filter(age=age)


class Filter2(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user_id = request.query_params.get('id')
        if not user_id:
            return queryset
        return queryset.filter(id__gt=user_id)


class UserView(ModelViewSet):
    filter_backends = [Filter1, Filter2]

    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        """ 序列化：对请求的数据校验成功后，执行保存。"""
        serializer.save(depart_id=1, password="123")
```



### 5.2 第三方Filter

在drf开发中有一个常用的第三方过滤器：DjangoFilterBackend。

```
pip install django-filter
```

注册app：

```python
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]
```

视图配置和应用（示例1）：

```python
# views.py
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )
    extra = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["username", "age", "email", "level_text", "extra"]

    def get_extra(self, obj):
        return 666


class UserView(ModelViewSet):
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ["id", "age", "email"]

    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        """ 序列化：对请求的数据校验成功后，执行保存。"""
        serializer.save(depart_id=1, password="123")

```



视图配置和应用（示例2）：

```python
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, filters
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )
    depart_title = serializers.CharField(
        source="depart.title",
        read_only=True
    )
    extra = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["id", "username", "age", "email", "level_text", "extra", "depart_title"]

    def get_extra(self, obj):
        return 666


class MyFilterSet(FilterSet):
    depart = filters.CharFilter(field_name="depart__title", lookup_expr="exact")
    min_id = filters.NumberFilter(field_name='id', lookup_expr='gte')

    class Meta:
        model = models.UserInfo
        fields = ["min_id", "depart"]


class UserView(ModelViewSet):
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = MyFilterSet

    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        """ 序列化：对请求的数据校验成功后，执行保存。"""
        serializer.save(depart_id=1, password="123")

```



视图配置和应用（示例3）：

```python
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from django_filters import FilterSet, filters
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(
        source="get_level_display",
        read_only=True
    )
    depart_title = serializers.CharField(
        source="depart.title",
        read_only=True
    )
    extra = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["id", "username", "age", "email", "level_text", "extra", "depart_title"]

    def get_extra(self, obj):
        return 666


class MyFilterSet(FilterSet):
    # /api/users/?min_id=2  -> id>=2
    min_id = filters.NumberFilter(field_name='id', lookup_expr='gte')

    # /api/users/?name=wupeiqi  -> not ( username=wupeiqi )
    name = filters.CharFilter(field_name="username", lookup_expr="exact", exclude=True)

    # /api/users/?depart=xx     -> depart__title like %xx%
    depart = filters.CharFilter(field_name="depart__title", lookup_expr="contains")

    # /api/users/?token=true      -> "token" IS NULL
    # /api/users/?token=false     -> "token" IS NOT NULL
    token = filters.BooleanFilter(field_name="token", lookup_expr="isnull")

    # /api/users/?email=xx     -> email like xx%
    email = filters.CharFilter(field_name="email", lookup_expr="startswith")

    # /api/users/?level=2&level=1   -> "level" = 1 OR "level" = 2（必须的是存在的数据，否则报错-->内部有校验机制）
    # level = filters.AllValuesMultipleFilter(field_name="level", lookup_expr="exact")
    level = filters.MultipleChoiceFilter(field_name="level", lookup_expr="exact", choices=models.UserInfo.level_choices)

    # /api/users/?age=18,20     -> age in [18,20]
    age = filters.BaseInFilter(field_name='age', lookup_expr="in")

    # /api/users/?range_id_max=10&range_id_min=1    -> id BETWEEN 1 AND 10
    range_id = filters.NumericRangeFilter(field_name='id', lookup_expr='range')

    # /api/users/?ordering=id     -> order by id asc
    # /api/users/?ordering=-id     -> order by id desc
    # /api/users/?ordering=age     -> order by age asc
    # /api/users/?ordering=-age     -> order by age desc
    ordering = filters.OrderingFilter(fields=["id", "age"])

    # /api/users/?size=1     -> limit 1（自定义搜索）
    size = filters.CharFilter(method='filter_size', distinct=False, required=False)
    
    class Meta:
        model = models.UserInfo
        fields = ["id", "min_id", "name", "depart", "email", "level", "age", 'range_id', "size", "ordering"]

    def filter_size(self, queryset, name, value):
        int_value = int(value)
        return queryset[0:int_value]


class UserView(ModelViewSet):
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = MyFilterSet

    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        """ 序列化：对请求的数据校验成功后，执行保存。"""
        serializer.save(depart_id=1, password="123")

```

`lookup_expr`有很多常见选择：

```python
'exact': _(''),
'iexact': _(''),

'contains': _('contains'),
'icontains': _('contains'),
'startswith': _('starts with'),
'istartswith': _('starts with'),
'endswith': _('ends with'),  
'iendswith': _('ends with'),
    
'gt': _('is greater than'),
'gte': _('is greater than or equal to'),
'lt': _('is less than'),
'lte': _('is less than or equal to'),

'in': _('is in'),
'range': _('is in range'),
'isnull': _(''),
    
'regex': _('matches regex'),
'iregex': _('matches regex'),
```



全局配置和应用：

```python
# settings.py 全局配置

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',]
}
```





### 5.3 内置Filter

drf源码中内置了2个filter，分别是：

- OrderingFilter，支持排序。

  ```python
  from rest_framework import serializers
  from rest_framework.viewsets import ModelViewSet
  from app01 import models
  from rest_framework.filters import OrderingFilter
  
  
  class UserModelSerializer(serializers.ModelSerializer):
      level_text = serializers.CharField(
          source="get_level_display",
          read_only=True
      )
      depart_title = serializers.CharField(
          source="depart.title",
          read_only=True
      )
      extra = serializers.SerializerMethodField(read_only=True)
  
      class Meta:
          model = models.UserInfo
          fields = ["id", "username", "age", "email", "level_text", "extra", "depart_title"]
  
      def get_extra(self, obj):
          return 666
  
  
  class UserView(ModelViewSet):
      filter_backends = [OrderingFilter, ]
      # ?order=id
      # ?order=-id
      # ?order=age
      ordering_fields = ["id", "age"]
  
      queryset = models.UserInfo.objects.all()
      serializer_class = UserModelSerializer
  
      def perform_create(self, serializer):
          """ 序列化：对请求的数据校验成功后，执行保存。"""
          serializer.save(depart_id=1, password="123")
  ```

- SearchFilter，支持模糊搜索。

  ```python
  from rest_framework import serializers
  from rest_framework.viewsets import ModelViewSet
  from app01 import models
  from rest_framework.filters import SearchFilter
  
  
  class UserModelSerializer(serializers.ModelSerializer):
      level_text = serializers.CharField(
          source="get_level_display",
          read_only=True
      )
      depart_title = serializers.CharField(
          source="depart.title",
          read_only=True
      )
      extra = serializers.SerializerMethodField(read_only=True)
  
      class Meta:
          model = models.UserInfo
          fields = ["id", "username", "age", "email", "level_text", "extra", "depart_title"]
  
      def get_extra(self, obj):
          return 666
  
  
  class UserView(ModelViewSet):
      # ?search=武沛%齐
      filter_backends = [SearchFilter, ]
      search_fields = ["id", "username", "age"]
  
      queryset = models.UserInfo.objects.all()
      serializer_class = UserModelSerializer
  
      def perform_create(self, serializer):
          """ 序列化：对请求的数据校验成功后，执行保存。"""
          serializer.save(depart_id=1, password="123")
  
  ```

  ```python
  "app01_userinfo"."id" LIKE %武沛齐% ESCAPE '\' 
  OR 
  "app01_userinfo"."username" LIKE %武沛齐% ESCAPE '\' 
  OR 
  "app01_userinfo"."age" LIKE %武沛齐% ESCAPE '\'
  ```