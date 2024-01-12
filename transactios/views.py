from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from books.models import BookDetails
from borrow_book.models import BorrowBook
from django.urls import reverse_lazy
from .forms import DepositForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from transactios.constants import DEPOSIT,BORROW,RETURN
from users.models import UserAccount
# Create your views here.

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

def send_borrow_email(user, subject, template):
        message = render_to_string(template, {
            'user' : user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class DepositMoneyView(LoginRequiredMixin,FormView):
    form_class = DepositForm
    title = 'Deposit'
    template_name = 'deposit.html'
    success_url = reverse_lazy('profile')

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        send_transaction_email(self.request.user, amount, "Deposite Message", "deposit_email.html")

        return super().form_valid(form)

    

class BorrowBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = get_object_or_404(BookDetails, pk=id)
        
        if book.quantity > 0:
            user_profile = UserAccount.objects.get(user=request.user)
            if user_profile.balance >= book.price:
                borrow = BorrowBook(user=request.user, book=book)
                borrow.save()

                # Decrease book quantity and update user balance
                book.quantity -= 1
                book.save()

                user_profile.balance -= book.price
                user_profile.save()
                send_borrow_email(self.request.user, "Borrow Message", "borrow_book_email.html")

                return redirect('profile')
            else:
                return render(request, 'insufficient_balance.html') 
        else:
            return render(request, 'out_of_stock.html')
        


class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = get_object_or_404(BookDetails, pk=id)
        user_profile = UserAccount.objects.get(user=request.user)

        # Check if the user has borrowed the book
        borrow_instance = BorrowBook.objects.filter(user=request.user, book=book, returned=False).first()

        if borrow_instance:
            # Mark the book as returned
            borrow_instance.returned = True
            borrow_instance.save()

            # Increase book quantity and update user balance
            book.quantity += 1
            book.save()

            user_profile.balance += book.price
            user_profile.save()

            send_borrow_email(request.user, "Return Message", "return_book_email.html")

            return redirect('profile')
        else:
            return render(request, 'return_book.html')


# class ReturnBookView(LoginRequiredMixin, View):
#     def get(self, request, id):
#         book = get_object_or_404(BookDetails, pk=id)
        
#         if book.quantity > 0:
#             user_profile = UserAccount.objects.get(user=request.user)
#             if user_profile.balance >= book.price:
#                 borrow = BorrowBook(user=request.user, book=book)
#                 borrow.save()

#                 book.quantity += 1
#                 book.save()

#                 user_profile.balance += book.price
#                 user_profile.save()
#                 send_borrow_email(self.request.user, "Return Message", "return_book_email.html")

#                 return redirect('profile')
#             else:
#                 return render(request, 'return_book.html') 
#         else:
#             return render(request, 'return_book.html')
        
