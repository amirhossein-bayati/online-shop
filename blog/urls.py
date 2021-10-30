from django.urls import path
from . import views
app_name = 'blog'


urlpatterns = [
    path('', views.homePage, name='home'),
    path('tag/<slug:tag_slug>', views.homePage, name='products_by_tag'),
    path('product/<int:pk>/<slug:slug>/', views.productDetail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update_item'),
    path('register/', views.registerPage.as_view(), name='register'),
    path('login/', views.loginPage.as_view(), name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('account/', views.accountPage, name='account'),
    path('search/', views.post_search, name='search'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
]
