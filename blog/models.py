from django.db import models
from django.utils import timezone


class Product(models.Model):
    STATUS_CHOICES = (
        ('publish', 'Publish'),
        ('draft', 'Draft'),
    )
    title = models.CharField(max_length=80)
    slug = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(max_length=500)
    image = models.ImageField(null=True, blank=True)
    status = models.CharField(default='publish', max_length=20)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

