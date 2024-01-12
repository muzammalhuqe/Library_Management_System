from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from .forms import RegistrationForm
from django.contrib import messages
from borrow_book.models import BorrowBook


class SignUpView(CreateView):
    form_class = RegistrationForm
    template_name = 'user_singup.html'
    success_url = reverse_lazy('singup')


class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        return reverse_lazy('profile')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')
    

def profile(request):
    borrow = BorrowBook.objects.filter(user=request.user)
    # return render(request, 'order_history.html', {'orders': orders})
    return render(request, 'profile.html', {'borrow' : borrow})
