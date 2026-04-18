from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.location_select, name='location_select'),
    path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('check-email/', views.check_email, name='check_email'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('profile/', views.profile, name='profile'),

    
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='orders/password_reset.html',
        email_template_name='orders/password_reset_email.html',
        subject_template_name='orders/password_reset_subject.txt'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='orders/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='orders/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='orders/password_reset_complete.html'
    ), name='password_reset_complete'),
]