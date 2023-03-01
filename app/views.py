import os
import requests


from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View


from .forms import CreatePlaylistForm, RegistrationForm, CommentsForm
from .models import Artists, Tracks, Playlists, CustomUser, Comments
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


@login_required(redirect_field_name='login')
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    tracks = user.added_tracks.all()
    liked_playlists = user.added_playlists.all()
    created_playlist = Playlists.objects.filter(creator=user)
    return render(
        request, 
        'content/profile.html', 
        {
        'user': user,
        'tracks': tracks,
        'liked_playlists': liked_playlists,
        'playlists': created_playlist
        }
    )

@login_required
def add_track(request):
    if request.method == "POST":
        track = Tracks.objects.get(id_musixmatch=request.POST.get('pk'))
        user = request.user
        if not user.added_tracks.filter(id=track.id).exists():
            user.added_tracks.add(track)
            messages.success(request, f'Трек "{track.name}" успешно добавлен!')
        else:
            messages.success(request, f'Трек "{track.name}" был добавлен ранее')
    next_url = request.POST.get('next')
    query = request.POST.get('query')
    if next_url and query:
        return redirect(next_url+'?query='+query)
    elif next_url:
        return redirect(next_url)
    else:
        return redirect('profile')


@method_decorator(
    login_required(redirect_field_name='login'), name='dispatch'
)
class CreatePlaylistView(View):
    template_name = 'content/create_playlist.html'

    def get(self, request):
        form = CreatePlaylistForm(user=request.user)
        return render(
            request,
            self.template_name,
            {'form': form}
        )
    
    def post(self, request):
        form = CreatePlaylistForm(request.POST, user=request.user)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.creator = request.user
            playlist.save()
            messages.success(request, f'Плейлист "{playlist.name}" создан успешно')
            return redirect('profile')
        return render(
            request,
            self.template_name,
            {'form': form}
        )


class MyLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, 'Неверные данные')
        return super().form_invalid(form)


class PlaylistView(View):
    template_name = 'content/playlist.html'

    def get(self, request, pk):
        playlist = Playlists.objects.get(pk=pk)
        tracks = playlist.tracks.all()
        comments = Comments.objects.filter(playlist=playlist)
        comment_form = CommentsForm()
        return render(
            request, 
            self.template_name, 
            {
            'playlist': playlist,
            'tracks': tracks,
            'comments': comments,
            'form': comment_form,
            }
        )
    
    @method_decorator(login_required)
    def post(self, request, pk):
        user = request.user
        if 'add' in request.POST:
            form = CommentsForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = user
                comment.playlist = Playlists.objects.get(pk=pk)
                comment.save()
                messages.success(request, 'Комментарий успешно добавлен')
                return redirect('playlist', pk=pk)
            messages.error(request, 'Что-то пошло не так!')
            return redirect('playlist', pk=pk)
        elif 'delete' in request.POST:
            comment = Comments.objects.get(id=request.POST.get('comment_id')).delete()
            messages.success(request, 'Сообщение удалено')
            return redirect('playlist', pk=pk)
        

            
class RegistrationView(View):
    registration_form = RegistrationForm
    template = 'registration/register.html'

    def get(self, request):
        form = self.registration_form()
        return render(request, self.template, {'form': form})
    
    def post(self, request):
        form = self.registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            errors = form.errors.as_data()
            for field, error in errors.items():
                messages.error(
                    request, 
                    'Ошибка в поле {}: {}'.format(
                    field, error[0]
                    )
                )
        return render(request, self.template, {'form': form})


class SearchView(View):
    template_name = 'content/searching.html'
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


class TopArtistsView(View):
    model = Artists
    template_name = 'content/top_artists.html'
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
    template_name = 'content/top_tracks.html'
    top_tracks_query = 'chart.tracks.get'
    params = f'?chart_name=mxmweekly&page=1&page_size=7&country=XW&f_has_lyrics=1'
    
    def get(self, request):
        track_response = requests.get(
            URL + self.top_tracks_query + self.params + APIKEY
        ).json()
        api_handler = APIDataMixins(track_response)
        api_handler.insert_to_db()
        self.tracks = api_handler.get_data()
        return render(
            request,
            self.template_name, 
            {'tracks': self.tracks}
        )
