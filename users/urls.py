# users/urls.py
from django.urls import path
from . import views
from .views import cake_detail
from .views import customer_orders
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
   
    path('signup/', views.customer_signup, name='customer_signup'),  # Customer Signup
    path('login/', views.customer_login, name='customer_login'),  # Customer Login
    path('add_to_cart/<int:cake_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/add/<int:cake_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),   
    path('payment/', views.payment, name='payment'),  # Add payment route
    path('payment/process/', views.process_payment, name='process_payment'),
    path('list-shops/', views.list_shops, name='list_shops'),
    path('profile/', views.customer_profile, name='customer_profile'),
    path('orders/', customer_orders, name='customer_orders'),
    path('cakes/<int:cake_id>/', cake_detail, name='cake_detail'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
