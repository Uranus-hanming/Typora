import asyncio


# 协程任务1
async def work_1():
	for _ in range(5):
		print('我是协程任务1...')
		await asyncio.sleep(1)


# 协程任务1
async def work_2():
	for _ in range(5):
		print('我是协程任务2...')
		await asyncio.sleep(1)

# 将当前的协程函数转为协程对象，并把多个协程对象添加到一个列表中
tasks = [
	work_1(),
	work_2()
]




# 使用asyncio创建一个事件循环对象
# loop = asyncio.get_event_loop()

# 使用事件循环对象调度执行多个协程任务
# loop.run_until_complete(asyncio.wait(tasks))


"""
1.需要使用asyncio创建事件循环对象
2.使用事件循环对象执行多个协程任务
"""


# 使用python3.7以上版本语法运行多个任务
asyncio.run(asyncio.wait(tasks))






