# adminpanel/urls.py
from django.urls import path
from . import views
from .views import custom_admin_login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', custom_admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-users/', views.approve_users, name='approve_users'),
    path('manage-shops/', views.manage_shops, name='manage_shops'),  # New URL
    path('approval-status/', views.approval_status, name='approval_status'),
    path('approve-user/<int:shop_id>/', views.user_approval, name='user_approval'),
    path('delete-shop/<int:shop_id>/', views.delete_shop, name='delete_shop'),
    path('users/logout/', LogoutView.as_view(), name='logout'),

]
