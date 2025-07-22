from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from . models import *
from datetime import date
from django.db.models import Count,Sum
from django.http import HttpResponse
from .ml import predict_maintenance


# Create your views here.
def is_admin(user):
    return user.is_superuser

def index(request):
    return render(request,"index.html")

@user_passes_test(is_admin)
def admin_home(request):
    total_users =User.objects.filter(is_superuser=False).count()
    total_garages =GarageProfile.objects.count()
    total_services =Service.objects.count()
    total_revenue =Booking.objects.filter(status='Completed').aggregate(total=Sum('service__price'))['total'] or 0

    top_services =(
        Service.objects.annotate(bookings=Count('booking')).order_by('-bookings')[:5]
    )

    peak_times = (
        Booking.objects
        .values('time')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    ) 
    return render(request,"admin_home.html",{
        'total_users': total_users,
        'total_garages': total_garages,
        'total_services': total_services,
        'total_revenue': total_revenue,
        'top_services': top_services,
        'peak_times': peak_times,
    })


def garage_home(request):
    return render(request,"garage_home.html")

def user_home(request):
    return render(request,"user_home.html")


def  user_register(request):
    if request.method =="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username Already Taken")
            return redirect("user_register")
        if confirm_password!=password:
            messages.error(request,"Password does not match")
            return redirect("user_register")
        User.objects.create_user(username=username,password=password)
        return redirect('login_page')
    return render(request,"user_register.html")


def garage_register(request):
    if request.method =="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        confirm_pass=request.POST.get("confirm_pass")
        name=request.POST.get("name")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username Already Taken")
            return redirect("garage_register")
        if confirm_pass!=password:
            messages.error(request,"Password does not match")
            return redirect("garage_register")
        if not phone.isdigit():
            messages.error(request,"Number must be digit")
            return redirect("garage_register")

        user=User.objects.create_user(username=username,password=password,email=email)
        GarageProfile.objects.create(user=user,name=name,address=address,phone=phone,is_approved=False)
        messages.info(request, "Registration successful. Wait for admin approval.")
        return redirect("login_page")
    return render(request, "garage_register.html")

def login_page(request):
    if request.method =="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            
            if user.is_superuser:
                return redirect('admin_home')
            try:
                garage=GarageProfile.objects.get(user=user)
                if garage.is_approved:
                    return redirect("garage_home")
                else:
                    messages.info(request,"You are Not Approved yet")
                    return redirect('login_page')
            except GarageProfile.DoesNotExist:
                return redirect("user_home")
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login_page')
    return render(request,"login_page.html")

@login_required
def logout_page(request):
    logout(request)
    return redirect('index')

@login_required
def add_vehicle_service(request):
    if request.method == 'POST':
        vehicle_type=request.POST.get("vehicle_type")
        model=request.POST.get("model")
        year=request.POST.get("year")
        km_run=request.POST.get("km_run")
        last_service_date=request.POST.get("last_service_date")

        Vehicle.objects.create(
            user=request.user,
            vehicle_type=vehicle_type,
            model=model,
            year=year,
            km_run=km_run,
            last_service_date=last_service_date
        )
        return redirect('user_home')
    return render(request, 'add_vehicle_service.html')

@login_required
def book_sevice(request):
    services=Service.objects.filter(garage__is_approved=True)
    if request.method == 'POST':
        service_id=request.POST.get("service")
        date=request.POST.get("date")
        time=request.POST.get("time")
        Type=request.POST.get("type")

        service=get_object_or_404(Service,id=service_id)

        Booking.objects.create(
            user=request.user,
            service=service,
            date=date,
            time=time,
            Type=Type
        
        )
        return redirect('user_home')
    return render(request, 'book_service.html', {'services': services})


@login_required
def view_service_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'service_history.html', {'bookings': bookings})


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        message=request.POST.get("message")
        Complaint.objects.create(
            user=request.user,
            message=message
        )
        return redirect('user_home')
    return render(request, 'complaints.html')

@login_required
def service_list(request):
    services=Service.objects.all()
    return render(request,"service_list.html",{'services':services})

@login_required
def service_view(request,service_id):
    garage=get_object_or_404(GarageProfile,user=request.user)
    service=get_object_or_404(Service,id=service_id,garage=garage)
    return render(request,"service_view.html",{'service':service})

@login_required
def add_service(request):
    garage=get_object_or_404(GarageProfile,user=request.user)
    if request.method == 'POST':
        name=request.POST.get("name")
        price=request.POST.get('price')
        duration= request.POST.get('duration')
       
        Service.objects.create(
            garage=garage,
            name=name,
            price=price,
            duration=duration
        )
        return redirect('garage_home')
    return render(request, 'add_service.html')


@login_required
def edit_service(request,service_id):
    garage=get_object_or_404(GarageProfile,user=request.user)
    service=get_object_or_404(Service,id=service_id,garage=garage)
    if request.method =="POST":
        service.name=request.POST.get('name',service.name)
        service.price=request.POST.get('price',service.price)
        service.duration=request.POST.get('duration',service.duration)
        service.save()
        messages.success(request,"service editted done")
        return redirect('service_view',service_id=service.id)
    return render(request,"edit_service.html",{'service':service})


@login_required
def delete_service(request,service_id):
    garage=get_object_or_404(GarageProfile,user=request.user)
    service=get_object_or_404(Service,id=service_id,garage=garage)
    service.delete()
    return redirect("service_list")


@login_required
def view_bookings(request):
    garage= GarageProfile.objects.get(user=request.user)
    bookings = Booking.objects.filter(service__garage=garage)
    return render(request, 'bookings.html', {'bookings': bookings})


@login_required
def update_booking_status(request, booking_id,status):
    VALID_STATUSES = ['Pending', 'In Progress', 'Completed', 'Cancelled']
    booking = get_object_or_404(Booking, id=booking_id)

    if status in VALID_STATUSES:
        booking.status=status
        booking.save()
        return redirect('view_bookings')
    return render(request, 'update_status.html', {'booking': booking})


@user_passes_test(is_admin)
def view_garage_requests(request):
    garages = GarageProfile.objects.filter(is_approved=False)
    return render(request, 'garage_requests.html', {'garages': garages})

@user_passes_test(is_admin)
def approve_garage_request(request,garage_id):
    garage=get_object_or_404(GarageProfile,id=garage_id)
    garage.is_approved=True
    garage.save()
    return redirect('view_garage_requests')

@user_passes_test(is_admin)
def reject_garage(request, garage_id):
    GarageProfile.objects.get(id=garage_id).delete()
    return redirect('view_garage_requests')


@user_passes_test(is_admin)
def view_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, 'complaint_list.html', {'complaints': complaints})

@user_passes_test(is_admin)
def view_users(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'view_users.html', {'users': users})


@user_passes_test(is_admin)
def view_all_services(request):
    services = Service.objects.select_related('garage')
    return render(request, 'view_services.html', {'services': services})


@user_passes_test(is_admin)
def view_all_garages(request):
    garages = GarageProfile.objects.all()
    return render(request, 'view_garages.html', {'garages': garages})


@login_required
def view_vehicles(request):
    vehicles=Vehicle.objects.filter(user=request.user)
    return render(request,"view_vehicles.html",{'vehicles':vehicles})


@login_required
def predict_risk(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)

    vehicle_age = date.today().year - vehicle.year

    if vehicle.last_service_date:
        last_service_days = (date.today() - vehicle.last_service_date).days
    else:
        last_service_days = 180 

    km_run = vehicle.km_run or 0

    try:
        result = predict_maintenance(vehicle_age, last_service_days, km_run)
    except Exception as e:
        return HttpResponse(f"Error: {e}")

    if result == 1:
        message = "🔧 High risk! Schedule maintenance soon."
    else:
        message = "✅ Vehicle is in good condition."

    return HttpResponse(message)