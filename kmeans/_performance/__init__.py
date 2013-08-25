"""
Utils for generating random data and comparing performance
"""
import time
import random

def timer():
    start = time.clock()
    return lambda: time.clock() - start

def random_points(n):
    """Returns n random [(x1, x2, x3), w] tuples.

        Constraints:
        0 <= abs(xN) <= 1<<8
        0 <= w <= 100
        xN, w are integers"""
    rx = lambda: random.randrange(0, 1<<8)
    rw = lambda: random.randrange(0, 10)
    rval = lambda: (rx(), rx(), rx())
    return [(rval(), rw()) for _ in xrange(n)]
