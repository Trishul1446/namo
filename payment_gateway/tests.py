from django.test import TestCase, Client
from payment_gateway.models import Logs

class PaymentGatewayTestCases(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logs_insertion(self):
        card = {
                "amount":"100",
                "currency": "USD",
                "type": "creditcard",
                "card": {
                    "number": "4111111111111111",
                    "expirationMonth": "9",
                    "expirationYear": "2019",
                    "cvv": "111"
                }
            }
        response = self.client.post("/paymentGateway", data=card,
                                    content_type='application/json')
        output = response.data
        log = Logs.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(log.count(), 1)

    def test_expiry(self):
        card = {
                "amount":"100",
                "currency": "USD",
                "type": "creditcard",
                "card": {
                    "number": "4111111111111111",
                    "expirationMonth": "9",
                    "expirationYear": "2019",
                    "cvv": "111"
                }
            }
        response = self.client.post("/paymentGateway", data=card,
                                    content_type='application/json')
        self.assertEqual(response.data["status"], "failed")
        self.assertTrue("message" in response.data)
        self.assertTrue("authorization_code" not in response.data)

    def test_invalid_cvv(self):
        card = {
                "amount":"100",
                "currency": "USD",
                "type": "creditcard",
                "card": {
                    "number": "4111111111111111",
                    "expirationMonth": "11",
                    "expirationYear": "2022",
                    "cvv": "1111"
                }
            }
        response = self.client.post("/paymentGateway", data=card,
                                    content_type='application/json')
        self.assertEqual(response.data["status"], "failed")
        self.assertTrue("message" in response.data)
        self.assertTrue("authorization_code" not in response.data)

    def test_invalid_card_number(self):
        card = {
                "amount":"100",
                "currency": "USD",
                "type": "creditcard",
                "card": {
                    "number": "41111111111111",
                    "expirationMonth": "11",
                    "expirationYear": "2022",
                    "cvv": "111"
                }
            }
        response = self.client.post("/paymentGateway", data=card,
                                    content_type='application/json')
        self.assertEqual(response.data["status"], "failed")
        self.assertTrue("message" in response.data)
        self.assertTrue("authorization_code" not in response.data)

    def test_success(self):
        card = {
                "amount":"100",
                "currency": "USD",
                "type": "creditcard",
                "card": {
                    "number": "4111111111111111",
                    "expirationMonth": "111",
                    "expirationYear": "2022",
                    "cvv": "111"
                }
            }
        response = self.client.post("/paymentGateway", data=card, content_type='application/json')
        self.assertEqual(response.data["status"], "success")
        self.assertFalse("message" in response.data)
        self.assertTrue("authorization_code" in response.data)
