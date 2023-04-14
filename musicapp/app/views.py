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
from .models import Tracks, Playlists, CustomUser, Comments
from .mixins import APIDataMixins


URL = 'https://api.musixmatch.com/ws/1.1/'
APIKEY = f"&apikey={os.getenv('MUSIXMATCH_API')}"


def welcome(request):
    intro = """
    Welcome to the social-music-app!
    """
    return render(request, 'content/index.html', {
        'content': intro
    })


@login_required
def content_manager(request):
    content = request.POST.get('content')
    user = request.user
    if content == 'playlist':
        playlist = Playlists.objects.get(id=request.POST.get('pk'))
        if 'add' in request.POST:
            if user.added_playlists.filter(id=playlist.id).exists():
                messages.success(request, f'Плейлист "{playlist.name}" был добавлен ранее')
            else:
                user.added_playlists.add(playlist)
                user.save()
                messages.success(request, f'Плейлист "{playlist.name}" уже успешно добавлен!')
        elif 'delete' in request.POST:
            if playlist.creator == user:
                playlist.delete()
                messages.success(request, f'Плейлист "{playlist.name}" успешно удален!')
                return redirect('profile')
            elif not user.added_playlists.filter(id=playlist.id).exists():
                messages.error(request, 'Недоступное действие')
            else:
                user.added_playlists.remove(playlist)
                user.save()
                messages.success(request, f'Плейлист "{playlist.name}" успешно удален!')
    elif content == 'track':
        track = Tracks.objects.get(id_musixmatch=request.POST.get('pk'))
        if 'add' in request.POST:
            if user.added_tracks.filter(id=track.id).exists():
                messages.success(request, f'Трек "{track.name}" уже был добавлен ранее')
            else:
                user.added_tracks.add(track)
                user.save()
                messages.success(request, f'Трек "{track.name}" успешно добавлен!')
        elif 'delete' in request.POST:
            if not user.added_tracks.filter(id=track.id).exists():
                messages.error(request, 'Недоступное действие')
            else:
                user.added_tracks.remove(track)
                user.save()
                messages.success(request, f'Трек "{track.name}" успешно удален!')
    next_url = request.POST.get('next')
    query = request.POST.get('query')
    if next_url and query:
        return redirect(next_url+'?query='+query)
    elif next_url:
        return redirect(next_url)
    else:
        return redirect('profile')


@login_required(redirect_field_name='login')
def profile(request):
    user = request.user
    created_playlists = user.playlists.all()
    liked_playlists = user.added_playlists.all()
    tracks = user.added_tracks.all()
    following = user.following.all()
    followers = user.followers.all()
    return render(
        request,
        'content/profile.html',
        {
            'user': user,
            'following': following,
            'followers': followers,
            'tracks': tracks,
            'liked_playlists': liked_playlists,
            'created_playlists': created_playlists
        }
    )


@method_decorator(login_required, name='dispatch')
class CreatePlaylistView(View):
    template_name = 'content/create_playlist.html'

    def get(self, request):
        form = CreatePlaylistForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreatePlaylistForm(request.POST, user=request.user)
        if form.is_valid():
            playlist = form.save()
            messages.success(request, f'Плейлист "{playlist.name}" создан успешно')
            return redirect('profile')
        else:
            messages.error(
                request,
                'Что-то пошло не так! Скорее всего у вас уже есть плейлист с таким именем! Но это не точно'
            )
            return render(request, self.template_name, {'form': form})


class MyLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, 'Неверные данные')
        return super().form_invalid(form)


class PlaylistView(View):
    template_name = 'content/playlist.html'

    def get(self, request, pk):
        owner = False
        playlist = Playlists.objects.get(pk=pk)
        tracks = playlist.tracks.all()
        comments = Comments.objects.filter(playlist=playlist)
        comment_form = CommentsForm()
        if request.user.is_authenticated and request.user == playlist.creator:
            owner = True
        return render(
            request,
            self.template_name,
            {
                'playlist': playlist,
                'tracks': tracks,
                'comments': comments,
                'form': comment_form,
                'owner': owner
            }
        )

    @method_decorator(login_required)
    def post(self, request, pk):
        user = request.user
        if 'add_comment' in request.POST:
            form = CommentsForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = user
                comment.playlist = Playlists.objects.get(pk=pk)
                comment.save()
                messages.success(request, 'Комментарий успешно добавлен')
                return redirect('playlist', pk=pk)
            else:
                messages.error(request, 'Что-то пошло не так!')
                return redirect('playlist', pk=pk)
        elif 'delete_comment' in request.POST:
            comment = Comments.objects.get(id=request.POST.get('comment_id')).delete()
            messages.success(request, 'Сообщение удалено')
            return redirect('playlist', pk=pk)


class ProfileView(View):
    template_name = "content/user.html"

    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            messages.error("Пользователь с таким id не найден")
            return redirect('index')
        finally:
            if request.user.is_authenticated and user == request.user:
                messages.success(request, 'Это ваш аккаунт')
                return redirect('profile')
            else:
                created_playlists = user.playlists.all()
                liked_playlists = user.added_playlists.all()
                tracks = user.added_tracks.all()
                following = user.following.all()
                followers = user.followers.all()
                return render(
                    request,
                    self.template_name,
                    {
                        'user': user,
                        'following': following,
                        'followers': followers,
                        'tracks': tracks,
                        'liked_playlists': liked_playlists,
                        'created_playlists': created_playlists
                    }
                )

    @method_decorator(login_required)
    def post(self, request, pk):
        user = request.user
        if 'follow' in request.POST:
            user_to_follow = CustomUser.objects.get(id=request.POST.get('user'))
            if user_to_follow == user:
                messages.error(request, 'Невозможная операция!')
            elif user.is_follow(user_to_follow):
                messages.warning(request, f'Вы были подписаны ранее на {user_to_follow}!')
            else:
                user.follow(user_to_follow)
                messages.success(request, f'{user_to_follow} добавлен в друзья')
        elif 'unfollow' in request.POST:
            user_to_unfollow = CustomUser.objects.get(id=request.POST.get('user'))
            if user_to_unfollow == user:
                messages.error(request, 'Невозможная операция!')
            elif user.is_follow(user_to_unfollow) is False:
                messages.error(request, f'Вы не были подписаны на {user_to_unfollow}')
            else:
                user.unfollow(user_to_unfollow)
                messages.success(request, f'Вы успешно отписались от {user_to_unfollow}')
        return redirect('user', pk=pk)


class RecommendationsView(View):
    template_name = 'content/recommendations.html'

    def get(self, request):
        users_to_recommend = []
        if request.user.is_authenticated:
            users_to_recommend = request.user.get_users_recommendations()
        return render(request, self.template_name, {'users': users_to_recommend})


class RegistrationView(View):
    template = 'registration/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
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

    def get(self, request):
        user_query = request.GET.get('query')
        if user_query is None or user_query == '':
            return render(
                request,
                self.template_name,
                {
                    'query': user_query
                }
            )
        tracks_response = requests.get(
            URL + self.api_tracks_query + user_query + APIKEY
        ).json()
        artists_response = requests.get(
            URL + self.api_artists_query + user_query + APIKEY
        ).json()
        api_handler1 = APIDataMixins(tracks_response)
        api_handler2 = APIDataMixins(artists_response)
        api_handler1.insert_to_db()
        api_handler2.insert_to_db()
        tracks = api_handler1.get_data()
        artists = api_handler2.get_data()
        profiles = CustomUser.objects.filter(username=user_query)
        return render(
            request,
            self.template_name,
            {
                'tracks': tracks,
                'artists': artists,
                'query': user_query,
                'profiles': profiles
            }
        )


class TopArtistsView(View):
    template_name = 'content/top_artists.html'
    top_artists_query = 'chart.artists.get'
    params = '?&page=1&page_size=7&format=json'

    def get(self, request):
        response = requests.get(URL+self.top_artists_query+self.params+APIKEY).json()
        api_handler = APIDataMixins(response)
        api_handler.insert_to_db()
        artists = api_handler.get_data()
        return render(request, self.template_name, {'artists': artists})


class TopTracksView(View):
    template_name = 'content/top_tracks.html'
    top_tracks_query = 'chart.tracks.get'
    params = '?chart_name=mxmweekly&page=1&page_size=6'

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
