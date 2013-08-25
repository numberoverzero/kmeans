from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import os
import sys

import kmeans

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

setup(
    name='kmeans',
    version=kmeans.__version__,
    url='http://github.com/numberoverzero/kmeans/',
    license='MIT',
    author='Joe Cross',
    tests_require=['pytest', 'tox'],
    install_requires=[],
    cmdclass={'test': Tox},
    author_email='joe.mcross@gmail.com',
    description='python wrapper for basic c implementation of kmeans',
    long_description=long_description,
    packages=['kmeans'],
    include_package_data=True,
    platforms='any',
    test_suite='kmeans.test.test_kmeans',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
