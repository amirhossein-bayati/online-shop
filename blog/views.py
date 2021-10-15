from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def homePage(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'blog/partials/content.html', context)

def productDetail(request, pk, slug):
    return HttpResponse("HI")