#!/usr/bin/env python

from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup


setup(
    name='keiyakusha',
    version='0.0.0',
    license='MIT',
    description=(
        'Time tracking, account management, and invoice generation tool'
        ' for contracting.'
    ),
    long_description='',
    author='Adam Barnes',
    author_email='sara.and.zuka@gmail.com',
    url='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers  # noqa
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=[
        'django==2.1',
    ],
)
