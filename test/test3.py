import math
def compute_roots(nums):
    result = []
    for n in nums:
        result.append(math.sqrt(n))
    return result

def test():
    nums = range(1000000)
    r = compute_roots(nums)

if __name__ == '__main__':
    from timeit import Timer
    t = Timer("test()", "from __main__ import test")
    print t.timeit(100)