from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Tour
from .forms import TourForm
from django.contrib.auth import get_user_model

User = get_user_model()

def is_dispatcher(user):
    return user.is_authenticated and user.user_type == 'dispatcher'

def is_driver(user):
    return user.is_authenticated and user.user_type == 'driver'

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def index(request):
    if request.user.is_staff:
        return redirect('tours:admin_dashboard')
    if request.user.user_type == 'dispatcher':
        return redirect('tours:dispatcher_dashboard')
    if request.user.user_type == 'driver':
        return redirect('tours:driver_dashboard')
    return render(request, 'tours/index.html')

@login_required
@user_passes_test(is_dispatcher, login_url='/')
def dispatcher_dashboard(request):
    tours = Tour.objects.filter(created_by=request.user).order_by('-pickup_time')
    return render(request, 'tours/dispatcher_dashboard.html', {'tours': tours})

@login_required
@user_passes_test(is_driver, login_url='/')
def driver_dashboard(request):
    tours = Tour.objects.filter(driver=request.user).order_by('-pickup_time')
    return render(request, 'tours/driver_dashboard.html', {'tours': tours})

@login_required
@user_passes_test(is_admin, login_url='/')
def admin_dashboard(request):
    tours = Tour.objects.all().order_by('-pickup_time')
    drivers = User.objects.filter(user_type='driver')
    return render(request, 'tours/admin_dashboard.html', {
        'tours': tours,
        'drivers': drivers
    })

@login_required
@user_passes_test(is_dispatcher, login_url='/')
def create_tour(request):
    if request.method == "POST":
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.created_by = request.user
            tour.save()
            return redirect('tours:dispatcher_dashboard')
    else:
        form = TourForm()
    return render(request, 'tours/create_tour.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='/')
def assign_driver(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    drivers = User.objects.filter(user_type='driver')
    if request.method == "POST":
        driver_id = request.POST.get('driver')
        driver = get_object_or_404(User, id=driver_id)
        tour.driver = driver
        tour.status = 'assigned'
        tour.save()
        return redirect('tours:admin_dashboard')
    return render(request, 'tours/assign_driver.html', {'tour': tour, 'drivers': drivers})

@login_required
@user_passes_test(is_driver, login_url='/')
def complete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if tour.driver == request.user:
        tour.status = 'completed'
        tour.save()
    return redirect('tours:driver_dashboard')

@login_required
@user_passes_test(is_admin, login_url='/')
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect('tours:admin_dashboard')

@login_required
@user_passes_test(is_admin, login_url='/')
def update_tour_status(request, tour_id):
    tour=get_object_or_404(Tour, id=tour_id)
    if request.method=="POST":
        new_status=request.POST.get('status')
        if new_status in dict(Tour.STATUS_CHOICES):
            tour.status=new_status
            tour.save()
    return redirect('tours:admin_dashboard')