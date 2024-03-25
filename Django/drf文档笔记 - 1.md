@[toc]
# day13 drf-上篇

## 1.前后端分离

![请添加图片描述](https://img-blog.csdnimg.cn/direct/db5e4c4c7ce84f6088fa9dddd8e8944e.png)
## 2.FBV和CBV

- FBV，function base views，其实就是编写函数来处理业务请求。

  ```python
  from django.contrib import admin
  from django.urls import path
  from app01 import views
  urlpatterns = [
      path('users/', views.users),
  ]
  ```

  ```python
  from django.http import JsonResponse
  
  def users(request,*args, **kwargs):
      if request.method == "GET":
          return JsonResponse({"code":1000,"data":"xxx"})
      elif request.method == 'POST':
          return JsonResponse({"code":1000,"data":"xxx"})
      ...
  ```

- CBV，class base views，其实就是编写类来处理业务请求。

  ```python
  from django.contrib import admin
  from django.urls import path
  from app01 import views
  urlpatterns = [
      path('users/', views.UserView.as_view()),
  ]
  ```

  ```python
  from django.views import View
  
  class UserView(View):
      def get(self, request, *args, **kwargs):
          return JsonResponse({"code": 1000, "data": "xxx"})
  
      def post(self, request, *args, **kwargs):
          return JsonResponse({"code": 1000, "data": "xxx"})
  ```

其实，CBV和FBV的底层实现本质上相同的。



## 3.drf

django restframework框架 是在django的基础上又给我们提供了很多方便的功能，让我们可以更便捷基于django开发restful API，来一个简单的实例，快速了解下：

注意：drf支持cbv和fbv，只不过基于drf在进行api开发时，一般都是使用cbv的形式。



### 3.1 drf项目（纯净版）

示例代码详见：`drf_demo-1.zip`



```
pip install django==3.2
pip install djangorestframework
```



#### 3.1.1 核心配置

```python
INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    "UNAUTHENTICATED_USER": None
}

```



#### 3.1.2 路由

```python
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('users/', views.UserView.as_view()),
]
```



#### 3.1.3 视图

```python
from rest_framework.views import APIView
from rest_framework.response import Response


class UserView(APIView):
    def get(self, request):
        return Response("...")
```



### 3.2 request和参数

#### 3.2.1 参数

示例代码详见：`drf_demo-2.zip`

![请添加图片描述](https://img-blog.csdnimg.cn/direct/c70fad9c8f1b4bda9aa29f2dd3871f81.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/e7ee6e36fcbb46568e41e6003371740e.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/3c734e19b09d42f2a5b2d9cb0b541507.png)




#### 3.2.2 request对象

##### 1.属性

先来学一个关于面向对象的知识点。

```python
class Request(object):
    def __init__(self, req, xx):
        self._request = req
        self.xx = xx


obj = Request(1, 2)
print(obj.xx)
print(obj._request)
```

获取对象中的成员时，本质上会调用 `__getattribute__`方法，默认我们不定义就用父类中的。

```python
class Request(object):
    def __init__(self, req, xx):
        self._request = req
        self.xx = xx

    def __getattribute__(self, item):
        print("执行__getattribute__", item)
        return super().__getattribute__(item)


obj = Request(1, 2)
print(obj.xx)
print(obj._request)
# int(obj.v1) # 报错
# 注意：如果不是对象中的成员，就会报错。
```

不过想要访问对象中不存在成员，则可以通过定义 `__getattr__`实现。

- 先执行自己的 `__getattribute__`
- 再执行父类的`__getattribute__`
  - 是自己对象，直接获取并返回
  - 不是自己对象，调用`__getattr__`

```python
class Request(object):
    def __init__(self, req, xx):
        self._request = req
        self.xx = xx

    def __getattribute__(self, item):
        print("执行__getattribute__", item)
        return super().__getattribute__(item)

    def __getattr__(self, item):
        print("__getattr__", item)
        return 999


obj = Request(1, 2)
print(obj.xx)
print(obj._request)
print(obj.v1)
```



##### 2.对象封装

```python
class HttpRequest(object):
    def __init__(self):
        pass
    
    def v1(self):
        print("v1")
        
    def v2(self):
        print("v1")

class Request(object):
    def __init__(self,req, xx):
        self._request = req
        self.xx = xx

request = HttpRequest()
request.v1()
request.v2()

request = Request(request,111)
request._request.v1()
request._request.v2()
```

```python
class HttpRequest(object):
    def __init__(self):
        pass
    
    def v1(self):
        print("v1")
        
    def v2(self):
        print("v1")

class Request(object):
    def __init__(self,req, xx):
        self._request = req
        self.xx = xx
        
    def __getattr__(self, attr):
        try:
            return getattr(self._request, attr)
        except AttributeError:
            return self.__getattribute__(attr)
        
request = HttpRequest()
request.v1()
request.v2()

request = Request(request,111)
request.v1()
request.v2()
```



##### 3.源码分析

![请添加图片描述](https://img-blog.csdnimg.cn/direct/317c1586b88e40f0b50a5aca96e2e0f0.png)




##### 4.request对象

drf中的request其实是对请求的再次封装，其目的就是在原来的request对象基础中再进行封装一些drf中需要用到的值。

示例代码详见：`drf_demo-3.zip`

![请添加图片描述](https://img-blog.csdnimg.cn/direct/fac20f94936f49d5aadb0f86a9f89ef5.png)




### 3.3 认证

在开发API过程中，有些功能需要登录才能访问，有些无需登录。drf中的认证组件主要就是用来实现此功能。

关于认证组件，我们用案例的形式，先来学习常见的用用场景，然后再来剖析源码。



#### 3.3.1 案例1

> 项目要开发3个接口，其中1个无需登录接口、2个必须登录才能访问的接口。
>
> 示例代码详见：`drf_demo-4.zip`

![请添加图片描述](https://img-blog.csdnimg.cn/direct/219c567c87334014ad686108db717589.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/38a8dbaf3cb246c6938e4066da874a7b.png)


在浏览器上中访问：`/order/token=xxxdsfsdfdf`

认证组件中返回的两个值，分别赋值给：`request.user` 和 `request.auth`。



#### 3.3.2 案例2

> 项目要开发100个接口，其中1个无需登录接口、99个必须登录才能访问的接口。
>
> 此时，就需要用到drf的全局配置（认证组件的类不能放在视图view.py中，会因为导入APIView导致循环引用）。
>
> 示例代码详见：`drf_demo-5.zip`

![请添加图片描述](https://img-blog.csdnimg.cn/direct/432a22bc09914c2b94b2cdac1fcb6638.png)




#### 3.3.3 案例3

> 项目要开发100个接口，其中1个无需登录接口、98个必须登录才能访问的接口、1个公共接口（未登录时显示公共/已登录时显示个人信息）。
>
> 示例代码详见：`drf_demo-6.zip`

![请添加图片描述](https://img-blog.csdnimg.cn/direct/21a198583dde4cc9ba30ee508d86f518.png)




#### 3.3.4 案例4

> 项目要开发100个接口，其中1个无需登录接口、98个必须登录才能访问的接口、1个公共接口（未登录时显示公共/已登录时显示个人信息）。
>
> 原来的认证信息只能放在URL中传递，如果程序中支持放在很多地方，例如：URL中、请求头中等。
>
> 认证组件中，如果是使用了多个认证类，会按照顺序逐一执行其中的`authenticate`方法
>
> - 返回None或无返回值，表示继续执行后续的认证类
> - 返回   (user, auth) 元组，则不再继续并将值赋值给request.user和request.auth
> - 抛出异常 `AuthenticationFailed(...)`，认证失败，不再继续向后走。
>
> 示例代码详见：`drf_demo-7.zip`

![请添加图片描述](https://img-blog.csdnimg.cn/direct/ab31e68ebf7946ef9f05e5eb103cf379.png)




#### 3.3.5 源码分析

![请添加图片描述](https://img-blog.csdnimg.cn/direct/f2a9a47d032e4bfdb5fa5b9bbd8b8068.png)




### 3.4 权限

在drf开发中，如果有些接口必须同时满足：A条件、B条件、C条件。  有些接口只需要满足：B条件、C条件，此时就可以利用权限组件来编写这些条件。

- 且关系，默认支持：A条件 且 B条件 且 C条件，同时满足。

  ```python
  class PermissionA(BasePermission):
      message = {"code": 1003, 'data': "无权访问"}
  
      def has_permission(self, request, view):
          if request.user.role == 2:
              return True
          return False
  	
      # 暂时先这么写
      def has_object_permission(self, request, view, obj):
          return True
  ```

  

- 或关系，自定义（方便扩展）

  ```python
  class APIView(View):
  	def check_permissions(self, request):
          """
          Check if the request should be permitted.
          Raises an appropriate exception if the request is not permitted.
          """
          for permission in self.get_permissions():
              if not permission.has_permission(request, self):
                  self.permission_denied(
                      request,
                      message=getattr(permission, 'message', None),
                      code=getattr(permission, 'code', None)
                  )
  ```

  

#### 思考题：自定义request对象

如何在开发过程中自定义request对象?



### 3.5 限流

限流，限制用户访问频率，例如：用户1分钟最多访问100次 或者 短信验证码一天每天可以发送50次， 防止盗刷。

- 对于匿名用户，使用用户IP作为唯一标识。
- 对于登录用户，使用用户ID或名称作为唯一标识。



```python
缓存={
	用户标识：[12:33,12:32,12:31,12:30,12,]    1小时/5次   12:34   11:34
{
```

```
pip3 install django-redis
```

```python
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "qwe123",
        }
    }
}
```

![请添加图片描述](https://img-blog.csdnimg.cn/direct/49b24410f1594c6ba7362275734d805b.png)


```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "qwe123",
        }
    }
}
```

```python
from django.urls import path, re_path
from app01 import views

urlpatterns = [
    path('api/order/', views.OrderView.as_view()),
]
```

```python
# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache as default_cache


class ThrottledException(exceptions.APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 'throttled'


class MyRateThrottle(SimpleRateThrottle):
    cache = default_cache  # 访问记录存放在django的缓存中（需设置缓存）
    scope = "user"  # 构造缓存中的key
    cache_format = 'throttle_%(scope)s_%(ident)s'

    # 设置访问频率，例如：1分钟允许访问10次
    # 其他：'s', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day'
    THROTTLE_RATES = {"user": "10/m"}

    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk  # 用户ID
        else:
            ident = self.get_ident(request)  # 获取请求用户IP（去request中找请求头）

        # throttle_u # throttle_user_11.11.11.11ser_2

        return self.cache_format % {'scope': self.scope, 'ident': ident}

    def throttle_failure(self):
        wait = self.wait()
        detail = {
            "code": 1005,
            "data": "访问频率限制",
            'detail': "需等待{}s才能访问".format(int(wait))
        }
        raise ThrottledException(detail)


class OrderView(APIView):
    throttle_classes = [MyRateThrottle, ]

    def get(self, request):
        return Response({"code": 0, "data": "数据..."})
```



**多个限流类**

本质，每个限流的类中都有一个 `allow_request` 方法，此方法内部可以有三种情况：

- 返回True，表示当前限流类允许访问，继续执行后续的限流类。
- 返回False，表示当前限流类不允许访问，继续执行后续的限流类。所有的限流类执行完毕后，读取所有不允许的限流，并计算还需等待的时间。
- 抛出异常，表示当前限流类不允许访问，后续限流类不再执行。



**全局配置**

```python
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES":["xxx.xxx.xx.限流类", ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "10/m",
        "xx":"100/h"
    }
}
```

**底层源码实现：**

![请添加图片描述](https://img-blog.csdnimg.cn/direct/4000753efc3743ebaf201dc6a7cf8596.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/186c66e85b5f4034bfb27b80fbc4e166.png)




### 3.6 版本

在restful规范中要去，后端的API中需要体现版本。



#### 3.1 URL的GET参数传递（*）

![请添加图片描述](https://img-blog.csdnimg.cn/direct/9dbbf5d84fd04fbfa4a3138f25402f35.png)


```python
# settings.py

REST_FRAMEWORK = {
    "VERSION_PARAM": "v",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2", "v3"],
    "DEFAULT_VERSIONING_CLASS":"rest_framework.versioning.QueryParameterVersioning"
}
```

源码执行流程：

![请添加图片描述](https://img-blog.csdnimg.cn/direct/dc991322bcbf4398a918a59609d01c90.png)




#### 3.2 URL路径传递（*）

![请添加图片描述](https://img-blog.csdnimg.cn/direct/22650217f34e41aab1dba8d5f0ebfc12.png)




















#### 3.3 请求头传递

![请添加图片描述](https://img-blog.csdnimg.cn/direct/3e34a8cc8bb34251b15c69f2d22bc9f1.png)






**全局配置**

上述示例中，如果想要应用某种 版本 的形式，需要在每个视图类中定义类变量：

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import QueryParameterVersioning


class UserView(APIView):
    versioning_class = QueryParameterVersioning
    ...
```

如果你项目比较大，需要些很多的视图类，在每一个类中都写一遍会比较麻烦，所有drf中也支持了全局配置。

```python
# settings.py

REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning",  # 处理版本的类的路径
    "VERSION_PARAM": "version",  # URL参数传参时的key，例如：xxxx?version=v1
    "ALLOWED_VERSIONS": ["v1", "v2", "v3"],  # 限制支持的版本，None表示无限制
    "DEFAULT_VERSION": "v1",  # 默认版本
}
```

![请添加图片描述](https://img-blog.csdnimg.cn/direct/3dbfab51dcc44d03a973f88aa7d71330.png)


访问URL：

````
http://127.0.0.1:8000/api/users/?version=v1
http://127.0.0.1:8000/api/users/?version=v2
http://127.0.0.1:8000/api/users/?version=v3

http://127.0.0.1:8000/api/admin/?version=v1
http://127.0.0.1:8000/api/admin/?version=v2
http://127.0.0.1:8000/api/admin/?version=v3

http://127.0.0.1:8000/api/v1/order/
http://127.0.0.1:8000/api/v2/order/
http://127.0.0.1:8000/api/v3/order/
````



**底层源码实现**

![请添加图片描述](https://img-blog.csdnimg.cn/direct/5d97577467644429998fa0a2606c4f8d.png)




**反向生成URL**

在每个版本处理的类中还定义了`reverse`方法，他是用来反向生成URL并携带相关的的版本信息用的，例如：

![请添加图片描述](https://img-blog.csdnimg.cn/direct/5ca5c489e3bf499e9feb5ee743a47814.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/77ca0f48cf6b405080b4a13d3f8e56ec.png)




### 3.7 解析器

之前使用 `request.data` 获取请求体中的数据。

这个 `reqeust.data` 的数据怎么来的呢？其实在drf内部是由解析器，根据请求者传入的数据格式 + 请求头来进行处理。

#### 3.7.1 JSONParser （*）

![请添加图片描述](https://img-blog.csdnimg.cn/direct/5c694395db054dabaa5b55879ccfb3e8.png)




#### 3.7.2 FormParser

![请添加图片描述](https://img-blog.csdnimg.cn/direct/c71b2ff7f5694a8ebc8b540340acb377.png)




#### 3.7.3 MultiPartParser（*）

![请添加图片描述](https://img-blog.csdnimg.cn/direct/70b5bbb3f4c34f90865736b0c3d0b14c.png)


```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form action="http://127.0.0.1:8000/test/" method="post" enctype="multipart/form-data">
    <input type="text" name="user" />
    <input type="file" name="img">

    <input type="submit" value="提交">

</form>
</body>
</html>
```



#### 3.7.4 FileUploadParser（*）

![请添加图片描述](https://img-blog.csdnimg.cn/direct/1635dc08472f4920bdbba5913c34bd11.png)




解析器可以设置多个，默认解析器：

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

class UserView(APIView):

    def post(self, request):
        print(request.content_type)
        print(request.data)

        return Response("...")

```

 







### 3.8 Serializer（*）

drf中为我们提供了Serializer，他主要有两大功能：

- 对请求数据校验（底层调用Django的Form和ModelForm）
- 对数据库查询到的对象进行序列化



#### 3.8.1 数据校验

示例1：基于Serializer：

![请添加图片描述](https://img-blog.csdnimg.cn/direct/2a01b3f172db463c9ffee091bb2cc323.png)




示例2：基于ModelSerializer：

```python
# models.py

from django.db import models


class Role(models.Model):
    """ 角色表 """
    title = models.CharField(verbose_name="名称", max_length=32)


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="名称", max_length=32)


class UserInfo(models.Model):
    """ 用户表 """
    level_choices = ((1, "普通会员"), (2, "VIP"), (3, "SVIP"),)
    level = models.IntegerField(verbose_name="级别", choices=level_choices, default=1)

    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄", default=0)
    email = models.CharField(verbose_name="邮箱", max_length=64)
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)

    # 外键
    depart = models.ForeignKey(verbose_name="部门", to="Department", on_delete=models.CASCADE)
    
    # 多对多
    roles = models.ManyToManyField(verbose_name="角色", to="Role")

```

![请添加图片描述](https://img-blog.csdnimg.cn/direct/552e5ef50fa448cc9fcba2b016b9fce9.png)


*提示：save方法会返回新生成的数据对象。*



示例3：基于ModelSerializer（含FK+M2M）：

![请添加图片描述](https://img-blog.csdnimg.cn/direct/06c5ad7d3c674063a50199596e56c47c.png)


*提示：save方法会返回新生成的数据对象。*







#### 3.8.2 序列化

通过ORM从数据库获取到的 QuerySet 或 对象 均可以被序列化为 json 格式数据。

```python
# models.py

from django.db import models


class Role(models.Model):
    """ 角色表 """
    title = models.CharField(verbose_name="名称", max_length=32)


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="名称", max_length=32)


class UserInfo(models.Model):
    """ 用户表 """
    level_choices = ((1, "普通会员"), (2, "VIP"), (3, "SVIP"),)
    level = models.IntegerField(verbose_name="级别", choices=level_choices, default=1)

    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄", default=0)
    email = models.CharField(verbose_name="邮箱", max_length=64, null=True, blank=True)
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)

    depart = models.ForeignKey(verbose_name="部门", to="Department", on_delete=models.CASCADE, null=True, blank=True)
    roles = models.ManyToManyField(verbose_name="角色", to="Role")
```



示例1：序列化基本字段

![请添加图片描述](https://img-blog.csdnimg.cn/direct/ff3989a2ee9440b4aa069f72f704f389.png)


```python
# 切记， 如果从数据库获取的不是QuerySet对象，而是单一对象，例如：
data_object = modes.UserInfo.objects.filter(id=2).first()
ser = UserModelSerializer(instance=data_object,many=False)
print(ser.data)
```





示例2：自定义字段

![请添加图片描述](https://img-blog.csdnimg.cn/direct/9d66f8cfc26a4b5080a6072413b10cb4.png)




示例3：序列化类的嵌套

![请添加图片描述](https://img-blog.csdnimg.cn/direct/308c546a083146ee8206bcd06a8697b2.png)




#### 3.8.3 数据校验&序列化

上述示例均属于单一功能（要么校验，要么序列化），其实当我们编写一个序列化类既可以做数据校验，也可以做序列化，例如：

![请添加图片描述](https://img-blog.csdnimg.cn/direct/db61770a12a44e90bf547a1d09456a17.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/88212b64560040fba6326c75797e008b.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/8eca4055b04f46c1ba1a53708dfed784.png)




```python
# models.py

from django.db import models


class Role(models.Model):
    """ 角色表 """
    title = models.CharField(verbose_name="名称", max_length=32)


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="名称", max_length=32)


class UserInfo(models.Model):
    """ 用户表 """
    level_choices = ((1, "普通会员"), (2, "VIP"), (3, "SVIP"),)
    level = models.IntegerField(verbose_name="级别", choices=level_choices, default=1)

    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄", default=0)
    email = models.CharField(verbose_name="邮箱", max_length=64, null=True, blank=True)
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)

    depart = models.ForeignKey(verbose_name="部门", to="Department", on_delete=models.CASCADE, null=True, blank=True)
    roles = models.ManyToManyField(verbose_name="角色", to="Role")

```



```python
# urls.py

from django.urls import path, re_path, include
from app01 import views

urlpatterns = [
    path('api/users/', views.UserView.as_view()),
]

```

```python
# views.py

from django.core.validators import EmailValidator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from app01 import models


class DepartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = ['id', "title"]
        extra_kwargs = {
            "id": {"read_only": False},  # 数据验证
            "title": {"read_only": True}  # 序列化
        }


class RoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ['id', "title"]
        extra_kwargs = {
            "id": {"read_only": False},  # 数据验证
            "title": {"read_only": True}  # 序列化
        }


class UserModelSerializer(serializers.ModelSerializer):
    level_text = serializers.CharField(source="get_level_display", read_only=True)

    # Serializer嵌套，不是read_only，一定要自定义create和update，自定义新增和更新的逻辑。
    depart = DepartModelSerializer(many=False)
    roles = RoleModelSerializer(many=True)

    extra = serializers.SerializerMethodField(read_only=True)
    email2 = serializers.EmailField(write_only=True)

    # 数据校验：username、email、email2、部门、角色信息
    class Meta:
        model = models.UserInfo
        fields = [
            "username", "age", "email", "level_text", "depart", "roles", "extra", "email2"
        ]
        extra_kwargs = {
            "age": {"read_only": True},
            "email": {"validators": [EmailValidator, ]},
        }

    def get_extra(self, obj):
        return 666

    def validate_username(self, value):
        return value

    # 新增加数据时
    def create(self, validated_data):
        """ 如果有嵌套的Serializer，在进行数据校验时，只有两种选择：
              1. 将嵌套的序列化设置成 read_only
              2. 自定义create和update方法，自定义新建和更新的逻辑
            注意：用户端提交数据的格式。
        """
        depart_id = validated_data.pop('depart')['id']

        role_id_list = [ele['id'] for ele in validated_data.pop('roles')]

        # 新增用户表
        validated_data['depart_id'] = depart_id
        user_object = models.UserInfo.objects.create(**validated_data)

        # 在用户表和角色表的关联表中添加对应关系
        user_object.roles.add(*role_id_list)

        return user_object


class UserView(APIView):
    """ 用户管理 """

    def get(self, request):
        """ 添加用户 """
        queryset = models.UserInfo.objects.all()
        ser = UserModelSerializer(instance=queryset, many=True)
        return Response({"code": 0, 'data': ser.data})

    def post(self, request):
        """ 添加用户 """
        ser = UserModelSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 1006, 'data': ser.errors})

        ser.validated_data.pop('email2')

        instance = ser.save(age=18, password="123", depart_id=1)

        # 新增之后的一个对象（内部调用UserModelSerializer进行序列化）
        print(instance)
        # ser = UserModelSerializer(instance=instance, many=False)
        # ser.data

        return Response({'code': 0, 'data': ser.data})

```



**底层源码实现：**

序列化的底层源码实现有别于上述其他的组件，序列化器相关类的定义和执行都是在视图中被调用的，所以源码的分析过程可以分为：定义类、序列化、数据校验。

源码1：序列化过程

![请添加图片描述](https://img-blog.csdnimg.cn/direct/76a66c5ad78c43c697bcd34e753c503b.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/4eaa5c8ca2fc4188bdc1754510151f37.png)


源码2：数据校验过程

![请添加图片描述](https://img-blog.csdnimg.cn/direct/204c098c770640fb96fde472e47b5154.png)


![请添加图片描述](https://img-blog.csdnimg.cn/direct/ad7ab83026e447d38bb56de58fc91d73.png)