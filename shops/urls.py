# shops/urls.py
from django.urls import path
from . import views
from .views import shop_reviews
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.shop_login, name='shop_login'),
    path('signup/', views.shop_signup, name='shop_signup'),
    path("dashboard/", views.shop_dashboard, name="shop_dashboard"),
    path('add-cake/', views.add_cake, name='add_cake'),
    path('update-cake/<int:cake_id>/', views.update_cake, name='update_cake'),
    path('delete-cake/<int:cake_id>/', views.delete_cake, name='delete_cake'),
    path('shops/', views.list_shops, name='list_shops'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('<int:shop_id>/menu/', views.shop_menu, name='shop_menu'),
    path('manage-menu/', views.manage_shop_menu, name='manage_shop_menu'),
    path('shop/<int:shop_id>/reviews/', shop_reviews, name='shop_reviews'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ]
