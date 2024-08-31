import time


def func(i):
	time.sleep(1)
	print(i)


now = lambda: time.time()
start = now()

for i in range(5):
	func(i)

print(f'同步所花费的时间为: {now() - start}')
