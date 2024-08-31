import time
import asyncio


now = lambda: time.time()
start = now()

# 协程函数
async def func(i):
	asyncio.sleep(1)
	print(i)

for i in range(5):
	asyncio.run(func(i))

print(f'当前异步程序所花费的时间为: {now() - start}')
