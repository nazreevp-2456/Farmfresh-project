from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product
from users.models import Profile
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages

from django.shortcuts import redirect

def root_redirect(request):
    return redirect('login')  # or 'home'


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def farmer_dashboard(request):
    products = Product.objects.filter(farmer=request.user)
    return render(request, 'store/farmer_dashboard.html', {
        'products': products
    })



@login_required
def my_products(request):
    if request.user.profile.role != 'farmer':
        return redirect('home')

    products = Product.objects.filter(farmer=request.user)
    return render(request, 'store/my_products.html', {'products': products})


@login_required
def browse_products(request):
    if request.user.profile.role != 'customer':
        return redirect('home')

    products = Product.objects.all()
    return render(request, 'store/browse_products.html', {'products': products})

@login_required
def add_product(request):
    profile = request.user.profile

    if profile.role != 'farmer':
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()

            messages.success(request, "Product added successfully!")
            return redirect('my_products')
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {
        'form': form
    })
