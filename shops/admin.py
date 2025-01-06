from django.contrib import admin
from .models import Shop

# @admin.register(Shop)
# class ShopAdmin(admin.ModelAdmin):
#     list_display = ('name', 'address', 'created_at')
    
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'shop_address', 'shop_contact', 'user', 'created_at')