from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from borrow.models import Borrow
from libapp.models import User
from .forms import catform, bookForm
from .models import Category, Book
from libapp import views


# Create your views here.

def catcreate(request):
    if request.method == 'POST':
        form = catform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catlist')
    else:
        form = catform()
    return render(request, 'book/category/addcategory.html', {'form': form})


def catlist(request):
    cate = Category.objects.all()
    return render(request, 'book/category/viewcat.html', {'cate': cate})


def catedit(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = catform(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('catlist')
    else:
        form = catform(instance=cat)
    return render(request, 'book/category/editcat.html', {'form': form})


def removecat(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    cat.delete()
    return redirect('catlist')




def create(request):
    if request.method == 'POST':
        form = bookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('booklist')
    else:
        form = bookForm()
    return render(request, 'book/addbook/createbook.html', {'form': form})


def booklist(request):
    books = Book.objects.all()
    return render(request, 'book/addbook/viewbooks.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book/addbook/book_detail.html', {'book': book})

def edit(request, pk):
    user = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = bookForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('booklist')
    else:
        form = bookForm(instance=user)
    return render(request, 'book/addbook/update.html', {'form': form})


def remove(request, pk):
    user = get_object_or_404(Book, pk=pk)
    user.delete()
    return redirect('booklist')

def customer_dashboard(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'customer_dashboard.html', {'books': books})


  # adjust import if your models are elsewhere

def staff_dashboard(request):
    total_books = Book.objects.count()
    total_users = User.objects.count()
    total_borrows = Borrow.objects.count()
    pending_returns = Borrow.objects.filter(return_date__isnull=True).count()

    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_borrows': total_borrows,
        'pending_returns': pending_returns,
    }

    return render(request, 'staff_dashboard.html', context)