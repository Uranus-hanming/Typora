[toc]
#### 多线程开发

1. 一个进程中可以包含多个线程
2.  线程也是一个运行行为，消耗计算机资源
3.  一个进程中的所有线程共享这个进程的资源
4.  多个线程之间的运行互不影响各自运行
5.  线程的创建和销毁消耗资源远小于进程
6.  各个线程也有自己的ID等特征

##### 1. Thread创建多线程

```python
import time
from threading import Thread


def count(x):
    time.sleep(x)


start = time.time()

jobs = []
for i in range(5):
    t = Thread(target=count, args=(i,))
    jobs.append(t)
    t.start()

for i in jobs:
    i.join()

print("用时：", time.time() - start)
```

##### 2. ThreadPoolExecutor创建进程池

```python
from concurrent.futures import ThreadPoolExecutor
import time

# 构造线程池实例，传入max_workers可以设置线程池中最多能同时运行的线程数目
pool = ThreadPoolExecutor(max_workers=2)

def task(i):
    print('线程名称：%s' % i)
    time.sleep(2)  # 定义睡眠时间
    
for i in range(5):  # 创建十个任务
    # submit() 提交线程需要执行的任务（函数名和参数）到线程池中，立刻返回一个future对象。
    future1 = pool.submit(task, i)
    # 取task的执行结果
    print(future1.result())
    # 取消该 Future 代表的线程任务。如果该任务正在执行，不可取消，则该方法返回 False；否则，程序会取消该任务，并返回 True。
    print(future1.cancel())
    # 返回 Future 代表的线程任务是否被成功取消。
    print(future1.cancelled())
    print(future1.running())
```

###### as_completed()

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
import threading

# 构造线程池实例，传入max_workers可以设置线程池中最多能同时运行的线程数目
pool = ThreadPoolExecutor(max_workers=2)


# def task(i):
#     print('线程名称：%s' % i)
#     time.sleep(2)  # 定义睡眠时间

def task(i):
    sleep_seconds = random.randint(1, 3)  # 随机睡眠时间
    print('线程名称：%s，参数：%s，睡眠时间：%s' % (threading.current_thread().name, i, sleep_seconds))
    time.sleep(sleep_seconds)  # 定义睡眠时间


all_task = [pool.submit(task, i) for i in range(5)]

for future in as_completed(all_task):
    data = future.result()
    print(data)
```

###### map()

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
import threading

# 构造线程池实例，传入max_workers可以设置线程池中最多能同时运行的线程数目
pool = ThreadPoolExecutor(max_workers=2)


# def task(i):
#     print('线程名称：%s' % i)
#     time.sleep(2)  # 定义睡眠时间

def task(i):
    sleep_seconds = random.randint(1, 3)  # 随机睡眠时间
    print('线程名称：%s，参数：%s，睡眠时间：%s' % (threading.current_thread().name, i, sleep_seconds))
    time.sleep(sleep_seconds)  # 定义睡眠时间


# 向线程池提交5个任务
x = range(5)
for i in pool.map(task, x):
    print('successful')
```