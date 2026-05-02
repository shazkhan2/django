from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm


# ---------------------------
# LOGIN VIEW
# ---------------------------

def login_user(request):
    if request.user.is_authenticated:
        return redirect('tours:index')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('tours:index')

        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/index.html')


# ---------------------------
# LOGOUT VIEW
# ---------------------------

def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('index')


# ---------------------------
# REGISTER VIEW
# ---------------------------

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'driver'
            user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, "You have successfully registered.")
            return redirect('tours:index')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {
        'form': form
    })