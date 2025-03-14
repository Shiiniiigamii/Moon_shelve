from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse


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

def catalog_view(request, category_id=None, subcategory_id=None):
    categories = Category.objects.all()
    subcategories = None
    books = Books.objects.all()

    selected_category = None
    selected_subcategory = None

    # Фильтрация по категории
    if category_id:
        selected_category = get_object_or_404(Category, category_id=category_id)
        subcategories = Subcategory.objects.filter(category=selected_category)  # Подкатегории для выбранной категории
        books = Books.objects.filter(category=selected_category)  # Книги для выбранной категории

    # Фильтрация по подкатегории
    if subcategory_id:
        selected_subcategory = get_object_or_404(Subcategory, subcategory_id=subcategory_id)
        books = books.filter(subcategory=selected_subcategory)  # Книги для выбранной подкатегории

    context = {
        "categories": categories,
        "subcategories": subcategories,
        "books": books,
        "selected_category": selected_category,
        "selected_subcategory": selected_subcategory
    }

    return render(request, "shop/catalog.html", context)

def search_suggestions(request):
    """Возвращает подсказки при поиске книг."""
    query = request.GET.get("q", "").strip()
    if query:
        books = Books.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )[:5]
        data = [{"title": book.title, "author": book.author.name} for book in books]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def search_results(request):
    """Вывод результатов поиска на новой странице."""
    query = request.GET.get("q", "").strip()
    books = []
    if query:
        books = Books.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    return render(request, "shop/search_results.html", {"books": books, "query": query})

def basket(request):
    pass

def orders(request):
    pass 

def profile(request):
    pass

def stock(request):
    pass