from django.urls import path, include


from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include([
        path('login/', views.MyLoginView.as_view(), name='login'),
        path('personal/', views.profile, name='profile'),
        path('register/', views.RegistrationView.as_view(), name='registration'), 
        path('', include('django.contrib.auth.urls')),
    ])),
    path('content/', include([
        path('create-playlist/', views.CreatePlaylistView.as_view(), name='create_playlist'), 
        path('playlist/<int:pk>/', views.PlaylistView.as_view(), name='playlist'),
        path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile_view')
    ])),
    path('search/', include([
        path('search', views.SearchView.as_view(), name='search'),
        path('top-artists', views.TopArtistsView.as_view(), name='top_artists'),
        path('top-tracks', views.TopTracksView.as_view(), name='top_tracks'), 
    ])),
    path('add_track', views.add_track, name='add_track'),        
]