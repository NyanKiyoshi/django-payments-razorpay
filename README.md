# Razorpay for django-payments

**WARNING:** only the paisa (INR) currency is supported by Razorpay as of now.

## Installation
Add `django-payments-razorpay` to your project requirements 
and/ or run the installation with:
```shell
pip install django-payments-razorpay
```


## Provider parameters
First of all, to create your API credentials, you need to go in your Razorpay account settings, 
then in the API Keys section ([direct link](https://dashboard.razorpay.com/#/app/keys)).

| Key          | Required | Type      | Description |
| ------------ | -------  | --------- | ----------- |
| `public_key` | Yes      | `string`  | Your Razorpay **key id**        |
| `secret_key` | Yes      | `string`  | Your Razorpay **secret key id** |
| `image`      | No       | `string`  | An absolute or relative link to your store logo |
| `name`       | No       | `string`  | Your store name |
| `prefill`    | No       | `boolean` | Pre-fill the email and customer's full name if set to `True` (disabled by default) |


## Example configuration

In your `settings.py` file, you can add the following keys or append the data to them:

```python
PAYMENT_VARIANTS = {
    'razorpay': ('django_payments_razorpay.RazorPayProvider', {
        'public_key': 'RAZORPAY_PUBLIC_KEY',
        'secret_key': 'RAZORPAY_SECRET_KEY'})}
```

Note: if you are using **Saleor**, you may want to add Razorpay to the checkout payment choices:

```python
CHECKOUT_PAYMENT_CHOICES = [
    ('razorpay', 'RazorPay')]
```


## Notes
1. Razorpay automatically capture the whole payment amount;
2. In test mode, you can use `4111 1111 1111 1111` (or any other valid credit card numbers) 
with any future expiry date and CVV to pay orders.
