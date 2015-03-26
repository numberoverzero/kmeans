import os
from setuptools import setup, find_packages
from distutils.extension import Extension

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.rst')) as readme_file:
    README = readme_file.read()
C_KMEANS = Extension(
    'kmeans/lib',
    sources=['kmeans/lib.c'],
    extra_compile_args=['-Wno-error=declaration-after-statement',
                        '-O3', '-std=c99']
)

# The packaging is a little wonky.  I've been fighting with tox to try to
# load the dll from the correct relative path, but
# kmeans.__init__:os.path.dirname(os.path.realpath(__file__)) just
# refuses to point anywhere BUT the .tox path.

# To get over that, I moved everything under the kmeans/ folder and for now,
# if it works that's cool.  It's not clean and I don't like it, but it's also
# 1:30 am

setup(
    name='kmeans',
    version='1.0.2',
    url='http://github.com/numberoverzero/kmeans/',
    license='MIT',
    author='Joe Cross',
    install_requires=[],
    author_email='joe.mcross@gmail.com',
    description='python wrapper for basic c implementation of kmeans',
    long_description=README,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    packages=find_packages(exclude=('tests',)),
    ext_modules=[C_KMEANS]
)
