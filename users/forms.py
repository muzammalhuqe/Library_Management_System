from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount


# class RegistrationForm(UserCreationForm):
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
#     email = forms.CharField(widget=forms.EmailInput(attrs={'id' : 'required'}))
    
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'id' : 'required'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def save(self, commit=True ):
        our_user = super().save(commit=False) # ami database e data save korbo na ekhn
        if commit == True:
            our_user.save()
            UserAccount.objects.create(
                user = our_user,
                account_no = 100000 + our_user.id,
            )
        return our_user
    
