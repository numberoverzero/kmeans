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
        xN, w are integers
    """

    rx = lambda: random.randrange(0, 1<<8)
    rw = lambda: random.randrange(0, 10)
    rval = lambda: (rx(), rx(), rx())
    return ListProxy([(rval(), rw()) for _ in xrange(n)])

class ListProxy(object):
    """So we don't have to keep generating random points,

    just fake smaller sizes using set_len
    """

    def __init__(self, real_list):
        self._data = real_list
        self._len = len(self._data)

    def set_len(self, n):
        self._len = n

    def __len__(self):
        return self._len

    def __getitem__(self, index):
        return self._data[index]

    def __iter__(self):
        for i in xrange(self._len):
            yield self._data[i]
