from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def find_us(request):
    return render(request, 'find_us.html')

def products(request):
    return render(request, 'products.html')

def categories(request):
    return render(request, 'categories.html')

def all_products(request):
    return render(request, 'all_products.html')

def cart(request):
    return render(request, 'cart.html')