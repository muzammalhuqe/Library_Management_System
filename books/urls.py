from django.urls import path, include
from . views import DetailBookView, view_comments
urlpatterns = [
    path('book/<int:id>', DetailBookView.as_view(), name='book_details'),
    path('view/<int:id>', view_comments, name='view_details'),
]