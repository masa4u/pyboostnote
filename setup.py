from setuptools import setup, find_packages
from boostnote import version

MODULE_NAME = 'pyboostnote'
CLASSIFIERS = [
    'Development Status :: 1 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python',
    'Topic :: Utilities',
]
PACKAGE_LIST = find_packages(exclude=(['boostnote.tests']))
setup(
    name='pyboostnote',
    version=version,
    packages=PACKAGE_LIST,
    include_package_data=True,
    zip_safe=False,

    author='masa4u@gmail.com',
    maintainer='masa4u@gmail.com',
    url='http://github.com/masa4u/pyboostnote',

    description='boostnote migrator/manager using python',
    classifiers=CLASSIFIERS,
    test_suite='boostnote.tests.loaders.boostnote_test_suite',
)
