from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product


def homePage(request):
    products = Product.objects.filter(status='published')

    context = {
        'products': products,
    }
    return render(request, 'blog/partials/content.html', context)

def productDetail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug, status='published')
    # product = Product.objects.get(id=pk, slug=slug)
    context = {
        'product': product,
    }
    return render(request, 'blog/partials/product_detail.html', context)