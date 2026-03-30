from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-pizza-to-cart/<int:pizza_id>/', views.add_pizza_to_cart, name='add_pizza_to_cart'),
    path('add-drink-to-cart/<int:drink_id>/', views.add_drink_to_cart, name='add_drink_to_cart'),
    path('remove-from-cart/<int:item_index>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('locations/', views.locations, name='locations'),
    path('reorder/<int:order_id>/', views.reorder, name='reorder'),
]
