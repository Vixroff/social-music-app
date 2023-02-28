from django.urls import path, include


from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('add_track', views.add_track, name='add_track'),
    path('create-playlist/', views.CreatePlaylistView.as_view(), name='create_playlist'), 
    path('playlist/<int:pk>', views.playlist, name='playlist'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('search', views.SearchView.as_view(), name='search'),
    path('top-artists', views.TopArtistsView.as_view(), name='top_artists'),
    path('top-tracks', views.TopTracksView.as_view(), name='top_tracks'),    
]