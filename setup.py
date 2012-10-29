#!/usr/bin/env python
from distutils.core import setup
from distutils.command.install_data import install_data

setup(name='DomainCheck',
        version='0.1',
        description='Domain check website',
        author='David Mcilwee',
        author_email='blak631@gmail.com',
        url='',
        packages=['domaincheck'],
        include_package_data=True,
        zip_safe=False,
        install_requires=['Flask', 'dnspython']
)

