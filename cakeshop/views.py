from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from shops.models import Shop, Cake, Order
from users.models import CartItem
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Home view for general visitors
def home(request):
    cafes = Shop.objects.filter(approved=True)
    return render(request, 'cakeshop/home.html', {'cafes': cafes})

