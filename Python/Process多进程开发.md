[toc]

#### 多进程开发

##### 1. Process创建多进程 

```python
import time
import multiprocessing


def worker():
    sum = 0
    for i in range(100000):
        sum += 1

    print(sum)


if __name__ == '__main__':
    start = time.time()
    jobs = []
    for i in range(6):
        p = multiprocessing.Process(target=worker)
        p.start()
        jobs.append(p)
    for p in jobs:
        p.join()

    end = time.time()
    print(end - start)
```

##### 2. 进程池Pool创建多进程

> 创建一定数量的进程来处理事件，事件处理完进 程不退出而是继续处理其他事件，直到所有事件全都处理完毕统一销毁。增加进程的重复利用，降低资源消耗。

1. 进程的创建和销毁过程消耗的资源较多
2. 当任务量众多，每个任务在很短时间内完成时，需要频繁的创建和销毁进程。此时对计算机压力较大
3. 进程池技术很好的解决了以上问题。

```python
from multiprocessing import Pool
import os
import time
import random


def worker(msg):
    t_start = time.time()
    print("%s开始执行,进程号为%d" % (msg, os.getpid()))
    # random.random()随机生成0~1之间的浮点数
    time.sleep(random.random() * 2)
    t_stop = time.time()
    print(msg, "执行完毕，耗时%0.2f" % (t_stop - t_start))


if __name__ == "__main__":
    po = Pool(3)  # 定义一个进程池，最大进程数3
    for i in range(0, 8):
        # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
        # 每次循环将会用空闲出来的子进程去调用目标
        po.apply_async(worker, (i,))

    print("----start----")
    # 关闭进程池，关闭后po不再接收新的请求
    po.close()
    # 等待po中所有子进程执行完成，必须放在close语句之后
    po.join()
    print("-----end-----")
```