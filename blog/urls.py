from django.urls import path
from . import views
app_name = 'blog'


urlpatterns = [
    path('', views.homePage, name='home'),
    path('product/<int:pk>/<slug:slug>/', views.productDetail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update_item'),

]
