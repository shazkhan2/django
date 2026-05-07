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
    sort_by = request.GET.get('sort', 'pickup_time')
    sort_map = {
        'passenger': 'passenger_name',
        '-passenger': '-passenger_name',
        'time': 'pickup_time',
        '-time': '-pickup_time',      
        'status': 'status',
        '-status': '-status',
        'driver': 'driver__username',
        '-driver': '-driver__username',
    }
    order_field = sort_map.get(sort_by, '-pickup_time')
    tours = Tour.objects.all().order_by(order_field)
    drivers = User.objects.filter(user_type='driver')
    drivers_count = drivers.count()
    total_count = tours.count()
    pending_count = tours.filter(status='pending').count()
    assigned_count = tours.filter(status='assigned').count()
    completed_count = tours.filter(status='completed').count()
    
    def get_percent(count):
        return (count / total_count * 100) if total_count > 0 else 0
    
    return render(request, 'tours/admin_dashboard.html', {
        'tours': tours,
        'drivers': drivers,
        'drivers_count': drivers_count,
        'pending_tours_count': pending_count,
        'assigned_tours_count': assigned_count,
        'completed_tours_count': completed_count,
        'pending_pct': get_percent(pending_count),
        'assigned_pct': get_percent(assigned_count),
        'completed_pct': get_percent(completed_count),
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
            if new_status == 'pending':
                tour.driver = None
            tour.save()
    return redirect('tours:admin_dashboard')