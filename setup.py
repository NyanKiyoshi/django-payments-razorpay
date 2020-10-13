#!/usr/bin/env python

from setuptools import setup

REQUIREMENTS = ["django-payments>=0.12.3", "razorpay>=1.1.1"]
TEST_REQUIREMENTS = ["pytest", "mock", "pre-commit"]

setup(
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
)
