from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.add_expense, name='add_expense'),
]