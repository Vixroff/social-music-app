from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('profile/', views.profile, name='profile'),
    path('create-playlist/', views.CreatePlaylistView.as_view(), name='create_playlist'),
    path('', include('django.contrib.auth.urls')),
]
