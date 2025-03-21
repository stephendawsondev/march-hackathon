import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField


# Create your models here.
class Payment(models.Model):
    confirmation_number = models.CharField(max_length=32, null=False, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("SUCCESS", "Success"), ("FAILED", "Failed"), ("PENDING", "Pending")],
        default="PENDING",
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=Decimal("0.00")
    )
    stripe_payment_intent_id = models.CharField(max_length=254, null=True, blank=True)
