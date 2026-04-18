from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import Group

def index(request):
    if request.method == "POST":
        # username = request.POST['username']
        # password = request.POST['password']
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('index')

    else:
        return render(request, 'users/index.html')



def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('index')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.user_type = 'driver'
            form.save()
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered.")
            return redirect('index')
    else:
        form= SignUpForm()
    return render(request, 'users/register.html', {
        'form': form
            })
    
    
            