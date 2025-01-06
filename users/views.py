# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from shops.models import Cake, Shop, Order, Review
from .forms import ReviewForm
from decimal import Decimal
from django.contrib.auth.hashers import check_password

def customer_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
            else:
                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = True  # Set user to active (optional)
                user.save()
                messages.success(request, 'Account created successfully! You can now login.')
                return redirect('customer_login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'users/customer_signup.html')



def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:  # Check if the user is active
                login(request, user)
                return redirect('list_shops')  # Redirect to the list of shops
            else:
                messages.error(request, 'Your account is inactive. Please contact support.')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'users/customer_login.html')


@login_required
def add_to_cart(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    if cake.stock < 1:
        messages.error(request, "This cake is out of stock.")
        return redirect('shop_menu', shop_id=cake.shop.id)

    # Get or create the cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create a cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, cake=cake)
    if not created:
        cart_item.quantity += 1  # Increment quantity if already exists
    cart_item.save()

    # Debugging logs
    print(f"CartItem created/updated: {cart_item}")
    print(f"Cart now contains: {[item.cake.name for item in cart.items.all()]}")

    # messages.success(request, f"{cake.name} has been added to your cart.")
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('cake')

    # Pre-calculate totals for each cart item
    cart_items_with_totals = []
    total_price = 0
    for item in cart_items:
        item_total = item.cake.price * item.quantity
        total_price += item_total
        cart_items_with_totals.append({
            'id': item.id,
            'cake': item.cake,
            'quantity': item.quantity,
            'item_total': item_total
        })

    # Debugging logs
    print(f"Cart contains: {cart_items_with_totals}")
    print(f"Total cart price: ₹{total_price}")

    return render(request, 'users/cart.html', {
        'cart_items_with_totals': cart_items_with_totals,
        'total_price': total_price
    })

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    # messages.success(request, "Item removed from your cart.")
    return redirect('view_cart')

login_required
def update_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(cart.items, id=item_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

    return redirect('view_cart')

@login_required
def checkout(request):
    # Fetch the user's cart
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('cake')

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    # Calculate total amount
    total_amount = Decimal(0)
    cart_items_data = []
    for item in cart_items:
        if item.cake.stock < item.quantity:
            messages.error(request, f"Not enough stock for {item.cake.name}.")
            return redirect('view_cart')

        item_total_price = item.cake.price * item.quantity
        total_amount += item_total_price

        cart_items_data.append({
            'cake_id': item.cake.id,
            'quantity': item.quantity,
            'total_price': float(item_total_price),  # Convert Decimal to float
        })

    # Save total amount and cart items in session
    request.session['total_amount'] = float(total_amount)  # Convert Decimal to float
    request.session['cart_items'] = cart_items_data

    # messages.success(request, "Proceed to payment.")
    return redirect('payment')



@login_required
def payment(request):
    # Retrieve the total amount from the session
    total_amount = request.session.get('total_amount', 0)

    # Debugging logs
    print(f"Total payment amount from session: ₹{total_amount}")

    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    years = [str(year) for year in range(2025, 2031)]

    return render(request, 'users/payment.html', {
        'total_amount': total_amount,
        'months': months,
        'years': years
    })

@login_required
def process_payment(request):
    if request.method == "POST":
        # Simulate payment validation
        card_number = request.POST.get('card_number', '')
        if len(card_number) != 16 or not card_number.isdigit():
            messages.error(request, "Invalid card number. Please enter a valid 16-digit card number.")
            return redirect('payment')

        payment_success = True  # Simulate payment success

        if payment_success:
            # Create orders from session data
            cart_items = request.session.get('cart_items', [])
            for item in cart_items:
                cake = get_object_or_404(Cake, id=item['cake_id'])
                Order.objects.create(
                    customer=request.user,
                    cake=cake,
                    quantity=item['quantity'],
                    total_price=item['total_price'],
                    status='Pending'
                )
                # Deduct stock
                cake.stock -= item['quantity']
                cake.save()

            # Clear session data
            request.session.pop('total_amount', None)
            request.session.pop('cart_items', None)

            # Clear cart
            Cart.objects.filter(user=request.user).delete()

            # Redirect to order confirmation page
            return redirect('order_confirmation')

        else:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('payment')

    return redirect('home')

@login_required
def order_confirmation(request):
    return render(request, 'users/order_confirmation.html')


@login_required
def list_shops(request):
    shops = Shop.objects.filter(approved=True)  # Only approved shops
    return render(request, 'users/customer_dashboard.html', {'shops': shops})


@login_required
def customer_profile(request):
    user = request.user

    if request.method == "POST":
        email = request.POST.get("email")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check and update email
        if email and email != user.email:
            user.email = email

        # Validate and update password
        if old_password and new_password:
            if not check_password(old_password, user.password):
                messages.error(request, "Old password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            elif old_password == new_password:
                messages.error(request, "New password cannot be the same as the old password.")
            else:
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # Keep user logged in after password change
                # messages.success(request, "Your password has been updated successfully.")

        user.save()
        # messages.success(request, "Your profile has been updated successfully.")
        return redirect("customer_profile")  # Redirect back to the profile page

    return render(request, "users/customer_profile.html")
@login_required
def customer_orders(request):
    orders = Order.objects.filter(customer=request.user).select_related('cake__shop')
    return render(request, 'users/customer_orders.html', {'orders': orders})

@login_required
def cake_detail(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    shop = cake.shop
    reviews = Review.objects.filter(cake=cake).select_related('user')

    # Handle review submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.cake = cake
            review.save()
            # messages.success(request, "Your review has been submitted.")
            return redirect('cake_detail', cake_id=cake.id)
    else:
        form = ReviewForm()

    return render(request, 'users/cake_detail.html', {'cake': cake,'shop': shop, 'reviews': reviews, 'form': form})



