import os
import kmeans
from setuptools import setup
from distutils.extension import Extension

here = os.path.abspath(os.path.dirname(__file__))
ckmeans = Extension(
    'lib',
    sources=['lib.c'],
    extra_compile_args=['-O3', '-std=c99']
)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n\n')
    contents = []
    for filename in filenames:
        with open(filename, encoding=encoding) as f:
            contents.append(f.read())
    return sep.join(contents)

long_description = read('README.rst', 'LICENSE')


setup(
    name='kmeans',
    version=kmeans.version,
    url='http://github.com/numberoverzero/kmeans/',
    license='MIT',
    author='Joe Cross',
    install_requires=[],
    author_email='joe.mcross@gmail.com',
    description='python wrapper for basic c implementation of kmeans',
    long_description=long_description,
    include_package_data=True,
    platforms='any',
    classifiers=[
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
    },
    ext_modules=[ckmeans]
)
