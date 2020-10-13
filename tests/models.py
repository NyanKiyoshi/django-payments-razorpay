from payments.models import BasePayment


class DummyPayment(BasePayment):
    class Meta:
        app_label = "test"

    def get_failure_url(self):
        return "http://testserver/failure"

    def get_success_url(self):
        return "http://testserver/success"
