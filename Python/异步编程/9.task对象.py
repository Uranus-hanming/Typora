# -*- coding: utf-8 -*-

"""
@author: 顾安
@software: PyCharm
@file: 9.task对象.py
@time: 2023/5/18 下午9:03
"""


import asyncio


async def other():
    print('协程任务启动...')
    await asyncio.sleep(5)
    print('协程任务完成...')
    return '这是当前协程任务的返回值...'


async def main():
    print('正在执行协程任务函数: other...')

    task_1 = asyncio.create_task(other())
    task_2 = asyncio.create_task(other())
    '''
    因为await必须要等待res_1拿到返回值 
        在当前res_1任务运行期间 主程序代码是堵塞的
            没有办法在同一时间将res_2提交到事件循环
    '''
    # res_1 = await other()
    # res_2 = await other()

    res_1 = await task_1
    res_2 = await task_2
    print('当前协程任务的返回值为: ', res_1, res_2)


asyncio.run(main())
