from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return render(request, 'shop/books.html')

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