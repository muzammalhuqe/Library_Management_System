from django.shortcuts import render
from books.models import BookDetails
from books.models import Category


def home(request, book_slug = None):

    data = BookDetails.objects.all()
    if book_slug is not None:
        cat = Category.objects.get(slug = book_slug)
        data = BookDetails.objects.filter(category = cat)
    categories = Category.objects.all()
    return render(request, 'home.html', {'data' : data, 'categories' : categories})





