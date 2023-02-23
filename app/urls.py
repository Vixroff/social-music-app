from django.urls import path


from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('top-artists', views.TopArtistsView.as_view(), name='top-artists'),
    path('top-tracks', views.top_tracks, name='top-tracks'),
]