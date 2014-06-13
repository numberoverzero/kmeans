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

__version__ = version = '0.3.0'
__all__ = ['kmeans', 'version']
_lib = None


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
        ('center', c_uint, 32),
        ('count', c_uint, 32)
    ]


class Center(Structure):
    _fields_ = [
        ('r', c_ulong, 64),
        ('g', c_ulong, 64),
        ('b', c_ulong, 64),
        ('count', c_uint, 32)
    ]


def _kmeans(*, points, k, means, tolerance, max_iterations):
    # Load c module
    global _lib
    if not _lib:
        _here = here(__file__)
        _lib = ctypes.CDLL(so_path(_here, '_lib'))

    # Format/Generate means
    if means:
        means = [(m, 1) for m in means]
    else:
        means = random.sample(points, k)
        print("Random Means:")
        print("\n".join(str(m) for m in means))

    kpoints_array = Center * k
    lib_means = kpoints_array()
    for i, center in enumerate(means):
        (r, g, b), count = center
        lib_means[i] = Center(r=r, g=g, b=b, count=count)
    pmeans = byref(lib_means)

    # Generate points
    npoints = len(points)
    npoints_array = Point * npoints
    lib_points = npoints_array()
    for i, point in enumerate(points):
        (r, g, b), count = point
        lib_points[i] = Point(r=r, g=g, b=b, center=-1, count=count)
    ppoints = byref(lib_points)

    # Compute means
    _lib.kmeans(ppoints, npoints, pmeans, k, tolerance, max_iterations)

    # Translate
    return [[mean.r, mean.g, mean.b] for mean in lib_means]


def kmeans(points, k, means=None, tolerance=1, max_iterations=0):
    """Return a list of *k* means.  Initial means are optional.

    :param points: (values, weight) tuples to find means of.
            value is a list of integer values.
    :type points: list

    :param k: number of means to calculate
    :type k: int

    :param means: initial means, leave blank to randomly select
    :type means: list

    :param tolerance: maximum delta to consider the means stable
    :type tolerance: int

    :param max_iterations: maximum assign/update iterations.  0 to loop until
            tolerance is met.
    :type max_iterations: int

    :rtype: list

    """
    return _kmeans(points=points, k=k, means=means,
                   tolerance=tolerance, max_iterations=max_iterations)
