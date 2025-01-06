from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from shops.models import Shop
from django.contrib.auth import authenticate, login
from django.template.context_processors import debug
from django.contrib import messages
from .forms import AdminLoginForm
from django.contrib.auth.models import User
from shops.models import Shop
from datetime import datetime


def is_admin(user):
    return user.is_staff

def custom_admin_login(request):
    form = AdminLoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_dashboard')  # Redirect to Django's admin panel
                else:
                    messages.error(request, 'You do not have superuser privileges.')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'adminpanel/admin_login.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    pending_shops_count = Shop.objects.filter(approved=False, declined=False).count()
    approved_shops_count = Shop.objects.filter(approved=True).count()
    users_count = User.objects.filter(is_active=True, is_staff=False).count()

    # Debugging: print the context
    context = {
        'pending_shops_count': pending_shops_count,
        'approved_shops_count': approved_shops_count,
        'users_count': users_count,
        'year': datetime.now().year
    }
    print(context)  # Print the context for debugging
    return render(request, 'adminpanel/admin_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def approve_users(request):
    # Query to fetch pending approval shops (approved=False, declined=False)
    pending_shops = Shop.objects.filter(approved=False, declined=False)
    pending_count = pending_shops.count()  # Count of pending shops

    # Pass both the pending shops and the count to the template
    return render(request, 'adminpanel/approve_users.html', {
        'pending_shops': pending_shops,
        'pending_count': pending_count
    })

@user_passes_test(lambda u: u.is_superuser)
def user_approval(request, shop_id):
    # Get the shop by ID
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            shop.approved = True  # Approve the shop
            shop.user.is_active = True  # Optionally, activate the associated user
            shop.user.save()
            shop.save()
            shop.refresh_from_db()
            # messages.success(request, f'Shop {shop.shop_name} has been approved.')
        elif action == 'decline':
            shop.approved = False  # Decline the shop approval
            shop.declined = True  # Mark shop as declined (new field)
            shop.user.is_active = False  # Optionally, deactivate the associated user
            shop.user.save()
            shop.save()
            # messages.warning(request, f'Shop {shop.shop_name} has been declined.')

        return redirect('approve_users')

    return render(request, 'adminpanel/user_approval.html', {'shop': shop})



@user_passes_test(lambda u: u.is_superuser)
def approval_status(request):
    approved_users = User.objects.filter(is_active=True)
    return render(request, 'adminpanel/approval_status.html', {'approved_users': approved_users})

@user_passes_test(lambda u: u.is_superuser)
def manage_shops(request):
    approved_shops = Shop.objects.filter(approved=True)
    return render(request, 'adminpanel/manage_shops.html', {'approved_shops': approved_shops})

@user_passes_test(lambda u: u.is_superuser)
def delete_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        shop_name = shop.shop_name
        shop.delete()
        # messages.success(request, f"{shop_name} has been deleted successfully.")
        return redirect('manage_shops')

    return render(request, 'adminpanel/delete_shop.html', {'shop': shop})


