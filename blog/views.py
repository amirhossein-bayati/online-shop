from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
import json

from django.urls import reverse_lazy

from .models import *

from .forms import CreateUserForm, AccountForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import FormView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import logout

from django.db.models import Q

from django.db.models import Count


import random

from taggit.models import Tag

from django.contrib.auth.decorators import login_required






def homePage(request, tag_slug=None):
    products = Product.objects.filter(status='published')
    tag =None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = Product.objects.filter(tags__in=[tag])

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

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, coplete=False)
        order_items_count = order.get_total_products

        user_ip = request.user.customer.ip_address
        if user_ip not in product.hits.all():
            product.hits.add(user_ip)
    else:
        order_items_count = 0

    product_tags = product.tags.values_list('id', flat=True)
    similar_products = Product.objects.filter(tags__in=product_tags, status='published').exclude(id=product.id)
    # print(similar_products)
    similar_products = similar_products.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {
        'product': product,
        'similar_products': similar_products,
        'order_items_count': order_items_count,

    }
    return render(request, 'blog/partials/product_detail.html', context)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, coplete=False)
        items = OrderItem.objects.filter(order=order)
        delivery = Delivery.objects.filter(active=True)
        if request.method == "POST":
            now = timezone.now()
            code = request.POST['code']

            try:
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                order.coupons = coupon
                order.save()
                off = coupon.discount
                messages.success(request, f"Discount: -${off}")


            except:
                messages.info(request, "Invalid Coupon")


    else:
        items = []
        order = {
            'get_total_price': 0,
            'get_total_products': 0,
        }
        return redirect('blog:login')
    order_items_count = order.get_total_products

    context = {
        'items': items,
        'order': order,
        'order_items_count': order_items_count,
        'delivery': delivery,
    }
    return render(request, 'blog/partials/cart.html', context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, coplete=False)
        items = OrderItem.objects.filter(order=order)
        if not (customer.first_name and customer.last_name and customer.address and customer.email and customer.phone):
            messages.error(request, 'complete your personal information')
            return redirect('blog:cart')
    else:
        items = []
        order = {
            'get_total_price': 0,
            'get_total_products': 0,
        }
        return redirect('blog:login')
    order_items_count = order.get_total_products
    context = {
        'items': items,
        'order': order,
        'order_items_count': order_items_count,
        'customer': customer,
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


@login_required
def logoutPage(request):
    logout(request)
    return redirect('blog:login')


@login_required
def accountPage(request):
    customer = request.user.customer
    order_history = Order.objects.filter(customer=customer, coplete=True)
    if request.method == "POST":
        accForm = AccountForm(data=request.POST)
        if accForm.is_valid():
            accForm = AccountForm(data=request.POST)
            if accForm.is_valid():
                cd = accForm.cleaned_data
                customer.first_name = cd['first_name']
                customer.last_name = cd['last_name']
                customer.email = cd['email']
                customer.phone = cd['phone']
                customer.address = cd['address']
                image = request.FILES.get('image')
                if image:
                    customer.image = image
                customer.save()
                return redirect('blog:account')
    else:
        accForm = AccountForm()
    context = {
        'customer': customer,
        'accForm': accForm,
        'order_history': order_history,
    }
    return render(request, 'blog/account/account.html', context)


def post_search(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        lookup = Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__name__icontains=query)
        products = Product.objects.filter(lookup, status='published')
    else:
        products = {}
    context = {
        'products': products,
    }
    return render(request, 'blog/partials/content.html', context)


@login_required
def payment(request):
    print(request)
    return render(request, 'blog/partials/payment.html')


@login_required
def payment_success(request):
    customer = request.user.customer
    transaction_id = random.randint(10000, 100000)

    order = Order.objects.get(customer=customer, coplete=False)
    order.transaction_id = transaction_id
    order.coplete = True
    order.save()

    return redirect('blog:account')