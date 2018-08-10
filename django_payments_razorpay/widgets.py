from django.forms.utils import flatatt
from django.forms.widgets import HiddenInput
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

CHECKOUT_SCRIPT_URL = 'https://checkout.razorpay.com/v1/checkout.js'


class RazorPayCheckoutWidget(HiddenInput):
    def __init__(self, provider, payment, *args, **kwargs):
        override_attrs = kwargs.get('attrs', None)
        base_attrs = kwargs['attrs'] = {
            'src': CHECKOUT_SCRIPT_URL,
            'data-key': provider.public_key,
            'data-buttontext': _('Pay now with Razorpay'),
            'data-image': provider.image,
            'data-name': provider.name,
            'data-description': payment.description or _('Total payment'),
            'data-amount': int(payment.total * 100),
            'data-currency': payment.currency
        }

        if provider.prefill:
            customer_name = '%s %s' % (
                payment.billing_last_name,
                payment.billing_first_name)
            base_attrs.update({
                'data-prefill.name': customer_name,
                'data-prefill.email': payment.billing_email
            })

        if override_attrs:
            base_attrs.update(override_attrs)
        super(RazorPayCheckoutWidget, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {})
        attrs.update(self.attrs)
        return format_html('<script{0}></script>', flatatt(attrs))
