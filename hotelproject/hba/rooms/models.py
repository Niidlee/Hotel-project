from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User  

class RoomType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    user_name = models.CharField(max_length=250)
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField(default=timezone.now)
    num_rooms = models.PositiveIntegerField(default=1)
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    email = models.EmailField()
    phone = models.CharField(max_length=15, default='')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.username} - Room {self.room_type} ({'Booked' if self.is_booked else 'Available'})"

class BookingSettings(models.Model):
    booking_enable = models.BooleanField(default=True)
    confirmation_required = models.BooleanField(default=True)
    
    disable_weekend = models.BooleanField(default=True)
    available_booking_months = models.IntegerField(default=1, help_text="if 2, users can only book bookings for the next two months.")
    max_booking_per_day = models.IntegerField(null=True, blank=True)
    period_of_each_booking = models.CharField(max_length=3, default="30", help_text="How long each booking takes.") #one night
    max_booking_per_time = models.IntegerField(default=1, help_text="how many bookings can be made for each time.")
