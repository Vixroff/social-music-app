import os
import requests


from django.shortcuts import render
from django.views import View


from .models import Authors


URL = 'https://api.musixmatch.com/ws/1.1/'
APIKEY = os.getenv('MUSIXMATCH_API')


def index(request):
    intro = """
    Welcome to the social-music-app!
    """
    return render(request, 'content/index.html', {
        'content': intro
    })


class TopArtistsView(View):
    model = Authors
    template_name = 'content/artists.html'
    top_artists_query = 'chart.artists.get'
    params = f'?&page=1&page_size=7&format=json&apikey={APIKEY}'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.artists = None
    
    def get(self, request):
        artists_response = requests.get(URL+self.top_artists_query+self.params).json()
        status = artists_response['message']['header'].get('status_code')
        if status is 200:
            self.artists = artists_response['message']['body']['artist_list']
            self.fill_db(self.artists)
        return render(request, self.template_name, {'artists': self.artists})

    def fill_db(self, artists: list):
        artists_to_db = []
        for artist in artists:
            if not self.model.objects.filter(
                id_musixmatch=artist['artist']['artist_id']
            ).first():
                artist = self.model(
                    id_musixmatch=artist['artist']['artist_id'],
                    name=artist['artist']['artist_name']
                )
                artists_to_db.append(artist)
        self.model.objects.bulk_create(artists_to_db)


def top_tracks(request):
    tracks = None
    top_tracks_query = 'chart.tracks.get'
    params = f'?chart_name=mxmweekly&page=1&page_size=7&country=XW&f_has_lyrics=1&apikey={APIKEY}'
    tracks_response = requests.get(URL+top_tracks_query+params).json()
    if tracks_response['message']['header']['status_code'] == 200:
        tracks = tracks_response['message']['body']['track_list']
    return render(request, 'content/tracks.html', {
        'tracks': tracks
    })
