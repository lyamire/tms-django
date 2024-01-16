from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products_list, name='products'),
    path('category/<int:category_id>/', views.category_details, name='category'),
    path('product/<int:product_id>/', views.product_details, name='detail'),
    path('product/<int:product_id>/add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete', views.cart_delete, name='cart_delete'),
]

