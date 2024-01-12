from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, unique = True, blank=True, null=True)

    def __str__(self):
        return self.name


class BookDetails(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length = 50)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to = 'books/media/uploads/', blank=True, null=True)


    def __str__(self) :
        return f"Book : {self.title}, Categories : {self.category.name}"
    


class Comment(models.Model):
    car = models.ForeignKey(BookDetails, on_delete = models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Comment by {self.name}"