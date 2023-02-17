import os
import requests
from django.shortcuts import render


URL = 'https://api.musixmatch.com/ws/1.1/'
APIKEY = os.getenv('MUSIXMATCH_API')

# Create your views here.
def index(request):
    intro = """
    Welcome to the social-music-app!
    """
    return render(request, 'index.html', {
        'content': intro
    })


def top_artists(request):
    artists = None
    top_artists_query = 'chart.artists.get'
    params = f'?&page=1&page_size=7&format=json&apikey={APIKEY}'
    artists_response = requests.get(URL+top_artists_query+params).json()
    if artists_response['message']['header']['status_code'] == 200:
        artists = artists_response['message']['body']['artist_list']
    return render(request, 'artists.html', {
        'artists': artists
    })


def top_tracks(request):
    tracks = None
    top_tracks_query = 'chart.tracks.get'
    params = f'?chart_name=mxmweekly&page=1&page_size=7&country=XW&f_has_lyrics=1&apikey={APIKEY}'
    tracks_response = requests.get(URL+top_tracks_query+params).json()
    if tracks_response['message']['header']['status_code'] == 200:
        tracks = tracks_response['message']['body']['track_list']
    return render(request, 'tracks.html', {
        'tracks': tracks
    })
