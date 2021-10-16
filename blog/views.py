from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def homePage(request):
    products = Product.objects.filter(status='published')

    # Paginate Site With 6 Items Per A Page
    paginator = Paginator(products, 8)
    page = request.GET.get('page')

    # Post Of Certain Page
    try:
        products = paginator.page(page)

    # If Page Not Integer
    except PageNotAnInteger:
        products = paginator.page(1)

    # If Page NOt Exists
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'page': page,
    }
    return render(request, 'blog/partials/content.html', context)


def productDetail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug, status='published')
    # product = Product.objects.get(id=pk, slug=slug)
    context = {
        'product': product,
    }
    return render(request, 'blog/partials/product_detail.html', context)


def cart(request):
    context = {

    }
    return render(request, 'blog/partials/cart.html', context)