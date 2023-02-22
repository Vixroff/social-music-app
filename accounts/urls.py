from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('register/', views.RegistrationView.as_view(), name='registration')
]
