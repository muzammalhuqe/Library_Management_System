from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from .models import UserAccount
from django.template.loader import render_to_string
from .forms import RegistrationForm
from django.contrib import messages
from borrow_book.models import BorrowBook
from django.contrib.auth.models import User




class SignUpView(CreateView):
    form_class = RegistrationForm
    template_name = 'user_singup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('profile'))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        user = form.save(commit=False)

        UserAccount.objects.create(
                user = user,
                account_no = 100000 + user.id,
            )
        user.save()
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"https://our-library-omv9.onrender.com/user/active/{uid}/{token}"
        email_subject = "Confirm Your Email"
        email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
        
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        return redirect('login')


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('singup')




class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        return reverse_lazy('profile')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
    

def profile(request):
    borrow = BorrowBook.objects.filter(user=request.user)
    # return render(request, 'order_history.html', {'orders': orders})
    return render(request, 'profile.html', {'borrow' : borrow})


# def BorrowHistory(request):
#     borrow = BorrowBook.objects.filter(user=request.user)
#     return render(request, 'borrow_history.html', {'borrow' : borrow})
