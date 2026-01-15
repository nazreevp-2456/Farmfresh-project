from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Account created successfully! Please log in.'
            )
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ ROLE-BASED REDIRECT
            if user.profile.role == 'farmer':
                return redirect('farmer_dashboard')
            else:
                return redirect('home')  # customer home

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html')



def user_logout(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')


@login_required
def farmer_dashboard(request):
    if request.user.profile.role != 'farmer':
        return redirect('home')

    # ✅ Count unread notifications
    notifications_count = request.user.notifications.filter(is_read=False).count()

    # ✅ Optionally, get all notifications
    all_notifications = request.user.notifications.order_by('-created_at')

    # ✅ Pass to template
    return render(request, 'users/farmer_dashboard.html', {
        'notifications_count': notifications_count,
        'all_notifications': all_notifications,
    })


@login_required
def customer_home(request):
    if request.user.profile.role != 'customer':
        messages.error(request, 'Access denied!')
        return redirect('home')

    notifications_count = request.user.notifications.filter(is_read=False).count()
    all_notifications = request.user.notifications.order_by('-created_at')

    return render(request, 'users/customer_home.html', {
        'notifications_count': notifications_count,
        'all_notifications': all_notifications,
    })

