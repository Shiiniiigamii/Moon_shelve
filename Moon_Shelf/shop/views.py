from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def main(request):
    books = Books.objects.all()
    return render(request, 'shop/books.html', {'books': books})

def books(request):
    pass

def basket(request):
    pass

def orders(request):
    pass 

def profile(request):
    pass

def stock(request):
    pass