from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model


def main(request):
    books = Books.objects.all()
    return render(request, 'shop/books.html', {'books': books})

def book_detail(request, book_id):
    # Получаем книгу по её ID
    book = get_object_or_404(Books, pk=book_id)
    
    # Получаем все отзывы для этой книги
    reviews = Reviews.objects.filter(book=book)
    
    return render(request, 'shop/book_detail.html', {'book': book, 'reviews': reviews})

# Вход
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        # Проверяем пользователя по email
        user = Users.objects.filter(email=email).first()
        
        if user and check_password(password, user.password):
            # Используем кастомного пользователя
            user_instance = user
            
            # Преобразуем UUID в строку для сессии
            request.session['user_id'] = str(user_instance.user_id)
            request.user = user_instance  # Устанавливаем текущего пользователя в request

            # Является важным, чтобы Django не пытался работать с целочисленным ID
            auth_login(request, user_instance)  # Стандартная функция входа
            
            return redirect('main')
        else:
            return render(request, 'shop/login_register.html', {'error': 'Неверный логин или пароль'})
    
    return render(request, 'shop/login_register.html')
# Регистрация
def register_view(request):
    if request.method == "POST":
        email = request.POST['email']
        name = request.POST['name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        password = request.POST['password']
        
        # Создаем нового пользователя
        new_user = Users(
            email=email,
            name=name,
            last_name=last_name,
            phone=phone,
            password=make_password(password),
        )
        new_user.save()
        
        return redirect('login')
    
    return render(request, 'shop/register.html')

@login_required
def profile_view(request):
    try:
        user = Users.objects.get(user_id=request.user.user_id)
    except Users.DoesNotExist:
        return redirect('login')  # Если пользователь не найден, перенаправляем на страницу авторизации

    return render(request, 'shop/profile.html', {'user': user})

def basket(request):
    pass

def orders(request):
    pass 

def profile(request):
    pass

def stock(request):
    pass