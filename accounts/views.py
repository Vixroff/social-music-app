from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


from .forms import RegistrationForm


@login_required
def profile(request):
    return render(request, 'profile.html')


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
        return render(request, self.template, {'form': form})