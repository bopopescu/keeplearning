@profile
def foo():
	sum_count = 0
	for i in range(100000):
		for j in range(1000):
			sum_count += 1

if __name__ == '__main__':
	# from timer import Timer
	# with Timer() as t:	
	# 	foo()
	# print t.secs
	foo()