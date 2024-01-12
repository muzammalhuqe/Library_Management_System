from django.urls import path
from .views import DepositMoneyView, BorrowBookView,ReturnBookView

urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path('borrow/<int:id>/', BorrowBookView.as_view(), name='borrow_book'),
    path('return/<int:id>/', ReturnBookView.as_view(), name='return_book'),
]