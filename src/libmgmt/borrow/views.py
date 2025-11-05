from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from bookapp.models import Book
from libapp.models import User
from .models import Borrow


@login_required
def borrow_book(request, book_id):
    # user = get_object_or_404(User, id=user_id)
    book = get_object_or_404(Book, id=book_id)

    # # Only allow borrowing for self
    # if request.user.id != request.user:
    #     messages.error(request, "You can only borrow books for yourself.")
    #     return redirect('borrow_list')

    # Check if same book already borrowed and not returned
    if Borrow.objects.filter(user=request.user, book=book, is_returned=False).exists():
        messages.warning(request, "You already borrowed this book and haven't returned it.")
        return redirect('borrow_list')

    Borrow.objects.create(user=request.user, book=book)
    messages.success(request, f"You borrowed '{book.title}'.")
    return redirect('borrow_list')


@login_required
def borrow_list(request):
    if request.user.is_staff:
        borrows = Borrow.objects.select_related('book', 'user').all()
    else:
        borrows = Borrow.objects.filter(user=request.user)

    return render(request, 'book/borrow/borrow_list.html', {'borrows': borrows})



@login_required
def all_borrowed_books(request):
    borrows = Borrow.objects.select_related('user', 'book').all()
    return render(request, 'book/borrow/all_borrowed_books.html', {'borrows': borrows})


@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if not borrow.is_returned:
        borrow.is_returned = True
        borrow.return_date = timezone.now()
        borrow.book.available_copies += 1
        borrow.book.save()
        borrow.save()
        messages.success(request, f"You returned '{borrow.book.title}'.")
    else:
        messages.info(request, f"'{borrow.book.title}' is already returned.")
    return redirect('all_borrowed_books')

#
# @login_required
# def delete_borrow_by_user(request, borrow_id):
#     borrow = get_object_or_404(Borrow, id=borrow_id)
#     borrow.delete()
#     messages.success(request, "Borrow record deleted.")
#     return redirect('all_borrowed_books')


@login_required
def delete_borrow_by_user(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if borrow.is_returned:
        borrow.is_hidden = True
        borrow.save()
        messages.success(request, "Returned book hidden from list.")
    else:
        messages.error(request, "Cannot delete a book that has not been returned.")
    return redirect('all_borrowed_books')
