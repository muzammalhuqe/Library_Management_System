from django.db import models
from django.contrib.auth.models import User
from books.models import BookDetails
# Create your models here.

class BorrowBook(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(BookDetails, on_delete = models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.book}"