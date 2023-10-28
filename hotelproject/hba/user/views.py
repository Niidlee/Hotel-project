from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View



from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from user.forms import UserUpdateForm
from user.models import Guest
from user.forms import RegisterUserForm, UserUpdateForm
from user.models import Guest
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')  # Redirect to the homepage or another appropriate page
        else:
            messages.error(request, "There was an error logging in. Please try again.")
    
    return render(request, 'login_register.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out successfully.")
    return redirect('index')  # Redirect to the homepage or another appropriate page

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log the user in
            messages.success(request, "Registration and login successful!")
            return redirect('index')  # Redirect to the homepage or another appropriate page
        else:
            messages.error(request, "Registration failed. Please check your input.")
            # Add debug messages to see form errors
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
    else:
        form = RegisterUserForm()
        
    return render(request, 'login_register.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from user.forms import UserUpdateForm
from user.models import Guest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from user.forms import UserUpdateForm
from user.models import Booking

class GuestUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        user_bookings = Booking.objects.filter(guest__user=request.user)

        context = {
            "user_form": user_form,
            "user_bookings": user_bookings,
        }

        return render(request, "profile.html", context=context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!")

        booking_id_to_delete = request.POST.get("booking_id_to_delete")
        if booking_id_to_delete:
            try:
                booking_to_delete = Booking.objects.get(id=booking_id_to_delete, guest__user=request.user)
                booking_to_delete.delete()
                messages.success(request, "Booking deleted successfully!")
            except Booking.DoesNotExist:
                messages.error(request, "Booking not found or you don't have permission to delete it.")

        return render(request, "success_update.html")


def success_update_view(request):
    return render(request, "success_update.html")
