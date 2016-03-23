#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    test_args = None
    test_suite = None

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''
        self.test_args = []
        self.test_suite = True

    def finalize_options(self):
        pass

    def run_tests(self):
        import pytest
        exit_code = pytest.main(self.pytest_args)
        sys.exit(exit_code)


def read(*path):
    with open(os.path.join(os.path.dirname(__file__), *path)) as fd:
        return fd.read().strip()


setup(
    name='octoconf',
    version='0.1.0',
    url='https://github.com/andras-tim/octoconf',
    license='GPLv3',
    author='Andras Tim',
    author_email='andras.tim@gmail.com',
    platforms='any',
    description='Multi-profile supported, flexible config library',
    long_description=read('README.rst'),

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='yaml config multi-profile inheritance',

    install_requires=read('requirements.txt').splitlines(),
    tests_require=read('requirements-dev.txt').splitlines(),

    packages=find_packages(exclude=['tests']),
    cmdclass={
        'test': PyTest
    },
)
