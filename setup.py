#!/usr/bin/env python

from setuptools import setup

REQUIREMENTS = ['django-payments>=0.12.3', 'razorpay>=1.1.1']
TEST_REQUIREMENTS = ['pytest', 'mock']


setup(
    name='django-payments-razorpay',
    author='NyanKiyoshi',
    author_email='hello@vanille.bid',
    url='https://github.com/NyanKiyoshi/django-payments-razorpay/',
    description='Razorpay provider for django-payments.',
    version='0.1.0',
    packages=['django_payments_razorpay'],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False)
