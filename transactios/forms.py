from django import forms
from .models import Transaction


class DepositForm(forms.Form):
    amount = forms.DecimalField()
