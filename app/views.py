from django.shortcuts import render, redirect

from app.forms import ProductModelForm
from app.models import Product


# Create your views here.
def index(request):
    products = Product.objects.all().order_by('-id')
    context = {
        'products': products
    }
    return render(request, 'product/index.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    attributes = product.get_attributes()
    contex = {
        'product': product,
        'attributes': attributes
    }
    return render(request, 'product/product-detail.html', contex)


# def add_product(request):
#     form = ProductForm()
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         name = request.POST['name']
#         description = request.POST['description']
#         price = request.POST['price']
#         rating = request.POST['rating']
#         discount = request.POST['discount']
#         quantity = request.POST['quantity']
#         product = Product(name=name, description=description, price=price, rating=rating, discount=discount,
#                           quantity=quantity)
#         if form.is_valid():
#             product.save()
#             return redirect('index')
#
#     context = {
#         'form': form
#     }
#     return render(request, 'app/add-product.html', context)

def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form,
    }
    return render(request, 'product/add-product.html', context)
