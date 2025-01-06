from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
# from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_view, name='login'),
    # path('signup/', views.signup, name='signup'),
    # path('cafe/<int:cafe_id>/', views.cafe_detail, name='cafe_detail'),
    # path('search/', views.search, name='search'),  # Add the search view URL
    # path('add_to_cart/<int:cake_id>/', views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart, name='cart'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('orders/', views.orders, name='orders'),
    # path('add-restaurant/', views.add_restaurant, name='add_restaurant'),
    # path('add_review/<int:cake_id>/', views.add_review, name='add_review'),
#     path('logout/', views.custom_logout, name='logout'),
    #  path('logout/', LogoutView.as_view(), name='logout'),
     path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
 ]
