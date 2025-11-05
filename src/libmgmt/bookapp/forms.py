from bookapp.models import Book, Category
from django import forms


class bookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields = ('title', 'author', 'published_date','category', 'isbn', 'available_copies','image',)

class catform(forms.ModelForm):
    class Meta:
        model=Category
        fields = ('category',)