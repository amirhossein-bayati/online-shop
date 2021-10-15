from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User



class Product(models.Model):
    STATUS_CHOICES = (
        ('publish', 'Publish'),
        ('draft', 'Draft'),
    )
    title = models.CharField(max_length=80)
    slug = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(null=True, blank=True)
    status = models.CharField(default='publish', max_length=20, choices=STATUS_CHOICES)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('blog:product_detail', args=[self.id, self.slug])
        return url

