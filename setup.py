import unittest
from setuptools import setup, find_packages
from boostnote import version


def boostnote_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite

MODULE_NAME = 'pyboostnote'
PACKAGE_DATA = list()
CLASSIFIERS = [
    'Development Status :: 1 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python',
    'Topic :: Utilities',
]


setup(
    name='pyboostnote',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    author='masa4u@gmail.com',
    maintainer='masa4u@gmail.com',
    url='http://github.com/masa4u/pyboostnote',

    description='boostnote migrator/manager using python',
    classifiers=CLASSIFIERS,
    test_suite='setup.boostnote_test_suite',
)
