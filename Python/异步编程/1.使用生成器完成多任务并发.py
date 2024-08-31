# def func():
# 	print('当前是一个生成器函数...')
# 	while True:
# 		yield '这是生成器函数返回的数据...'


# obj = func()  # 返回一个对象：生成器对象

# 生成器需要通过next方法进行驱动
# print(next(obj))
# print(next(obj))


# 利用生成器特性进行任务切换
import time

def func_a():
	while True:
		print('这是func_a函数...')
		yield
		time.sleep(0.5)


def func_b(obj):
	while True:
		print('这是func_b函数...')
		obj.__next__()


a = func_a()
func_b(a)
