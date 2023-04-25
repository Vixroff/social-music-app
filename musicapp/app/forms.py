from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CheckboxSelectMultiple, HiddenInput

from .models import CustomUser, Playlists, Comments


class RegistrationForm(UserCreationForm):
    class Meta:
        heyel = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class CreatePlaylistForm(ModelForm):
    """Playlist creation form."""
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['tracks'].queryset = user.added_tracks.all()
        self.fields['creator'].initial = user.id

    class Meta:
        model = Playlists
        fields = ['name', 'description', 'tracks', 'creator']
        widgets = {
            'creator': HiddenInput(),
            'tracks': CheckboxSelectMultiple()
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'tracks': 'Треки'
        }


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['message']
        labels = {
            'message': 'Комментарий'
        }
        help_text = {
            'message': 'Ваш комментарий'
        }
