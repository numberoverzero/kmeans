import os
import kmeans
from setuptools import setup
from distutils.extension import Extension

HERE = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(HERE, 'README.rst')).read()
ckmeans = Extension(
    'lib',
    sources=['lib.c'],
    extra_compile_args=['-Wno-error=declaration-after-statement',
                        '-O3', '-std=c99']
)


setup(
    name='kmeans',
    version=kmeans.version,
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
    py_modules=['kmeans'],
    ext_modules=[ckmeans]
)
