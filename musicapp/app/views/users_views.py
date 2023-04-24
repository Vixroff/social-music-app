import requests

from django.contrib import messages
from django.contrib.auth import login
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views import View

from app.forms import RegistrationForm, CreatePlaylistForm, CommentsForm
from app.models import CustomUser, Tracks, Playlists, Comments


class RegistrationView(View):
    """View is responsible to registration process."""

    template = 'registration/register.html'

    def get(self, request):
        """GET request handler method returns registration form."""

        form = RegistrationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        """
        POST request handler method.

        It creates new user if data is valid and redirects to 'profile' view.
        If data is not valid return GET request handler.
        """

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


class UserProfilesView(View):
    """View provides profile page."""

    template = 'content/profile.html'

    def get(self, request, user_pk):
        """GET request handler method."""
        try:
            user_content = CustomUser.objects.\
                select_related('playlists').\
                prefetch_related('following', 'followers', 'added_tracks', 'added_playlists').\
                get(id=user_pk)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Профиль не найден!')
            return redirect('welcome')
        else:
            context = {
                'username': user_content.username,
                'email': user_content.email,
                'following': user_content.following.all(),
                'followers': user_content.followers.all(),
                'playlists': user_content.playlists.all(),
                'added_tracks': user_content.added_tracks.all(),
                'added_playlists': user_content.added_playlists.all()
            }
            return render(request, self.template, context)


class DeleteUserProfileView(View):
    """View is responsible for a user profile deleting."""

    def delete(self, request, user_pk):
        """POST request method handler."""

        try:
            user = CustomUser.objects.get(pk=user_pk)
        except CustomUser.DoesNotExist:
            messages.error(request, f'Пользователь id:{user_pk} не найден!')
        else:
            user.delete()
            messages.success(request, f'Пользователь id:{user_pk} успешно удален!')
        finally:
            return redirect('welcome')


class UserAddTrackView(View):
    """View is responsible for adding track in user profile."""

    def post(self, request, user_pk):
        """POST request handler method."""

        try:
            user = CustomUser.objects.get(pk=user_pk)
            track = Tracks.objects.get(pk=request.POST.get('pk'))
            user.added_tracks.add(track)
        except (CustomUser.DoesNotExist, Tracks.DoesNotExist):
            messages.error(request, 'Объект пользователя/произведения не найден!')
        except ValidationError:
            messages.error(request, f'Трек {track.name} уже был добавлен ранее!')
        else:
            user.save()
            messages.success(request, f'Трек {track.name} успешно добавлен!')
        finally:
            return redirect('profile-view')


class UserDeleteTrackView(View):
    """View is responsible for deleting track from user profile."""

    def delete(self, request, user_pk, track_pk):
        """DELETE request handler method."""

        try:
            user = CustomUser.objects.get(pk=user_pk)
            track = Tracks.objects.get(pk=request.POST.get('pk'))
            user.added_tracks.remove(track)
        except (CustomUser.DoesNotExist, Tracks.DoesNotExist):
            messages.error(request, 'Объект пользователя/произведения не найден!')
        except ValueError:
            messages.error(request, f'Трек {track.name} не был ранее добавлен к пользователю!')
        else:
            user.save()
            messages.success(request, f'Трек {track.name} успешно удален!')
        finally:
            return redirect('profile-view')


class UserLikePlaylistView(View):
    """View provides a user feature to like playlist."""

    def post(self, request, user_pk):
        """POST request handler method."""

        try:
            user = CustomUser.objects.get(pk=user_pk)
            playlist = Playlists.objects.get(pk=request.POST.get('pk'))
            user.liked_playlists.add(playlist)
        except (CustomUser.DoesNotExist, Tracks.DoesNotExist):
            messages.error(request, 'Объект пользователя/плейлиста не найден!')
        except ValidationError:
            messages.error(request, 'Плейлист уже был лайкнут ранее!')
        else:
            user.save()
            messages.success(request, f'Вам понравился плейлист {playlist.name}')
        finally:
            return redirect('profile-view')


class UserUnlikePlaylistView(View):
    """View provides a user feature to unlike playlist."""

    def delete(self, request, user_pk, playlist_pk):
        """DELETE request handler method."""

        try:
            user = CustomUser.objects.get(pk=user_pk)
            playlist = Playlists.objects.get(pk=playlist_pk)
            user.liked_playlists.remove(playlist)
        except (CustomUser.DoesNotExist, Tracks.DoesNotExist):
            messages.error(request, 'Объект пользователя/плейлиста не найден!')
        except ValueError:
            messages.error(request, f'Плейлист {playlist.name} не был ранее добавлен к пользователю!')
        else:
            user.save()
            messages.success(request, f'Плейлист {playlist.name} успешно удален из понравившихся!')
        finally:
            return redirect('profile-view')


class UserFollowView(View):
    """View provides a user feature to follow other users."""

    def post(self, request, user_pk):
        """POST request handler method."""

        try:
            user = CustomUser.objects.get(pk=user_pk)
            user_to_follow = CustomUser.objects.get(pk=request.POST.get('pk'))
        except CustomUser.DoesNotExist:
            messages.error(request, 'Объект пользователя не найден')
        else:
            if user.following.filter(pk=user_to_follow.pk).exists():
                messages.warning(request, f'Вы уже подписаны на пользователя {user_to_follow.username}')
            else:
                user.following.add(user_to_follow)
                user.save()
                messages.success(request, f'Вы успешно подписались на пользователя {user_to_follow.username}')
        finally:
            return redirect('profile-view')


class UserUnfollowView(View):
    """View provides a user feature to unfollow other users."""

    def delete(self, request, user_pk, following_pk):
        """DELETE request handle method."""

        try:
            user = CustomUser.objects.get(pk=user_pk)
            user_to_follow = CustomUser.objects.get(pk=following_pk)
            user.following.remove(user_to_follow)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Объект пользователя не найден!')
        except ValidationError:
            user.save()
            messages.error(request, 'Вы не были подписаны на пользователя ранее!')
        finally:
            return redirect('profile-view')


class CreatePlaylistView(View):
    """View provides capability to create playlist."""

    template = 'content/create_playlist.html'

    def get(self, request):
        """
        Method handles GET request. 
        Provide playlist creation form.
        """

        form = CreatePlaylistForm(user=request.user)
        return render(request, self.template, {'form': form})  

    def post(self, request):
        """
        Method handles POST request.
        It validates form data and creates a new playlist in database.
        """

        form = CreatePlaylistForm(request.POST, user=request.user)
        if form.is_valid():
            playlist = form.save()
            messages.success(request, f'Плейлист {playlist.name} успешно создан!')
            return redirect('profile-view')
        else:
            messages.error(request, 'Что-то пошло не так!')
            return render(request, self.template, {'form': form})


class PlaylistView(View):
    """View provides a playlist page."""

    template = 'content/playlist.html'

    def get(self, request, playlist_pk):
        """Method handles GET request and return template with playlist context."""

        try:
            playlist = Playlists.objects. \
                select_related('creator'). \
                prefetch_related(
                    'tracks',
                    Prefetch('comments', queryset=Comments.objects.select_related('author')),
                    Prefetch('customuser_set', to_attr='liked')
                ). \
                get(pk=playlist_pk)
        except Playlists.DoesNotExist:
            messages.error(request, f'Плейлист с заданным id:{playlist_pk} не существует!')
            return redirect('profile-view')
        else:
            form = CommentsForm()
            context = {
                'name': playlist.name,
                'creator': playlist.creator,
                'created_at': playlist.created_at,
                'likes': playlist.liked.count(),
                'tracks': playlist.tracks.all(),
                'comments': playlist.comments.all(),
                'form': form
            }
            return render(request, self.template, context)


class DeletePlaylistView(View):
    """View provides a feature to delete playlist."""

    def delete(self, request, playlist_pk):
        """Method handles DELETE request to delete playlist."""

        try:
            playlist = Playlists.objects.get(pk=playlist_pk)
        except Playlists.DoesNotExist:
            messages.error(request, 'Плейлист не найден!')
        else:
            playlist.delete()
            messages.success(request, f'Плейлист {playlist.name} успешно удален!')
        finally:
            return redirect('profile-view')
        

class AddCommentView(View):
    """View provides a feature to leave a comment to playlist."""

    def post(self, request, playlist_pk):
        """
        Method handles POST request.
        It validates data and save comment.
        """

        form = CommentsForm(request.POST)
        try:
            playlist = Playlists.objects.get(pk=playlist_pk)
            if not form.is_valid():
                raise ValidationError
        except Playlists.DoesNotExist:
            messages.error(request, 'Плейлист не найден!')
        except ValidationError:
            errors = form.errors.as_data()
            for field, error in errors.items():
                messages.error(request, 'Ошибка в поле {}: {}'.format(field, error[0]))
        else:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.playlist = playlist
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен!')
        finally:
            return redirect('playlist-view', playlist_pk=playlist_pk)


class DeleteCommentView(View):
    """View provides a feature to delete playlist's comment."""

    def delete(self, request, playlist_pk, comment_pk):
        """Method handles DELETE request and provides deleting comment."""

        try:
            comment = Comments.objects.get(pk=comment_pk)
        except Comments.DoesNotExist:
            messages.error(request, 'Комментарий не найден!')
        else:
            comment.delete()
            messages.success(request, 'Комментарий успешно удален!')
        finally:
            return redirect('playlist-view', pk=playlist_pk)


class AddTrackToPlaylistView(View):
    """View provides a feature to add track to playlist."""

    def post(self, request, playlist_pk):
        """View handles POST request to provide a view feature."""

        try:
            playlist = Playlists.objects.get(pk=playlist_pk)
            track = Tracks.objects.get(pk=request.POST.get('pk'))
        except (Playlists.DoesNotExist, Tracks.DoesNotExist):
            messages.error(request, 'Объект плейлиста/произведения не найден!')
        else:
            playlist.tracks.add(track)
            playlist.save()
            messages.success(request, f'Трек {track.name} успешно добавлен!')
        finally:
            return redirect('playlist-view', pk=playlist_pk)


class DeleteTrackFromPlaylistView(View):
    """View provides a feature to delete track from playlist."""

    def delete(self, request, playlist_pk, track_pk):
        """View handles DELETE request to provide a view feature."""

        try:
            playlist = Playlists.objects.get(pk=playlist_pk)
            track = Tracks.objects.get(pk=track_pk)
            playlist.tracks.remove(track)
        except (Playlists.DoesNotExist, Tracks.DoesNotExist):
            messages.error(request, 'Объект плейлиста/пользователя не найден!')
        except ValidationError:
            messages.error(request, 'Трек невозможно удалить!')
        else:
            playlist.save()
            messages.success(request, 'Трек успешно удален!')
        finally:
            return redirect('playlist-view', pk=playlist_pk)


class SearchView(View):
    """
    View provides a feature to search musical content from MusixMatch library and profiles.
    """

    template = 'content/searching.html'

    def get(self, request):
        """Method handles GET request."""

        query = request.GET.get('query')
        if query:
            tracks = 

