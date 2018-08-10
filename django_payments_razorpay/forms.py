import json
from decimal import Decimal

from django import forms
from django.utils.translation import ugettext as _
from payments import PaymentStatus
from payments.forms import PaymentForm

from .widgets import RazorPayCheckoutWidget


class ModalPaymentForm(PaymentForm):
    razorpay_payment_id = forms.CharField(
        required=True, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(ModalPaymentForm, self).__init__(
            hidden_inputs=False, autosubmit=True, *args, **kwargs)

        widget = RazorPayCheckoutWidget(
            provider=self.provider, payment=self.payment)
        self.fields['razorpay'] = forms.CharField(
            widget=widget, required=False)
        self.transaction_id = None

    def clean(self):
        data = super(ModalPaymentForm, self).clean()

        if self.payment.transaction_id:
            msg = _('This payment has already been processed.')
            self._errors['__all__'] = self.error_class([msg])
        else:
            self.transaction_id = data['razorpay_payment_id']

            charge = self.provider.charge(self.transaction_id, self.payment)
            captured_amount = Decimal(charge['amount']) / 100

            self.payment.attrs.capture = json.dumps(charge)
            self.payment.captured_amount = captured_amount
            self.payment.transaction_id = self.transaction_id
            self.payment.change_status(PaymentStatus.CONFIRMED)
        return data
