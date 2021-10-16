from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# # with method of manager
# class PostManager(models.Manager):
#     def get_published(self):
#         return self.filter(status='published')
#
#
# class ProductPublishManager(models.Manager):
#     def get_queryset(self):
#         return super(ProductPublishManager, self).get_queryset().filter(status='published')


class Product(models.Model):
    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    title = models.CharField(max_length=80)
    slug = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(null=True, blank=True)
    status = models.CharField(default='published', max_length=20, choices=STATUS_CHOICES)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # published = ProductPublishManager()
    # objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('blog:product_detail', args=[self.id, self.slug])
        return url

