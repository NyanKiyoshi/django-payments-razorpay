import pytest
from django_payments_razorpay import ModalPaymentForm
from payments import PaymentStatus
from tests.conftest import TOTAL, TOTAL_INT, TRANSACTION_ID


def test_modal_payment_form_valid_data(
        provider, payment, valid_payment_form_data):
    form = ModalPaymentForm(
        provider=provider, payment=payment, data=valid_payment_form_data)
    assert form.is_valid()
    provider.razorpay_client.payment.capture.assert_called_once_with(
        TRANSACTION_ID, TOTAL_INT)
    assert payment.captured_amount == TOTAL
    assert payment.transaction_id == TRANSACTION_ID
    assert payment.status == PaymentStatus.CONFIRMED


def test_modal_payment_form_already_processed(
        provider, payment, valid_payment_form_data):
    payment.transaction_id = TRANSACTION_ID
    form = ModalPaymentForm(
        provider=provider, payment=payment, data=valid_payment_form_data)
    assert not form.is_valid()
    provider.razorpay_client.payment.capture.assert_not_called()


def test_modal_payment_form_invalid_data(
        provider, payment, valid_payment_form_data):
    form = ModalPaymentForm(
        provider=provider, payment=payment, data={})

    with pytest.raises(KeyError, message='razorpay_payment_id'):
        form.is_valid()
    provider.razorpay_client.payment.capture.assert_not_called()
