from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from io import BytesIO
from django.utils.translation import gettext_lazy as _
from rooms.models import Booking
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from rooms.models import Booking

class Guest(models.Model):
    user = models.OneToOneField(User, null=True, verbose_name=_("Guest"), on_delete=models.CASCADE)
    phoneNumber = PhoneNumberField(unique=True)

    def __str__(self):
        return str(self.user)

    def num_of_booking(self):
        return Booking.objects.filter(guest=self).count()

    def num_of_days(self):
        total_day = 0
        bookings = Booking.objects.filter(guest=self)
        for b in bookings:
            day = b.endDate - b.startDate
            total_day += int(day.days)
        return total_day

    def num_of_last_booking_days(self):
        try:
            return int(
                (Booking.objects.filter(guest=self).last().endDate - Booking.objects.filter(guest=self).last().startDate).days)
        except:
            return 0

    def current_room(self):
        booking = Booking.objects.filter(guest=self).last()
        return booking.roomNumber


class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

    roomNumber = models.CharField(max_length=10)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return f"{self.guest} - Room {self.roomNumber}"

    def total_days(self):
        return (self.endDate - self.startDate).days

    def is_current(self):
        today = date.today()
        return self.startDate <= today <= self.endDate




