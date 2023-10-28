from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user.models import Guest

from django import forms
class RegisterUserForm(UserCreationForm):
    email= forms.EmailField()
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    
    class Meta:
        model=User
        fields=('username', 'first_name', 'last_name', 'email','password1', 'password2')

"""


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['roomNumber', 'startDate', 'endDate']


"""

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name","email")
