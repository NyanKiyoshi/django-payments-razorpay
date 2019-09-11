from decimal import Decimal

import mock
import pytest
import razorpay.errors
from django_payments_razorpay import RazorPayProvider
from payments import PaymentStatus, RedirectNeeded
from payments.core import provider_factory
from tests.conftest import CLIENT_ID, SECRET, TOTAL, TRANSACTION_ID


def test_provider_factory():
    assert isinstance(provider_factory('razorpay'), RazorPayProvider)


def test_authentication(provider):
    assert provider.razorpay_client.auth == (CLIENT_ID, SECRET)


@mock.patch(
    'django_payments_razorpay.forms.RazorPayCheckoutWidget', create=True)
def test_get_form(mocked_razor_checkout, provider, payment):
    form = provider.get_form(payment)
    mocked_razor_checkout.assert_called_once_with(
        provider=provider, payment=payment)
    assert 'razorpay' in form.fields
    assert form.fields['razorpay'].widget == mocked_razor_checkout.return_value


def test_get_form_invalid_data(provider, payment):
    with pytest.raises(KeyError) as exc:
        provider.get_form(payment, data={})

    assert exc.value.args == ('razorpay_payment_id',)

    assert payment.captured_amount == 0
    assert payment.transaction_id is None


def test_get_form_valid_data(valid_payment_form_data, provider, payment):
    with pytest.raises(RedirectNeeded) as exc:
        provider.get_form(payment, data=valid_payment_form_data)

    assert exc.value.args[0] == payment.get_success_url()

    assert payment.save.call_count != 0
    assert payment.status == PaymentStatus.CONFIRMED
    assert payment.captured_amount == payment.total
    assert payment.transaction_id == TRANSACTION_ID


@mock.patch('payments.models.provider_factory', create=True)
@pytest.mark.parametrize(
    'partial_refund,expected_status', (
        (False, PaymentStatus.REFUNDED),
        (True, PaymentStatus.CONFIRMED)
    ))
def test_refund(
        mocked_provider_factory,
        partial_refund, expected_status,
        valid_partial_refund_data, provider, payment):

    mocked_provider_factory.return_value = provider
    provider.refund = mock.MagicMock(wraps=provider.refund)

    if partial_refund:
        refund_amount = Decimal(20)
        expected_captured_amount = Decimal(200)
        provider.razorpay_client.payment.refund.return_value = (
            valid_partial_refund_data)
    else:
        refund_amount = TOTAL
        expected_captured_amount = 0

    payment.captured_amount = payment.total
    payment.status = PaymentStatus.CONFIRMED
    payment.refund(amount=refund_amount)

    mocked_provider_factory.assert_called_once_with('razorpay')
    provider.refund.assert_called_once_with(payment, refund_amount)
    assert payment.captured_amount == expected_captured_amount
    assert payment.status == expected_status


def test_refund_invalid_data(provider, payment):
    def _raise_fake_error(*args, **kwargs):
        raise razorpay.errors.BadRequestError('hello world')
    payment.captured_amount = payment.total
    provider.razorpay_client.payment.refund.side_effect = _raise_fake_error

    with pytest.raises(ValueError) as exc:
        provider.refund(payment, Decimal(2220))

    assert str(exc.value.args) == str(('hello world',))
    assert payment.captured_amount == payment.total
