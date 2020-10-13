from decimal import Decimal

import mock
import pytest
from payments import PaymentStatus

from django_payments_razorpay import RazorPayProvider
from tests.models import DummyPayment

TRANSACTION_ID = "pay_7IZD7aJ2kkmOjk"

CLIENT_ID = "abc123"
SECRET = "123abc"
PAYMENT_TOKEN = "5a4dae68-2715-4b1e-8bb2-2c2dbe9255f6"
VARIANT = "razorpay"
EMAIL = "hello@example.com"
FIRST_NAME = "John"
LAST_NAME = "Doe"
TOTAL = Decimal(220)
TOTAL_INT = 22000


@pytest.fixture
def payment():
    payment_data = {
        "description": "payment",
        "currency": "USD",
        "delivery": Decimal(10),
        "status": PaymentStatus.WAITING,
        "tax": Decimal(10),
        "token": PAYMENT_TOKEN,
        "total": TOTAL,
        "captured_amount": Decimal(0),
        "variant": VARIANT,
        "transaction_id": None,
        "message": "",
        "billing_first_name": FIRST_NAME,
        "billing_last_name": LAST_NAME,
        "billing_email": EMAIL,
    }
    _payment = DummyPayment(**payment_data)
    _payment.id = 1
    _payment.save = mock.MagicMock()
    _payment.get_success_url = mock.MagicMock(new_callable=lambda: "https://success")
    return _payment


@pytest.fixture
def valid_capture_data():
    return {
        "id": TRANSACTION_ID,
        "entity": "payment",
        "amount": TOTAL_INT,
        "currency": "INR",
        "status": "captured",
        "order_id": None,
        "invoice_id": None,
        "international": False,
        "method": "wallet",
        "amount_refunded": 0,
        "refund_status": None,
        "captured": True,
        "description": "Purchase Description",
        "wallet": "freecharge",
        "email": "a@b.com",
        "contact": "91xxxxxxxx",
        "notes": {"merchant_order_id": "order id"},
        "error_code": None,
        "error_description": None,
        "created_at": 1400826750,
    }


@pytest.fixture
def valid_full_refund_data():
    return {
        "id": "rfnd_5UXHCzSiC02RBz",
        "entity": "refund",
        "amount": TOTAL_INT,
        "currency": "INR",
        "payment_id": "pay_5UWttxtCjkrldV",
        "notes": {},
        "created_at": 1462887226,
    }


@pytest.fixture
def valid_partial_refund_data(valid_full_refund_data):
    valid_full_refund_data = valid_full_refund_data.copy()
    valid_full_refund_data["amount"] = 2000
    return valid_full_refund_data


@pytest.fixture
def provider(valid_capture_data, valid_full_refund_data):
    _provider = RazorPayProvider(CLIENT_ID, SECRET)
    mocked_payment = _provider.razorpay_client.payment = mock.MagicMock()
    mocked_payment.capture.return_value = valid_capture_data
    mocked_payment.refund.return_value = valid_full_refund_data
    return _provider


@pytest.fixture
def valid_payment_form_data():
    return {"razorpay_payment_id": TRANSACTION_ID}
