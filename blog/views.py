from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from .models import *

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
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, coplete=False)
        items = OrderItem.objects.filter(order=order)
    else:
        items = []
        order = {
            'get_total_price': 0,
            'get_total_products': 0,
        }
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'blog/partials/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, coplete=False)
        items = OrderItem.objects.filter(order=order)
    else:
        items = []
        order = {
            'get_total_price': 0,
            'get_total_products': 0,
        }
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'blog/partials/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=request.user.customer, coplete=False)
    orderItem, created = OrderItem.objects.get_or_create(product=product, order=order)


    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('update item', safe=False)