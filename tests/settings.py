from __future__ import unicode_literals
import os

PROJECT_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'django_payments_razorpay'))

SECRET_KEY = 'secret'
PAYMENT_HOST = 'example.com'

INSTALLED_APPS = ['payments', 'django.contrib.sites']

PAYMENT_VARIANTS = {
    'razorpay': ('django_payments_razorpay.RazorPayProvider', {
        'public_key': 'RAZORPAY_PUBLIC_KEY',
        'secret_key': 'RAZORPAY_SECRET_KEY'})}
