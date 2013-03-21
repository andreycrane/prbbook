#!/usr/bin/env python

from setuptools import setup

setup(
    name='Problems Book',
    version='1.0.1',
    description='Problems Book application for OpenShift cloud platform',
    author='Andrey Zhuravlyov',
    author_email='example@example.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django==1.5', 'South==0.7.6', 'PIL==1.1.7', 'celery==3.0.16', 'django-celery==3.0.11', 'kombu==2.5.7'],
)
