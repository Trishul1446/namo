from django.db import models

# Create your models here.

class Logs(models.Model):
    card_type = models.CharField(max_length=12)
    currency = models.CharField(max_length=3)
    amount = models.CharField(max_length=64)
    card_number = models.CharField(max_length=16)
    status = models.CharField(max_length=10)
    message = models.CharField(max_length=255, default="NA")
    authorization_code = models.CharField(max_length=10, default="NA")
    time = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} {self.card_type} {self.currency} {self.amount} {self.card_number} {self.status} {self.message} {self.authorization_code} {self.time}"
