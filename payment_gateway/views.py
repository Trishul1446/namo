from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
import random
import string

from payment_gateway.models import Logs
# Create your views here.

class PaymentGateway(APIView):

    @staticmethod
    def save_logs(output):
        """
        To update Logs table
        """
        if output["status"] == "success":
            log = Logs(
                        card_type = output["type"],
                        currency = output["currency"],
                        amount = output["amount"],
                        card_number = output["card"]["number"],
                        status = output["status"],
                        authorization_code = output["authorization_code"],
                        time = output["time"]
            )
        else:
            log = Logs(
                        card_type = output["type"],
                        currency = output["currency"],
                        amount = output["amount"],
                        card_number = output["card"]["number"],
                        status = output["status"],
                        message = output["message"],
                        time = output["time"]
            )
        log.save()

    @staticmethod
    def validate_card(data):
        """
        To check the card validity like expiry.
        """

        valid_types = ["debitcard", "creditcard"]
        card_details = data["card"]
        response = {}
        current_date = datetime.now()
        response["time"] = current_date.strftime("%Y-%m-%d %H:%M:%S")

        if data["type"].lower() not in valid_types or \
             len(card_details["number"]) != 16 or \
             len(card_details["cvv"]) != 3:
             response["status"] = "failed"
             response["message"] = "Incorrect card details."
             return response


        exp_year = int(card_details["expirationYear"])
        exp_month = int(card_details["expirationMonth"])

        if (current_date.year > exp_year) or \
            (current_date.month >  exp_month and current_date.year ==  exp_year):
            response["status"] = "failed"
            response["message"] = "Card has already expired."
            return response

        response["status"] = "success"
        response["authorization_code"] = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        return response

    def post(self, request):
        """
        To handle post request and send corresponding response
        """

        output = PaymentGateway.validate_card(request.data)
        output["amount"] = request.data["amount"]
        output["currency"] = request.data["currency"]
        output["type"] = request.data["type"].lower()
        output["card"] = {"number" : request.data["card"]["number"]}

        PaymentGateway.save_logs(output)
        return Response(output)
