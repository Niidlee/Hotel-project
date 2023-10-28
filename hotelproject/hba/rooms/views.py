from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking, RoomType
from .forms import BookingForm, RoomTypeForm

def room_types(request):
    if request.method == 'POST':
        room_type_form = RoomTypeForm(request.POST)
        if room_type_form.is_valid():
            room_type_form.save()
            return redirect('rooms:room_types')
        else:
            print(room_type_form.errors)
    else:
        room_type_form = RoomTypeForm()

    room_types = RoomType.objects.all()
    return render(request, 'room_types.html', {'room_types': room_types, 'room_type_form': room_type_form})

def book_room(request):
    if not RoomType.objects.exists():
        RoomType.objects.create(name='Single Room')
        RoomType.objects.create(name='Double Room')
        RoomType.objects.create(name='Suite')
        RoomType.objects.create(name='Family Room')

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            new_booking = booking_form.save(commit=False)

            overlapping_bookings = Booking.objects.filter(
                room_type=new_booking.room_type,
                check_out__gt=new_booking.check_in,
                check_in__lt=new_booking.check_out,
                is_booked=True
            )

            if overlapping_bookings.exists():
                taken_dates = ', '.join([f"{booking.check_in} to {booking.check_out}" for booking in overlapping_bookings])
                error_message = f"The selected dates ({new_booking.check_in} to {new_booking.check_out}) for this room are already taken. Please choose different dates. Taken dates: {taken_dates}"
                room_types = RoomType.objects.all()
                return render(request, 'booking_form.html', {'booking_form': booking_form, 'error_message': error_message, 'room_types': room_types})

            new_booking.is_booked = True
            new_booking.save()
            return redirect('rooms:success_page')
    else:
        booking_form = BookingForm()

    room_types = RoomType.objects.all()
    return render(request, 'booking_form.html', {'booking_form': booking_form, 'room_types': room_types})

def success_page(request):
    return render(request, 'success_page.html')

@login_required
def user_bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_bookings.html', {'user_bookings': user_bookings})

@login_required
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('rooms:user_bookings')  
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('rooms:user_bookings') 
    
    if booking.user != request.user:
        messages.error(request, "You don't have permission to delete this booking.")
        return redirect('rooms:user_bookings')  
    booking.delete()

    messages.success(request, "Booking deleted successfully.")
    return redirect('rooms:user_bookings')  


