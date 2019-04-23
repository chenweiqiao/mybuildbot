#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.test import test as TestCommand
import re
import os
import sys


class PyTest(TestCommand):
    """ 添加自定义test命令来测试用例 """

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']  # 测试用例所在目录
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath, filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]  # 筛取非py包目录

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = 'v0.0'

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist")
    os.system("python setup.py bdist_wheel")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

setup(
    name='myproject',
    version=version,
    url='',
    license='BSD',
    description='',
    author='ubuntu',
    author_email='',
    packages=get_packages(''),
    package_data=get_package_data(''),
    cmdclass={'test': PyTest},
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)

