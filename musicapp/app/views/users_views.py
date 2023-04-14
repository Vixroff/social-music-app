from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from app.forms import RegistrationForm
from app.models import CustomUser


class RegistrationView(View):
    """
    View handles GET/POST requests.
    Purpose is to create a new user
    """

    template = 'registration/register.html'

    def get(self, request):
        """GET request handler returns registration form."""

        form = RegistrationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        """
        POST request handler method creates new user if data is valid and redirects to 'profile' view.
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
    """
    View handles GET request.
    Purpose is to provide profile page with content.
    """

    template = 'content/profile.html'

    def get(self, request):
        """GET request handler method."""

        user_content = CustomUser.objects.prefetch_related(
        'following',
        'added_tracks',
        'added_playlists',
        'playlists'
    ).get(id=request.user.id)
        profile = {
            'username': user_content.username,
            'email': user_content.email,
            'following': user_content.following,
            'playlists': user_content.playlists,
            'added_tracks': user_content.added_tracks,
            'added_playlists': user_content.added_playlists
        }
        return render(request, self.template, profile)
