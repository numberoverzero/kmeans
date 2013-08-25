"""
.. module:: kmeans
   :synopsis: python wrapper for a basic c implementation of the k-means algorithm.

.. moduleauthor:: Joe Cross <joe.mcross@gmail.com>


"""

__version__ = '0.2.2'

__all__ = ['kmeans', 'version']

import ctypes
import random
from kmeans.util import here, so_path
from ctypes import Structure, c_int, byref
_here = here(__file__)
_lib = ctypes.CDLL(so_path(_here, '_lib'))

class Point(Structure):
    _fields_ = [
        ('r', c_int),
        ('g', c_int),
        ('b', c_int),
        ('cluster', c_int),
        ('weight', c_int)
    ]

def _kmeans(points, k, means=None):
    if means is not None:
        means = [(m, 1) for m in means]
    # Generate means
    else:
        means = random.sample(points, k)
    kpoints_array = Point * k
    lib_means = kpoints_array()
    for i, center in enumerate(means):
        (r, g, b), count = center
        lib_means[i] = Point(r=r, g=g, b=b, cluster=i, weight=count)
    pmeans = byref(lib_means)

    # Generate points
    npoints = len(points)
    npoints_array = Point * npoints
    lib_points = npoints_array()
    for i, point in enumerate(points):
        (r, g, b), count = point
        lib_points[i] = Point(r=r, g=g, b=b, cluster=-1, weight=count)
    ppoints = byref(lib_points)

    # Compute means
    _lib.kmeans(ppoints, npoints, pmeans, k)

    # Translate
    return [[mean.r, mean.g, mean.b] for mean in lib_means]

def kmeans(points, k, means=None):
    """Return a list of *k* means.  Initial means are optional.

    :param points: (values, weight) tuples to find means of.
            value is a list of integer values.
    :type points: list
    :param k: number of means to calculate
    :type k: int
    :param means: initial means
    :type means: list
    :rtype: list

    """
    return _kmeans(points, k, means=means)
