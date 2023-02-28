from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CheckboxSelectMultiple


from .models import CustomUser, Playlists


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class CreatePlaylistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tracks'].queryset = user.added_tracks.all()
    
    class Meta:
        model = Playlists
        fields = ['name','description', 'tracks']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'tracks': 'Треки'
        }
        widgets = {
            'tracks': CheckboxSelectMultiple()
        }
