from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BorrowBook

@method_decorator(login_required, name = 'dispatch')
class BorrowHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        borrow = BorrowBook.objects.filter(user=request.user)
        return render(request, 'profile.html', {'borrow': borrow})