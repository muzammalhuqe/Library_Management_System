from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'id' : 'required'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1','password2',]
        
    def save(self, commit = True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save()

            UserAccount.objects.create(
                user = our_user,
                account_no = 100000 + our_user.id,
            )
            return our_user
        
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError({'error' : "Email Already exists"})
        
        account = User(username = username, email=email, first_name = first_name, last_name = last_name)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
    
