from .models import Albums, Artists, Genres, Tracks 


class APIDataMixins:

    def __init__(self, api_response):
        if type(api_response) is not dict or not api_response.get('message'):
            raise ValueError
        self.header = dict(api_response['message']['header'])
        self.body = dict(api_response['message']['body'])
    
    def _check_status(self):
        if self.header.get('status_code') == 200:
            return True
        else:
            return False
    
    def get_data(self):
        if not self._check_status():
            return None
        data = []
        key = list(self.body.keys())[0]
        value = self.body.get(key)
        if len(value) == 0:
            return None
        if key == 'track_list':
            data += self._get_tracks_data(value)
        elif key == 'artist_list':
            data += self._get_artists_data(value)
        return data
        
    def _get_artists_data(self, data):
        result = []
        for row in data:
            artist = {
                'artist': {
                'id_musixmatch': row['artist']['artist_id'],
                'name': row['artist']['artist_name']
                }
            }
            result.append(artist)
        return result

    def _get_tracks_data(self, data):
        result = []
        for row in data:
            track = {
                    'track': {
                    'id_musixmatch': row['track']['track_id'],
                    'name': row['track']['track_name'],
                    }
                }
            album = {
                'id_musixmatch': row['track']['album_id'],
                'name': row['track']['album_name']
            }
            author = {
                'id_musixmatch': row['track']['artist_id'],
                'name': row['track']['artist_name']
            }
            genres = []
            for genre in row['track']['primary_genres']['music_genre_list']:
                genre = {
                    'id_musixmatch': genre['music_genre']['music_genre_id'],
                    'name': genre['music_genre']['music_genre_name']
                }
                genres.append(genre)
            track['track']['album'] = album
            track['track']['artist'] = author
            track['track']['genres'] = genres
            result.append(track)
        return result
    
    def insert_to_db(self):
        data = self.get_data()
        if data:
            for obj in data:
                obj_name = list(obj.keys())[0]
                obj_data = obj[obj_name]
                if obj_name == 'track':
                    if Tracks.objects.filter(id_musixmatch=obj_data['id_musixmatch']).exists():
                        continue
                    obj_to_save = Tracks.objects.create(
                        id_musixmatch=obj_data['id_musixmatch'],
                        name=obj_data['name'], 
                    )
                    album = Albums.objects.get_or_create(
                        id_musixmatch=obj_data['album']['id_musixmatch'],
                        name=obj_data['album']['name']
                    )[0]
                    obj_to_save.album = album
                    artist = Artists.objects.get_or_create(
                        id_musixmatch=obj_data['artist']['id_musixmatch'],
                        name=obj_data['artist']['name']
                    )[0]
                    obj_to_save.author = artist
                    for _genre in obj_data['genres']:
                        genre = Genres.objects.get_or_create(
                            id_musixmatch=_genre['id_musixmatch'],
                            name=_genre['name']
                        )[0]
                        obj_to_save.genres.add(genre)
                    obj_to_save.save()
                elif obj_name == 'artist':
                    if Artists.objects.filter(id_musixmatch=obj_data['id_musixmatch']).exists():
                        continue
                    obj_to_save = Artists.objects.create(
                        id_musixmatch=obj_data['id_musixmatch'],
                        name=obj_data['name']
                    )
