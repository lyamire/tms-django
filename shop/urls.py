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
    path('cart/delete/<int:product_id>', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('cart/update/<int:product_id>/count', views.update_product_from_cart, name='update_product_from_cart'),
    path('cart/submit', views.cart_submit, name='cart_submit'),
    path('profile/', views.profile_details, name='profile'),
    path('profile/history/', views.profile_history_of_orders, name='profile_history_of_orders'),
    path('profile/<int:order_id>/', views.order_details, name='order_details'),
    path('profile/<int:order_id>/reorder', views.reorder, name='reorder')
]

