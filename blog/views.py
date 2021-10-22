from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
import json

from django.urls import reverse_lazy

from .models import *

from .forms import CreateUserForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import FormView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import logout




def homePage(request):
    products = Product.objects.filter(status='published')
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, coplete=False)
        order_items_count = order.get_total_products
    else:
        order_items_count = 0
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
        'order_items_count':  order_items_count,
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
    order_items_count = order.get_total_products
    context = {
        'items': items,
        'order': order,
        'order_items_count': order_items_count,
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
    order_items_count = order.get_total_products
    context = {
        'items': items,
        'order': order,
        'order_items_count': order_items_count,
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
    elif action == "delete":
        orderItem.delete()

    orderItem.save()
    if action == "delete":
        orderItem.delete()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('update item', safe=False)


class registerPage(FormView):
    template_name = 'blog/account/register.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('blog:login')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('blog:home')
        return super().get(*args, **kwargs)


    def form_valid(self, form):
        user = form.save()
        email = form.cleaned_data['email']
        customer = Customer.objects.create(user=user, email=email)
        return super().form_valid(form)


class loginPage(LoginView):
    template_name = 'blog/account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('blog:home')

    def form_invalid(self, form):
        messages.error(self.request, 'Username or password is Incorrect')
        return super().form_invalid(self)


def logoutPage(request):
    logout(request)
    return redirect('blog:login')



def accountPage(request):
    context = {

    }
    return render(request, 'blog/account/account.html', context)