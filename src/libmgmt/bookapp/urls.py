from django.urls import path
from . import views

urlpatterns = [
    path('addcategory/', views.catcreate, name='catcreate'),
    path('editcat/<pk>/', views.catedit, name='editcat'),
    path('viewcat/', views.catlist, name='catlist'),
    path('removecat/<pk>/', views.removecat, name='removecat'),

    path('createbook/', views.create, name='createbook'),
    path('editbook/<pk>/', views.edit, name='updatebook'),
    path('viewbook/', views.booklist, name='booklist'),
    path('deletebook/<pk>/', views.remove, name='removebook'),

    path('customer_dash/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),

    path('book/<uuid:pk>/', views.book_detail, name='book_detail'),

]
