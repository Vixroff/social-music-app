from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View


from .forms import RegistrationForm, CreatePlaylistForm
from .models import CustomUser
from app.models import Playlists


@login_required(redirect_field_name='login')
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    tracks = user.added_tracks.all()
    liked_playlists = user.added_playlists.all()
    created_playlist = Playlists.objects.filter(creator=user)
    return render(request, 'profile.html', {
        'user': user,
        'tracks': tracks,
        'liked_playlists': liked_playlists,
        'playlists': created_playlist
    }
    )


class MyLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, 'Неверные данные')
        return super().form_invalid(form)


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


@method_decorator(login_required, name='dispatch')
class CreatePlaylistView(View):
    template_name = 'create_playlist.html'

    def get(self, request):
        form = CreatePlaylistForm(user=request.user)
        return render(
            request,
            self.template_name,
            {'form': form}
        )
    
    def post(self, request):
        form = CreatePlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.creator = request.user
            form.save()
            return redirect('profile')
        return render(
            request,
            self.template_name,
            {'form': form(user=request.user)}
        )

