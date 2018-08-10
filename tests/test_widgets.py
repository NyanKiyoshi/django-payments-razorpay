from django_payments_razorpay.widgets import RazorPayCheckoutWidget


def test_checkout_widget_attrs_overriding(provider, payment):
    base_attrs = RazorPayCheckoutWidget(provider, payment).attrs
    overridden_attrs = RazorPayCheckoutWidget(
        provider, payment, attrs={'data-currency': 'INR'}).attrs

    base_attrs['data-currency'] = 'INR'
    assert base_attrs == overridden_attrs


def test_checkout_widget_render_without_prefill(provider, payment):
    widget = RazorPayCheckoutWidget(provider, payment)
    assert widget.render() == (
        '<script data-amount="22000" '
        'data-buttontext="Pay now with Razorpay" '
        'data-currency="USD" '
        'data-description="payment" '
        'data-image="" '
        'data-key="abc123" data-name="" '
        'src="https://checkout.razorpay.com/v1/checkout.js"></script>')


def test_checkout_widget_render_with_prefill(provider, payment):
    provider.prefill = True
    widget = RazorPayCheckoutWidget(provider, payment)
    assert widget.render() == (
        '<script data-amount="22000" '
        'data-buttontext="Pay now with Razorpay" '
        'data-currency="USD" '
        'data-description="payment" '
        'data-image="" '
        'data-key="abc123" data-name="" '
        'data-prefill.email="hello@example.com" '
        'data-prefill.name="Doe John" '
        'src="https://checkout.razorpay.com/v1/checkout.js"></script>')
