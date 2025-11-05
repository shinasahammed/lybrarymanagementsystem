import uuid
from django.db import models
from django.db.models import CASCADE


# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=CASCADE, null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
