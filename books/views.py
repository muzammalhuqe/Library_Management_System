from . import forms
from django.views.generic import DetailView
from books.models import BookDetails


# Create your views here.

class DetailBookView(DetailView):
    model = BookDetails
    template_name = 'book_details.html'
    pk_url_kwarg = 'id'
    context_object_name = 'book_details'


    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data = self.request.POST)
        car  = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit = False)
            new_comment.car = car
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        car = self.object
        comments = car.comments.all()

        
        comment_form = forms.CommentForm()

        context ['comments'] = comments
        context ['comment_form'] = comment_form
        return context



from django.shortcuts import render, get_object_or_404
from .models import Comment
from .forms import CommentForm
from books.models import BookDetails  # Assuming your BookDetails model is in the 'books' app

def view_comments(request, book_id):
    book = get_object_or_404(BookDetails, pk=book_id)
    comments = Comment.objects.filter(car=book)

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = book
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'comments.html', {'comment_form': comment_form, 'comments': comments, 'user': request.user})

