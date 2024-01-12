from django.db import models
from .constants import TRANSACTION_TYPE
from users.models import UserAccount
# Create your models here.

class Transaction(models.Model):
    account = models.OneToOneField(UserAccount, related_name = 'transactions', on_delete = models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True)