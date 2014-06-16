"""
.. module:: kmeans
   :synopsis: python wrapper for a basic c implementation of the
              k-means algorithm.

.. moduleauthor:: Joe Cross <joe.mcross@gmail.com>

"""
import os
import ctypes
import random
import sysconfig
from ctypes import Structure, c_uint, c_ulong, byref

__version__ = version = '0.3.1'
__all__ = ['kmeans', 'version']
lib = None


def so_path(dir, filename):
    '''http://www.python.org/dev/peps/pep-3149/'''
    suffix = sysconfig.get_config_var('SO')
    if not suffix:
        soabi = sysconfig.get_config_var('SOABI')
        suffix = ".{}.so".format(soabi)
    return os.path.join(dir, filename + suffix)


def here(__file__):
    '''Absolute directory of a script given its __file__ value'''
    return os.path.dirname(os.path.realpath(__file__))


class Point(Structure):
    _fields_ = [
        ('r', c_uint, 8),
        ('g', c_uint, 8),
        ('b', c_uint, 8),
        ('center', c_uint, 8),
        ('count', c_uint, 32)
    ]


class Center(Structure):
    _fields_ = [
        ('r', c_ulong, 64),
        ('g', c_ulong, 64),
        ('b', c_ulong, 64),
        ('count', c_uint, 32)
    ]


def _kmeans(*, points, k, centers, tolerance, max_iterations):
    # Load c module
    global lib
    if not lib:
        _here = here(__file__)
        lib = ctypes.CDLL(so_path(_here, 'lib'))

    if centers:
        if k != len(centers):
            raise ValueError(
                "Provided {} centers but k is {}".format(len(centers), k))
    else:
        centers = random.sample(points, k)

    pcenters = (Center * k)()
    for i, center in enumerate(centers):
        (r, g, b), count = center
        pcenters[i] = Center(r=r, g=g, b=b, count=count)
                        # Save a reference to the array so we can read out
    centers = pcenters  # the results
    pcenters = byref(pcenters)

    # Generate points
    n = len(points)
    ppoints = (Point * n)()
    for i, point in enumerate(points):
        (r, g, b), count = point
        ppoints[i] = Point(r=r, g=g, b=b, center=-1, count=count)
    ppoints = byref(ppoints)

    # Compute centers
    lib.kmeans(ppoints, n, pcenters, k, tolerance, max_iterations)

    # Translate
    return [[center.r, center.g, center.b] for center in centers]


def kmeans(points, k, centers=None, tolerance=1, max_iterations=0):
    """Return a list of *k* centers (means).  Initial centers are optional.

    :param points: (values, weight) tuples to find centers of.
            value is a list of integer values.
    :type points: list

    :param k: number of centers to calculate
    :type k: int

    :param centers: initial centers, leave blank to randomly select
    :type centers: list

    :param tolerance: maximum delta to consider the centers stable
    :type tolerance: int

    :param max_iterations: maximum assign/update iterations.  0 to loop until
            tolerance is met.
    :type max_iterations: int

    :rtype: list

    """
    return _kmeans(points=points, k=k, centers=centers,
                   tolerance=tolerance, max_iterations=max_iterations)
