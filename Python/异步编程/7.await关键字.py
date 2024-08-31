import asyncio


async def work():
    await asyncio.sleep(3)
    return '这是一个协程任务...'


async def main():
    res = await work()  # 如果当前任务是一个耗时任务 则会阻塞当前代码
    print(1)
    print(res)


asyncio.run(main())
