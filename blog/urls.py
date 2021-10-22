from django.urls import path
from . import views
app_name = 'blog'


urlpatterns = [
    path('', views.homePage, name='home'),
    path('product/<int:pk>/<slug:slug>/', views.productDetail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update_item'),
    path('register/', views.registerPage.as_view(), name='register'),
    path('login/', views.loginPage.as_view(), name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('account/', views.accountPage, name='account'),
]
