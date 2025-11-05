from django.urls import path
from . import views

urlpatterns = [
    path('borrowlist/', views.borrow_list, name='borrow_list'),
    path('borrow/<uuid:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<uuid:borrow_id>/', views.return_book, name='return_book'),
    path('all/', views.all_borrowed_books, name='all_borrowed_books'),
    path('borrow/delete/<uuid:borrow_id>/', views.delete_borrow_by_user, name='delete_borrow_by_user'),
]
