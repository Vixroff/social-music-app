from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True
        )
    added_tracks = models.ManyToManyField('app.Tracks', through='app.UserHasTracks')
    added_playlists = models.ManyToManyField('app.Playlists', through='app.UserHasPlaylists')
