import os

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

from taggit.managers import TaggableManager

from django.core.validators import MinValueValidator, MaxValueValidator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.title}{ext}"
    return f"products/{instance.author}/{final_name}"


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='media/', blank=True, default='man.png')
    email = models.EmailField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    ip_address = models.OneToOneField(IPAddress, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    coplete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    coupons = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def get_total_products(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

    @property
    def get_total_price(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total_price for item in orderItems])
        return total


    @property
    def get_last_total_price(self):
        total = self.get_total_price
        if self.coupons:
            total -= self.coupons.discount

        if total < 0:
            total = 0
        return total


class Delivery(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    active = models.BooleanField()



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    title = models.CharField(max_length=80)
    slug = models.CharField(max_length=100)
    price = models.FloatField()
    offPrice = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(null=True, blank=True)
    status = models.CharField(default='published', max_length=20, choices=STATUS_CHOICES)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ratings = GenericRelation(Rating, related_query_name='products')
    hits = models.ManyToManyField(IPAddress, blank=True, related_name='hits')
    tags = TaggableManager()

    # published = ProductPublishManager()
    # objects = PostManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('blog:product_detail', args=[self.id, self.slug])
        return url


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        if self.product.offPrice:
            price = self.quantity * self.product.offPrice
        else:
            price = self.quantity * self.product.price
        return price
