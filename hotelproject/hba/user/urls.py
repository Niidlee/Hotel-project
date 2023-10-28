from django.urls import path
from .views import login_user, register_user, GuestUpdateView, success_update_view

app_name = 'user'

urlpatterns = [
    path('login_user', login_user, name="login"),
    path('register_user', register_user, name="register"),
    path('profile', GuestUpdateView.as_view(), name="profile"),
    path('success_update', success_update_view, name='success_update'),

]
