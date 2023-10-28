from django import forms
from .models import BookingSettings, Booking, RoomType


from .models import RoomType

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name']  

class ChangeInputsStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            input_type = self.fields[field].widget.input_type
            classes = self.fields[field].widget.attrs.get("class", "")
            classes += " form-check-input" if input_type == "checkbox" else " form-control flatpickr-input"
            self.fields[field].widget.attrs.update({'class': classes.strip()})

class BookingForm(ChangeInputsStyleMixin, forms.ModelForm):
    room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.all(),
        label='Room Type',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),  # Add a class to the widget for styling
    )

    class Meta:
        model = Booking
        fields = ['user_name', 'check_in', 'check_out', 'num_rooms', 'num_adults', 'num_children', 'email', 'phone', 'room_type']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check_in'].widget.attrs.update({'type': 'date'})
        self.fields['check_out'].widget.attrs.update({'type': 'date'})

class BookingSettingsForm(forms.ModelForm):
    start_time = forms.TimeField(label='Start Time', widget=forms.TimeInput(format='%H:%M'), required=False)
    end_time = forms.TimeField(label='End Time', widget=forms.TimeInput(format='%H:%M'), required=False)

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError("The end time must be later than the start time.")

        return cleaned_data

    class Meta:
        model = BookingSettings
        fields = "__all__"
        exclude = ["max_booking_per_time", "max_booking_per_day"]

class BookingCustomerForm(ChangeInputsStyleMixin, forms.Form):
    user_name = forms.CharField(max_length=250, label='Username')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=10, required=False, label='Phone')
