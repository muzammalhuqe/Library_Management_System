from django import forms
from .models import Comment, Category,BookDetails

class CategoryForm(forms.ModelForm):
    class Meta: 
        model = Category
        fields = '__all__'

class AddBookForm(forms.ModelForm):
    class Meta: 
        model = BookDetails
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment
        fields = ['name', 'email', 'body']