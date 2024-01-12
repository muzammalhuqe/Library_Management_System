from django.urls import path, include
from . import views

urlpatterns = [
    path('book/', views.BorrowHistoryView.as_view(), name='borrow_history'),
]