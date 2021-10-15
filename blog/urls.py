from django.urls import path
from . import views
app_name = 'blog'


urlpatterns = [
    path('', views.homePage, name='home'),
    path('product/<int:pk>/<slug:slug>/', views.productDetail, name='product_detail')
]
