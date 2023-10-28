from django.urls import path
from . import views
from .views import user_bookings, delete_booking

app_name = 'rooms'

urlpatterns = [
    path('book-room/', views.book_room, name='book_room'),
    path('room-types/', views.room_types, name='room_types'),
    path('success-page/', views.success_page, name='success_page'),
    path('user_bookings/', user_bookings, name='user_bookings'),
    path('delete_booking/<int:booking_id>/', delete_booking, name='delete_booking'),

]
