from django.db import models
from accounts.models import CustomUser


class Albums(models.Model):
    id_musixmatch = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    reliased = models.DateField(blank=True)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Album(id_musixmatch={}, name={})".format(self.id_musixmatch, self.name)


class Authors(models.Model):
    id_musixmatch = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Author(id_musixmatch={}, name={})".format(self.id_musixmatch, self.name)


class Genres(models.Model):
    id_musixmatch = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Genre(id_musixmatch={}, name={})".format(self.id_musixmatch, self.name)


class Tracks(models.Model):
    id_musixmatch = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    album = models.ForeignKey(Albums, on_delete=models.RESTRICT)
    genre = models.ForeignKey(Genres, on_delete=models.RESTRICT)
    authors = models.ManyToManyField(Authors)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Track(id_musixmatch={}, name={})".format(self.id_musixmatch, self.name)


class Playlists(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Tracks)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "Playlist(name={}, creator={})".format(self.name, self.creator)


class Comments(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)

    def __repr__(self):
        return "Comment(author={}, playlist={}, created_at={})".format(
            self.author, 
            self.playlist, 
            self.created_at
        )
    
    def __str__(self):
        return self.message


class UserHasTracks(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class UserHasPlaylists(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlists, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
