from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GarageProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    km_run = models.PositiveIntegerField(default=0)
    last_service_date = models.DateField(null=True, blank=True) 

    def __str__(self):
        return f"{self.vehicle_type} - {self.model}"
    

class Service(models.Model):
    garage = models.ForeignKey(GarageProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    Type = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    estimated_completion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"
    


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)