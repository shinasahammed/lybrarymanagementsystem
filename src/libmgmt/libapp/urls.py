from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # dashboards
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),

    path('profile/', views.profile_view, name='profile'),
    path('firstprofile/',views.profile, name='firstprofile'),

]
