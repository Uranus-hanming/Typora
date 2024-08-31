# -*- coding: utf-8 -*-

"""
@author: 顾安
@software: PyCharm
@file: 10.协程并发.py
@time: 2023/5/18 下午9:29
"""


import asyncio


async def work(x):
    print('当前接受的参数为: ', x)
    # 模拟一个耗时任务
    await asyncio.sleep(x)
    return f'当前任务的返回值为: {x}'


async def main():
    # 创建十个任务并将十个任务提交到事件循环
    tasks = [asyncio.create_task(work(i)) for i in range(10)]

    # wait方法获取的返回值是无序的
    # done, pending = await asyncio.wait(tasks)
    # for item in done:
    #     print(item.result())

    # gather用来收集所有已完成的任务的返回值 并且获取到的任务的返回值是有顺序的
    res = await asyncio.gather(*tasks)
    print(res)

asyncio.run(main())
