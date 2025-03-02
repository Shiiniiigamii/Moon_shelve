from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('books', views.books),
    path('basket', views.basket),
    path('orders', views.orders),
    path('profile', views.profile),
    path('stock', views.stock),
]
