from django.urls import path


from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('top-artists', views.top_artists, name='top-artists'),
    path('top-tracks', views.top_tracks, name='top-tracks'),
]