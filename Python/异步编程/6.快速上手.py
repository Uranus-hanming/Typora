"""
协程函数
	使用async关键字定义的函数

协程对象
	协程函数()会返回一个协程对象，可以使用事件循环去调度协程对象
"""

import asyncio


async def work():
	print('运行协程任务...')


# python 3.6版本
# loop = asyncio.get_event_loop()
# loop.run_until_complete(work())


# python3.7以上版本
# async def main():
# 	task = [
# 		asyncio.create_task(work())
# 	]
# 	await asyncio.wait(task)

task = [
	work()
]

asyncio.run(asyncio.wait(task))


