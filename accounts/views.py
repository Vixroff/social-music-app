from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


from .forms import RegistrationForm
from .models import CustomUser


@login_required(redirect_field_name='login')
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    tracks = user.added_tracks.all()
    playlists = user.added_playlists.all()
    return render(request, 'profile.html', {
        'user': user,
        'tracks': tracks,
        'playlists': playlists
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