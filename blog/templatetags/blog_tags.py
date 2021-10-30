from django import template
from ..models import Product

register = template.Library()

@register.inclusion_tag('blog/top_products.html')
def show_top_products(count=4):
    top_products = Product.objects.filter().order_by('-ratings__average')[:4]
    return {"similar_products": top_products}



@register.inclusion_tag('blog/most_viewed_products.html')
def show_most_viewed_products(count=4):
    most_viewed_products = Product.objects.filter().order_by('-hits')[:4]
    return {"similar_products": most_viewed_products}


@register.simple_tag
def define(val=None):
  return val