asyncio 的运算核心：event loop
	他面对很多可以执行的任务，然后决定执行哪个任务
coroutine: 
	coroutine function
	coroutine object
	如何运行coroutine代码：
		第一，进入async模式，即进入event loop开始控制整个程序的状态
			使用一个入口函数: asyncio.run
				asyncio.run的参数是coroutine，第一他会建立起event loop，第二他会把这个coroutine变成event loop里面的第一个task
				event loop 建立之后他会去找哪个task可以执行；
				event loop 的核心是他有很多个task,然后他来决定哪个task要运行
		第二，把coroutine变成task
			把coroutine变成task，让他可以排队执行的办法:
				1.使用await
					await coroutine 时发生了如下几件事：
						第一，这个coroutine被包装成一个task,并且被告诉了event loop说这里有一个新的task;
						第二，他会告诉event loop，我现在这个task需要等到这个say_after task 完成之后我才能继续
						第三，他会yield出去，即他会告诉event loop 当前的task阻塞了，所以先让别的task执行，最后当event loop再次安排当前task运行时，当前task会把
						say_after这个coroutine里面真正的返回值拿出来保存起来
				2. 使用asyncio.create_task()
					create_task 函数会把 coroutine 变成一个task, 并且把这个task注册到event loop 里面
				3. 使用asyncio.gather()
					如果参数是coroutine,gather首先会把它包装成task,并且注册到event loop.然后它会返回一个future值，当 await 这个future的时候，
					相当于告诉event loop 我要等待这里面每一个task都完成才可以继续，同时会把这些task的return值放到一个list里返回。
					并且这个list的顺序和里面 task 的顺序是一致的。
task: 
python 运行的单进程单线程的程序，所以同时执行的任务只有一个，不存在系统级的上下文切换，即asyncio并不能提升你的运算速度，比较适合处理那些需要等待的任务，典型的如网络通讯

import asyncio
import time


async def say_after(delay, what):
    # asyncio.sleep() 返回的是coroutine object
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"started at {time.strftime('%X')}")

    # say_after() 返回的是 coroutine object
    # await coroutine 时发生了如下几件事：
    # 第一，这个coroutine被包装成一个task,并且被告诉了event loop说这里有一个新的task;
    # 第二，他会告诉event loop，我现在这个task需要等到这个say_after task 完成之后我才能继续
    # 第三，他会yield出去，即他会告诉event loop 当前的task阻塞了，所以先让别的task执行，最后当event loop再次安排当前task运行时，当前task会把
    # say_after这个coroutine里面真正的返回值拿出来保存起来
    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")


# 首先asyncio.run把main()作为一个task给放到了event loop, event loop去寻找task发现只有一个task main()
# 然后就开始让这个task main() 运行main(), main在运行的时候首先print了一个start at
# 然后他运行了 say_after() 这个 coroutine function 得到一个coroutine object, await 这个 coroutine object 把这个 coroutine object
# 变成一个 task 放回了 event loop 里，同时告诉 event loop 我需要等待他，然后把控制权交还给了 event loop , 现在 event loop
# 里面有两个 task , 一个是 main, 一个是 say_after , 但是main运行不了，因为他要等say_after, 所以 event loop 就让 say_after
# 先运行，say_after里面做了一个很相似的事情，asyncio.sleep 也是一个 coroutine , say_after 也是把他变成一个 task, 然后告诉
# event loop 说，我得等这个sleep完成了我才能运行，然后他前面的 await 又把这个控制权转回了 event loop，event loop 现在就有了
# 三个 task ，即 main、say_after、sleep , sleep 会告诉event loop一秒钟之后就好了，所以event loop 就等了一秒钟，等sleep好了之后
# 现在 event loop 还有两个 task, 即 main、say_after，这个main要等say_after，但是这时say_after等的东西已经完成了，于是
# event loop 就让say_after先运行，接着say_after print 一个 hello, 然后 say_after也完成了，于是又把控制权交还给了 event loop
# 此时event loop 只有一个task即main, 然后就把控制权给main, 这个时候main就把第一个say_after完成了，然后再做第二个say_after
# 做同样的事又等了2秒之后完成，所以整个过程用了3秒。
# 所有的控制权的返回都是显示的，即 event loop 并没有办法强行从一个task里边拿回控制权，必须要这个task主动把控制权交回去，交回去的方法
# 有两种，第一个是 await 会交回，第二个是当这个函数运行完毕之后会交回。如果task里面有个死循环，则整个event loop就卡死了。
# 这里还是要等3秒，原因是直接用await把一个coroutine变成task所遇到的问题，因为await需要做的事太多了，他要变成task，变成task之后会主动把控制权交出去
# 还是要等，这样后面的代码必须要等到他完成之后才能变成一个task才能被征召被翻牌。
# 为了解决这个问题，asyncio提供了 create_task 函数，这个函数的参数也是一个 coroutine ，即create_task调用之后返回的是coroutine, 他不会运行任何coroutine里面的代码
# create_task 函数会把 coroutine 变成一个task, 并且把这个task注册到event loop 里面，所以create_task函数分摊了 await coroutine 的一部分功能。
# create_task 函数把 coroutine 变成一个task并不能马上执行这个task, 因为控制权还在main手里，此时main趁着自己手里有控制权，他就往下执行做了task2。
# task2也是告诉main 这还有一个新的task 。在这之后才开始 await task1 await task2 。
# await 后面是一个 coroutine 的时候，他有的功能是把coroutine变成一个task，然后把控制权交还，然后等他拿返回值。
# 当await后面是一个task而不是一个coroutine的时候，他就省略了把coroutine变成task这一步，他就只是告诉event loop我需要这个task完成，我把控制权交还给你，并且在控制权回来的时候，从这个task里面提取所需要的返回值。
#
asyncio.run(main())


##################### create_task ####################

async def say_after(delay, what):
    # asyncio.sleep() 返回的是coroutine object
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # 这个程序只用了两秒钟，因为当他在await task1的时候，event loop里面实际上已经有了三个task: main task1 task2,
    # 当task1跟event loop说我要等一秒钟才能完成之后，event loop 就会去执行task2, task2说他要2秒才能结束，这样两个task就可以同时进行等待了。
    # 这也就是为什么async很适合解决一些网络通讯的问题，因为网络通讯很多时间是在等待上的。
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())


##################### coroutine的return ####################

async def say_after(delay, what):
    # asyncio.sleep() 返回的是coroutine object
    await asyncio.sleep(delay)
    return f"{what} - {delay}"


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    ret1 = await task1
    ret2 = await task2

    print(ret1)
    print(ret2)

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())


##################### gather ####################

async def say_after(delay, what):
    # asyncio.sleep() 返回的是coroutine object
    await asyncio.sleep(delay)
    return f"{what} - {delay}"


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # gather函数不是一个coroutine，他会返回一个future, future也是可以用await的
    # gather的作用：首先它的参数是若干个coroutine或者是task,甚至可以是future，也就是gather的return值，它还可以接着gather
    # 如果是coroutine,gather首先会把它包装成task,并且注册到event loop.然后它会返回一个future值，当你await这个future的时候，
    # 你就相当于告诉event loop 我要等待这里面每一个task都完成才可以继续，同时会把这些task的return值放到一个list里返回。
    # 这个list的顺序和里面 task 的顺序是一致的。
    ret = await asyncio.gather(task1, task2)
    print(ret)

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())


##################### gather最终版 ####################

async def say_after(delay, what):
    # asyncio.sleep() 返回的是coroutine object
    await asyncio.sleep(delay)
    return f"{what} - {delay}"


async def main():
    print(f"started at {time.strftime('%X')}")

    # gather函数不是一个coroutine，他会返回一个future, future也是可以用await的
    # gather的作用：首先它的参数是若干个coroutine或者是task,甚至可以是future，也就是gather的return值，它还可以接着gather
    # 如果是coroutine,gather首先会把它包装成task,并且注册到event loop.然后它会返回一个future值，当你await这个future的时候，
    # 你就相当于告诉event loop 我要等待这里面每一个task都完成才可以继续，同时会把这些task的return值放到一个list里返回。
    # 这个list的顺序和里面 task 的顺序是一致的。
    ret = await asyncio.gather(
        say_after(1, 'hello'),
        say_after(2, 'world')
    )
    print(ret)

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
