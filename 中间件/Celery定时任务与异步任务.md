[toc]
##### Celery

- 作用：使用celery来实现异步任务和定时任务

##### 組成模塊

- 任務模塊

  - 异步任务（不会阻塞当前主程序的運行）：异步任务（Async Task）通常在业务逻辑中被触发，并被发往任务队列；
  - 定时任务：定时任务由celery beat进程周期性地将任务发往任务队列。

- 消息中間件broker

  > broker，即为任务调度队列，接收任务生产者发来的任务消息，将任务存入队列。celery本身不提供任务队列，推荐使用RabbitMQ和Redis。

- 任務執行單元worker

  >worker实时监控消息队列，获取调度的任务，并执行。

- 任務結果存儲backend

  > backend用于存储任务的执行结果，同消息中间件一样，存储可使用RabbitMQ，Redis，MongoDB等。

##### 異步任務

> 使用celery实现异步任务主要包括三个步骤：
>
> - **创建一个celery实例**
> - **启动celery worker**
> - **程序调用异步任务**

- celery_app/\__init__.py文件

```python
from celery import Celery

# 创建celery实例
app = Celery('demo')
 
# 通过celery实例加载配置模块
app.config_from_object('celery_app.celeryconfig')
```

- celery_app/celeryconfig.py

```python
# 指定broker
BROKER_URL = 'redis://127.0.0.1:6379'
# 指定backend
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
 
# 指定时区
CELERY_TIMEZONE = 'Asia/Shanghai'
 
# 指定导入的任务模块
CELERY_IMPORTS = (
    'celery_app.task1',
    'celery_app.task2'
)
```

- celery_app/task1.py

```python
import time
from celery_app import app
 
@app.task
def add(x,y):
    time.sleep(2)
    return x+y
```

- celery_app/task2.py

```python
import time
from celery_app import app
 
@app.task
def multiply(x,y):
    time.sleep(2)
    return x*y
```

- client.py文件

```python
import time
from celery_app import task1
from celery_app import task2
 
 
print('开始', time.ctime())
task1.add.delay(2,3) # delay是apply_async的快捷方式
task2.multiply.apply_async(args=[2,3])
 
print('完成', time.ctime())
```

- 啟動worker進程

```shell
在当前目录下，使用如下方式启动celery worker
linux:celery worker -A celery_app --loglevel=info
	参数-A指定了celery实例的位置，这里是task.py中，celery会自动在该文件中寻找celery实例对象，当然也可以直接指定为-A task.app;
	参数--loglevel指定了日志级别，默认为warning，也可以使用-l info来表示；
window:celery worker -A celery_app -l info -P eventlet
```

- 程序調用異步任務

> 执行python命令运行client.py文件。

##### django中实现定时任务

> celery beat进程通过读取配置文件的内容，周期性地将定时任务发往任务队列。

###### 基本配置

1. 安装依赖包

   ```go
   pip install celery django-celery-beat django-celery-results redis
   ```

2. settings.py

   ```go
   INSTALLED_APPS = [
       'django_celery_beat',
       'django_celery_results',
   ]
   
   # Celery配置
   CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'  # 使用Redis作为消息代理
   CELERY_RESULT_BACKEND = 'django-db'  # 使用数据库存储任务结果
   CELERY_TIMEZONE = 'Asia/Shanghai'  # 设置时区
   DJANGO_CELERY_BEAT_TZ_AWARE = False  # 关闭时区感知
   CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'  # 使用数据库调度器
   
   # 定时任务配置
   CELERY_BEAT_SCHEDULE = {
       'get_tapd_data': {
           'task': 'mainapp.tapd.tasks.tapd_task',
           'schedule': 100,  # 每天执行（单位：秒）
       }
   }
   ```

3. 创建celery实例

   ```python
   # myproject/celery.py
   
   import os
   from celery import Celery
   from django.conf import settings
   
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
   
   app = Celery('myproject')
   
   # 从Django配置文件中读取Celery配置
   app.config_from_object('django.conf:settings', namespace='CELERY')
   
   # 自动发现所有Django应用中的tasks.py文件
   app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
   ```

4. 初始化项目文件（init.py）

   ```python
   # myproject/__init__.py
   
   from .celery import app as celery_app
   
   __all__ = ('celery_app',)
   ```

5. 编写定时任务（myapp/tasks.py）

   ```python
   # myapp/tasks.py
   
   from celery import shared_task
   import time
   
   @shared_task
   def send_daily_emails():
       """示例任务：每天发送邮件"""
       print("开始发送每日邮件...")
       time.sleep(5)  # 模拟耗时操作
       print("邮件发送完成！")
       return "已发送所有每日邮件"
   
   @shared_task
   def clear_temp_data():
       """示例任务：每小时清理临时数据"""
       print("清理临时数据中...")
       return "临时数据已清理"
   ```

6. 数据库表迁移

   ```python
   python manage.py migrate
   ```

###### 项目部署配置

1. docker-compose.py

   ```yaml
   version: '3'
   
   services:
     django:
       build: .
       container_name: myproject
       command: python manage.py runserver 0.0.0.0:8080
       volumes:
         - .:/home/myproject
       ports:
         - "8080:8080"
       depends_on:
         - db
         - redis
       environment:
         - MYSQL_DATABASE=myproject
         - MYSQL_USER=root
         - MYSQL_PASSWORD=123456
         - MYSQL_ROOT_PASSWORD=123456
         - MYSQL_PORT=13306
         - MYSQL_HOST=127.0.0.1
         - REDIS_HOST=127.0.0.1
         - DEBUG=False
       restart: always
   
     db:
       image: mysql:latest
       container_name: myproject_db
       environment:
         - MYSQL_DATABASE=myproject
         - MYSQL_ROOT_PASSWORD=123456
       ports:
         - "13306:3306"
       volumes:
         - /home/db_data:/var/lib/mysql  # 将本地目录挂载到容器的初始化脚本目录
       restart: always
   
     redis:
       image: redis:latest
       container_name: redis
       ports:
         - "6379:6379"
       networks:
         - backend
       healthcheck:
         test: [ "CMD", "redis-cli", "ping" ]
         interval: 5s
         timeout: 3s
         retries: 3
   
     celery_worker:
       build: .
       container_name: worker
       command: bash start-celery-worker.sh
       volumes:
         - .:/app
       depends_on:
         - redis
         - django
       environment:
         - MYSQL_DATABASE=myproject
         - MYSQL_USER=root
         - MYSQL_PASSWORD=123456
         - MYSQL_ROOT_PASSWORD=123456
         - MYSQL_PORT=13306
         - MYSQL_HOST=127.0.0.1
         - REDIS_HOST=127.0.0.1
         - DEBUG=False
       networks:
         - backend
       restart: unless-stopped
       healthcheck:
         test: [ "CMD", "celery", "-A", "config", "inspect", "ping" ]
         interval: 30s
         timeout: 10s
         retries: 3
   
     celery_beat:
       build: .
       container_name: beat
       command: bash start-celery-beat.sh
       volumes:
         - .:/app
       depends_on:
         - redis
         - django
       environment:
         - MYSQL_DATABASE=myproject
         - MYSQL_USER=root
         - MYSQL_PASSWORD=123456
         - MYSQL_ROOT_PASSWORD=123456
         - MYSQL_PORT=13306
         - MYSQL_HOST=127.0.0.1
         - REDIS_HOST=127.0.0.1
         - DEBUG=False
       networks:
         - backend
       restart: unless-stopped
   
   networks:
     backend:
       driver: bridge
   ```

2. start-celery-worker.sh

   ```shell
   #!/bin/sh
   
   # 等待依赖服务就绪
   while ! nc -z log_redis 6379; do
     echo "等待Redis启动..."
     sleep 1
   done
   
   echo "启动Celery Worker..."
   exec celery -A myproject worker \
     --loglevel=info \
     --concurrency=4 \
     --hostname=worker@%h
   ```

3. bash start-celery-beat.sh

   ```shell
   #!/bin/sh
   
   # 等待依赖服务就绪
   while ! nc -z log_redis 6379; do
     echo "等待Redis启动..."
     sleep 1
   done
   
   echo "启动Celery Beat..."
   exec celery -A myproject beat \
     --loglevel=info \
     --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```



##### django-celery-beat

> 实现定时任务的动态操作（添加/删除）等，此插件本质是对数据库表变化做 检查，一旦有数据库表改变，调度器重新读取任务进行调度

- django_celery_results

  >用于在数据库中存储 Celery 任务执行的结果。

- django_celery_beat

  > 用于在数据库中记录预先定义好的任务执行规则（比如每隔一分钟执行一次），以及与这些规则关联的待执行的具体任务。

- 運行腳本

  ```shell
  windows
  django-admin startproject project_name
  # 数据库迁移，创建超级用户：
  $ python manage.py migrate
  $ python manage.py createsuperuser
  # 啟動服務
  # 配置 ALLOWED_HOSTS = ['*']
  python manage.py runserver ip:port
  # 啟動celery worker
  #Celery Worker 负责执行由 Beat 传过来的任务，输出执行结果并将结果保存至 result backend（即数据库）
  celery -A celerytest worker -l info -P eventlet
  # 啟動celery beat 
  # Celery Beat 持续监测数据库中存储的计划任务信息，将满足触发条件的任务传递给 Celery Worker 执行
  celery beat -A celerytest -l info --pidfile=
  celery -A celerytest beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --pidfile=
  ```

- PERIODIC TASKS

  > 下面则是由 `django_celery_beat` 创建的用于保存 Celery 任务及其执行规则的几张数据库表

  - Clocked：定义在具体某个时间点触发的执行规则
  - Crontabs：类似于 Linux 系统下 crontab 的语法
  - Intervals：定义任务重复执行的时间间隔
  - Periodic tasks：具体某个待执行的任务，需要与其他表（Clocked、Crontabs、Intervals、Solar events）中定义的执行规则相关联
  - Solar events：根据日升和日落等太阳运行轨迹确定执行规则