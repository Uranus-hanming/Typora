# -*- coding: utf-8 -*-

"""
@author: 顾安
@software: PyCharm
@file: 8.协程嵌套.py
@time: 2023/5/18 下午8:53
"""


import asyncio


async def other():
    print('协程任务启动...')
    await asyncio.sleep(2)
    print('协程任务完成...')
    return '这是当前协程任务的返回值...'


async def main():
    print('正在执行协程任务函数: other...')
    res_1 = await other()
    res_2 = await other()
    print('当前协程任务的返回值为: ', res_1, res_2)


asyncio.run(main())

