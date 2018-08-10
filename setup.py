#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test as TestCommand
from sys import version_info, exit


REQUIREMENTS = ['django-payments>=0.12.3', 'razorpay>=1.1.1']
TEST_REQUIREMENTS = ['pytest', 'pytest-django']

if version_info < (3,):
    TEST_REQUIREMENTS.append('mock')


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    test_args = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        exit(errno)


setup(
    name='django-payments-razorpay',
    author='NyanKiyoshi',
    author_email='hello@vanille.bid',
    url='https://github.com/NyanKiyoshi/django-payments-razorpay',
    description='Razorpay provider for django-payments.',
    version='0.0.0',
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
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=REQUIREMENTS,
    cmdclass={'test': PyTest},
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False)
