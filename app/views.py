import os
import requests
import pprint


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View


from .models import Authors, Tracks, Genres, Albums


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
    model = Authors
    template_name = 'content/artists.html'
    top_artists_query = 'chart.artists.get'
    params = f'?&page=1&page_size=7&format=json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.artists = None
    
    def get(self, request):
        response = requests.get(URL+self.top_artists_query+self.params+APIKEY).json()
        status = response['message']['header'].get('status_code')
        if status == 200:
            self.artists = response['message']['body']['artist_list']
            self.fill_db(self.artists)
        return render(request, self.template_name, {'artists': self.artists})

    def fill_db(self, artists):
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


class TopTracksView(View):
    model = Tracks
    template_name = 'content/tracks.html'
    top_tracks_query = 'chart.tracks.get'
    params = f'?chart_name=mxmweekly&page=1&page_size=7&country=XW&f_has_lyrics=1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracks = None
    
    def get(self, request):
        response = requests.get(URL+self.top_tracks_query+self.params+APIKEY).json()
        status = response['message']['header'].get('status_code')
        if status == 200:
            self.tracks = response['message']['body']['track_list']
            self.fill_db(self.tracks)
        return render(request, self.template_name, {
        'tracks': self.tracks
    })

    @method_decorator(login_required)
    def post(self, request):
        track = self.model.objects.get(
            id_musixmatch=request.POST.get('pk')
        )
        user = request.user
        if not user.added_tracks.filter(id=track.id).exists():
            user.added_tracks.add(track)
        return redirect('top-tracks')
    
    def fill_db(self, tracks):
        for track in tracks:
            if not self.model.objects.filter(
                id_musixmatch=track['track']['track_id']
            ):
                album, created = Albums.objects.get_or_create(
                    id_musixmatch=track['track']['album_id'],
                    name=track['track']['album_name']
                )
                author, created = Authors.objects.get_or_create(
                    id_musixmatch=track['track']['artist_id'],
                    name=track['track']['artist_name']
                )
                genres = []
                for genre in track['track']['primary_genres']['music_genre_list']:
                    genre, created = Genres.objects.get_or_create(
                        id_musixmatch=genre['music_genre']['music_genre_id'],
                        name=genre['music_genre']['music_genre_name']
                    )
                    genres.append(genre)
                track = self.model.objects.create(
                    id_musixmatch=track['track']['track_id'],
                    name=track['track']['track_name'],
                    album=album,
                    author=author
                )
                track.genres.set(genres)


class SearchView(View):
    template_name = 'content/search.html'
    api_tracks_query = 'track.search&page=1&page_size=5&s_track_rating=desc&q_track='
    api_artists_query = 'artist.search&page=1&page_size=5&q_artist='

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tracks = None
        self.artists = None

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

        tracks_response_status = tracks_response['message']['header'].get('status_code')
        if tracks_response_status == 200:
            self.tracks = tracks_response['message']['body']['track_list']
        
        artists_response_status = artists_response['message']['header'].get('status_code')
        if artists_response_status == 200:
            self.artists = artists_response['message']['body']['artist_list']

        return render(
            request,
            self.template_name,
            {
            'tracks': self.tracks,
            'artists': self.artists,
            'query': self.user_query
            }
        )
        