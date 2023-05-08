from django.urls import path

from user_profile.views import ProfileView, RegisterView

app_name = 'api'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
]
