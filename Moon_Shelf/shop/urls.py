from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name='main'),
    path('book/<uuid:book_id>/', views.book_detail, name='book_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('catalog/<int:category_id>/', views.catalog_view, name='category_books'),
    path('catalog/<int:category_id>/<int:subcategory_id>/', views.catalog_view, name='subcategory_books'),
    path("search_suggestions/", views.search_suggestions, name="search_suggestions"),
    path("search/", views.search_results, name="search_results"),
]
