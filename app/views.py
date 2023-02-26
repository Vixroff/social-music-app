import os
import requests
import pprint


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View


from .models import Artists, Tracks, Genres, Albums
from .mixins import APIDataMixins


URL = 'https://api.musixmatch.com/ws/1.1/'
APIKEY = f"&apikey={os.getenv('MUSIXMATCH_API')}"


def index(request):
    intro = """
    Welcome to the social-music-app!
    """
    return render(request, 'content/index.html', {
        'content': intro
    })


class TopArtistsView(View):
    model = Artists
    template_name = 'content/artists.html'
    top_artists_query = 'chart.artists.get'
    params = f'?&page=1&page_size=7&format=json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.artists = None
    
    def get(self, request):
        response = requests.get(URL+self.top_artists_query+self.params+APIKEY).json()
        api_handler = APIDataMixins(response)
        api_handler.insert_to_db()
        self.artists = api_handler.get_data()
        return render(request, self.template_name, {'artists': self.artists})


class TopTracksView(View):
    model = Tracks
    template_name = 'content/tracks.html'
    top_tracks_query = 'chart.tracks.get'
    params = f'?chart_name=mxmweekly&page=1&page_size=7&country=XW&f_has_lyrics=1'
    
    def get(self, request):
        track_response = requests.get(URL+self.top_tracks_query+self.params+APIKEY).json()
        api_handler = APIDataMixins(track_response)
        api_handler.insert_to_db()
        self.tracks = api_handler.get_data()
        return render(request, self.template_name, {
        'tracks': self.tracks
    })

    @method_decorator(login_required)
    def post(self, request):
        next_url = request.GET.get('next')
        track = self.model.objects.get(
            id_musixmatch=request.POST.get('pk')
        )
        user = request.user
        if not user.added_tracks.filter(id=track.id).exists():
            user.added_tracks.add(track)
        if next_url:
            return redirect('next_url')
        else:
            return redirect('top-tracks')


class SearchView(View):
    template_name = 'content/search.html'
    api_tracks_query = 'track.search&page=1&page_size=5&s_track_rating=desc&q_track='
    api_artists_query = 'artist.search&page=1&page_size=5&q_artist='

    def get(self, request):
        self.user_query = request.GET.get('query')
        if self.user_query == None or self.user_query == '':
            return render(
                request,
                self.template_name,
                {
                'tracks': self.tracks,
                'artists': self.artists,
                'query': self.user_query
                }
            )
        tracks_response = requests.get(
            URL + self.api_tracks_query + self.user_query + APIKEY
        ).json()
        artists_response = requests.get(
            URL + self.api_artists_query + self.user_query + APIKEY
        ).json()
        api_handler1 = APIDataMixins(tracks_response)
        api_handler2 = APIDataMixins(artists_response)
        api_handler1.insert_to_db()
        api_handler2.insert_to_db()
        self.tracks = api_handler1.get_data()
        self.artists = api_handler2.get_data()
        return render(
            request,
            self.template_name,
            {
            'tracks': self.tracks,
            'artists': self.artists,
            'query': self.user_query
            }
        )
        