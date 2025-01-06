from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Shop, Cake, Order, Review
from django.db import models

# Shop Owner Login View
def shop_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('shop_dashboard')  # Redirect to shop owner dashboard after successful login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'shops/shop_login.html')

# Shop Owner Signup View
def shop_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        shop_name = request.POST['shop_name']
        shop_address = request.POST['shop_address']
        shop_contact = request.POST['shop_contact']
        shop_description = request.POST.get('shop_description', '')
        shop_logo = request.FILES.get('shop_logo', None)
        created_at = models.DateTimeField(auto_now_add=True)  # Automatically add timestamp when created

        # Server-side validations
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('shop_signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect('shop_signup')
            else:
                # Create a new shop owner user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Create a shop profile
                Shop.objects.create(
                    user=user,
                    shop_name=shop_name,
                    shop_address=shop_address,
                    shop_contact=shop_contact,
                    shop_description=shop_description,
                    shop_logo=shop_logo
                )

                messages.success(request, 'Your account has been created and is pending admin approval.')
                return redirect('shop_login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('shop_signup')

    return render(request, 'shops/shop_signup.html')

@login_required
def shop_dashboard(request):
    shop = get_object_or_404(Shop, user=request.user)
    cakes = Cake.objects.filter(shop=shop)
    return render(request, 'shops/shop_dashboard.html', {'shop': shop, 'cakes': cakes})

@login_required
def manage_shop_menu(request):
    shop = get_object_or_404(Shop, user=request.user)
    menu_items = Cake.objects.filter(shop=shop)
    return render(request, 'shops/shop_manage_menu.html', {'shop': shop, 'menu_items': menu_items})

@login_required
def add_cake(request):
    shop = get_object_or_404(Shop, user=request.user)
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        image = request.FILES['image']

        Cake.objects.create(
            shop=shop,
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image
        )
        # messages.success(request, 'Cake added successfully.')
        return redirect('manage_shop_menu')

    return render(request, 'shops/add_cake.html')


@login_required
def update_cake(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id, shop__user=request.user)
    if request.method == 'POST':
        cake.name = request.POST['name']
        cake.description = request.POST['description']
        cake.price = request.POST['price']
        cake.stock = request.POST['stock']
        if 'image' in request.FILES:
            cake.image = request.FILES['image']
        cake.save()
        # messages.success(request, 'Cake updated successfully.')
        return redirect('manage_shop_menu')

    return render(request, 'shops/update_cake.html', {'cake': cake})


@login_required
def delete_cake(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id, shop__user=request.user)
    if request.method == 'POST':
        cake.delete()
        # messages.success(request, 'Cake deleted successfully.')
        return redirect('manage_shop_menu')

    return render(request, 'shops/delete_cake.html', {'cake': cake})

def list_shops(request):
    shops = Shop.objects.filter(approved=True)  # Only show approved shops
    return render(request, 'shops/list_shops.html', {'shops': shops})

def shop_menu(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, approved=True)  # Only approved shops
    menu_items = Cake.objects.filter(shop=shop)  # Use Cake model for the shop's menu
    return render(request, 'shops/shop_menu.html', {'shop': shop, 'menu_items': menu_items})

@login_required
def manage_orders(request):
    # Get the shop owned by the currently logged-in user
    shop = get_object_or_404(Shop, user=request.user)

    # Separate orders: "Out for Delivery" and others
    out_for_delivery_orders = Order.objects.filter(cake__shop=shop, status='Out for Delivery')
    other_orders = Order.objects.filter(cake__shop=shop).exclude(status='Out for Delivery')

    return render(request, 'shops/manage_orders.html', {
        'out_for_delivery_orders': out_for_delivery_orders,
        'other_orders': other_orders,
    })

@login_required
def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id, cake__shop__user=request.user)
        new_status = request.POST.get("status")

        # Validate allowed statuses
        allowed_statuses = ['Pending', 'Processing', 'Confirmed', 'Out for Delivery', 'Completed', 'Cancelled']

        # Prevent changes to 'Completed' or 'Cancelled' statuses
        if order.status in ['Completed', 'Cancelled']:
            messages.error(request, f"Order {order.id} has already been marked as {order.status} and cannot be updated.")
            return redirect('manage_orders')

        if new_status in allowed_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status update.")

    return redirect('manage_orders')

@login_required
def shop_reviews(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, user=request.user)
    reviews = Review.objects.filter(cake__shop=shop).select_related('cake', 'user')

    return render(request, 'shops/shop_reviews.html', {'shop': shop, 'reviews': reviews})
