#!/usr/bin/env python
import os
from setuptools import setup


setup(
    name='django-queryset-iterator',
    version='0.1.1',
    description='Iterate over large Data-sets in Django efficiently.',
    long_description='''
        Queryset Iterator ReadMe
        ========================

        General
        -------

        Queryset Iterator is a tool that is useful for iterating over large data-sets
        in Django.

        Queryset Iterator iterates over large data-sets in batches, which can be
        manually set to any batch size of your choosing, to improve performance.
        The iterator maintains an open database cursor to a median table containing
        only the primary keys of the results that would normally be obtained. Due to
        this, primary keys must be unique within the collection and this tool will
        not work should primary keys be non-unique within the database query results.
    ''',
    author='Andrew Crosio',
    author_email='andrew@andrewcrosio.com',
    url='https://github.com/Andrew-Crosio/django-queryset-iterator',
    packages=['queryset_iterator'],
    include_package_data=True,
    setup_requires=[],
    install_requires=[],
    test_suite='tests',
    tests_require=[]
)
