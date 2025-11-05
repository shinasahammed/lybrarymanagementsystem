from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm, UserImageForm
from .models import User
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save user with default role = Customer
            user = form.save(commit=False)
            user.role = 'Customer' # enforce default role
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'logout.html')

# --------------------------
# Dashboard Routing
# --------------------------
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    if user.role == 'Staff':
        return redirect('staff_dashboard')
    elif user.role == 'Customer':
        return redirect('customer_dashboard')
    else:
        return redirect('login')  # fallback

# --------------------------
# Role-based Dashboards
# --------------------------

@login_required(login_url='login')
@user_passes_test(lambda u: u.role == 'Staff')
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.role == 'Customer')
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')





@login_required(login_url='login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user=user, data=request.POST)

        # Detect which form was submitted
        if 'update_profile' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('login')
    else:
        profile_form = ProfileForm(instance=user)
        password_form = PasswordChangeForm(user=user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form
    }
    return render(request, 'profile/profile.html', context)

#
# @login_required(login_url='login')
# def porfile(request):
#     return render(request, 'profile/firstprofile.html', {'user': request.user})




@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('firstprofile')  # or another page
    else:
        form = UserImageForm(instance=request.user)
    return render(request, 'profile/firstprofile.html', {'form': form})
