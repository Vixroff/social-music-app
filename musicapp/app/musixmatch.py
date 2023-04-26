import os
from abc import abstractmethod

import requests

from app.models import Albums, Artists, Genres, Tracks


class AbstractMusixmatchAPIManager:
    """Abstract class that manages MusixMatch API requests."""

    @abstractmethod
    def __init__(self, request_type):
        """Initializes instance with given API request type."""
        pass

    @abstractmethod
    def make_request(self, **params):
        """Makes API request with the given parameters."""
        pass

    @abstractmethod
    def extract_json_response(self):
        """Returns response as dict."""
        pass


class AbstractTracksResponseHandler:
    """Abstract class that extracts, uploads and returns `Tracks` objects."""

    @abstractmethod
    def search_tracks_data(self):
        """Extracts `track` datasets from the MusixMatch API response."""
        pass

    @abstractmethod
    def upload_tracks_to_db(self):
        """Uploads tracks in a database."""
        pass

    @abstractmethod
    def retrieve_handled_track_objects(self):
        """Returns all handled `Tracks` objects."""
        pass


class MusixMatchAPIManager(AbstractMusixmatchAPIManager):
    """
    A class that manages MusixMatch API requests.

    Attributes:
        1). `api (dict)`:
            A dictionary that maps allowed API request types to their corresponding parameters and URLs.
            Go to https://developer.musixmatch.com/documentation to see detailed documentation.

        2). `url (str)`:
            A base MusixMatch API URL.

        3). `apikey (str)`:
            A MusixMatch API apikey.

    Methods:
        1). `__init__(self, api_request: str)` -> None:
            Initializes MusixMatchAPIManager instance and 
            defines `self.api_request` of it as MusixMatch API request type.

        2). `make_request(self, **params: Any)` -> None:
            Sends a request to the MusixMatch API URL with the specified api_request and given parameters.

        3). `extract_json_response(self)` -> dict:
            Returns the response data as dict.
    """

    api = {
        'top-tracks': {
            'allowed_params': [
                'country',
                'page',
                'page_size',
                'format',
                'f_has_lyrics',
            ],
            'path': 'chart.tracks.get'
        },
        'top-artists': {
            'allowed_params': [
                'country',
                'page',
                'page_size',
                'format',
            ],
            'path': 'chart.artists.get'
        },
        'track-search': {
            'allowed_params': [
                'q_track',
                'q_artist',
                'q_lyrics',
                'q_track_artist',
                'q_writer',
                'q',
                'f_artist_id',
                'f_music_genre_id',
                'f_lyrics_language',
                'f_has_lyrics',
                'f_track_release_group_first_release_date_min',
                'f_track_release_group_first_release_date_max',
                's_artist_rating',
                's_track_rating',
                'quorum_factor',
                'page',
                'page_size',
            ],
            'path': 'track.search'
        }
    }
    url = 'https://api.musixmatch.com/ws/1.1/'
    apikey = os.getenv('MUSIXMATCH_API')

    def __init__(self, api_request):
        """
        Initializes MusixMatchAPIManager instance.

        Method constructs an instance and defines attribute of it:
            1). `self.api_request`
                Type of MusixMatch API request.

        Args:
            1). `api_request (str)`:
                Type of MusixMatch API request.

        Raises:
            1). `ValueError`:
                If api_request is not string or valid.
        """

        self._check_api_request(api_request)
        self.api_request = api_request

    def make_request(self, **params):
        """
        Makes request.

        Method validates the given parameters, constructs Musixmatch API URL to be requested according to the
        specified `self.api_request` of instance and given parameters. Then makes request, and saves the response as
        `self.response` if response`s status is in 200 range.

        Args:
            1). `**params (Any)`:
                Parameters to pass in the request.

        Raises:
            1). `ValueError`:
                If the given parameters are not valid with specified `self.api_request` type.

            2). `requests.HTTPError`:
                If the response status code is not in the 200 range.
        """

        self._check_params(params)
        params.update({'apikey': self.apikey})
        response = requests.get(
            self.url + self.api.get(self.api_request).get('path'),
            params=params
        )
        response.raise_for_status()
        self.response = response

    def extract_json_response(self):
        """Returns response as dict."""

        return self.response.json()

    def _check_api_request(self, api_request):
        """
        Method checks `api_request` to proper value.

        Args:
            1). `api_request (str)`:
                Type of Musixmatch API request.

        Raises:
            1). `ValueError`:
                If `api_request` is not a string or is not valid.
        """

        if not isinstance(api_request, str):
            raise ValueError('`api_request` should be string!')
        elif api_request not in self.api:
            raise ValueError(f'Entered api_request: {api_request} is not valid!')

    def _check_params(self, params: dict):
        """
        Checks parameters according to `self.api_request` allowed parameters.

        Args:
            1). `params (dict)`:
                Dict of parameters.

        Raises:
            1). `ValueError`:
                If parameter is not valid.
        """

        allowed_params = self.api.get(self.api_request).get("allowed_params")
        for param in params:
            if param not in allowed_params:
                raise ValueError('`{}` parameter is not valid to make {} request!'.format(param, self.api_request))


class MusixmatchAPIResponseHandler(
    AbstractTracksResponseHandler,
):
    """
    A class that handles the response of the Musixmatch API, extracts the relevant data, and stores it in a database.

    Methods:
        1). `__init__(self, response: dict)` -> None:
            Initializes MusixmatchAPIResponseHandler class instance.

        2). `search_tracks_data(self)` -> None:
            Searches for `track` key in the `self.response` and extracts founded datasets to `self.content_to_insert`

        3). `upload_tracks_to_db(self)` -> None:
            Uploads tracks with all depended entities taken from `self.content_to_upload` in a database.

        4). `retrieve_handled_track_objects(self)` -> list:
            Returns list of `Tracks` handled objects taken from `self.content_handled`.

        5). `_get_or_create_track_object(self, track_data: dict)` -> tuple(album: `Tracks`, upload_status: bool):
            Creates `Tracks` object if it doesn`t exist else retrieves.
            Makes relevant records in `self.content_uploaded` and `self.content_handled`

        6). `_get_or_create_album_object(self, album_data: dict)` -> tuple(album: `Albums`, upload_status: bool):
            Creates `Albums` object if it doesn`t exist else retrieves.
            Makes relevant records in `self.content_uploaded` and `self.content_handled`

        7). `_get_or_create_artist_object(self, artist_data: dict)` -> tuple(album: `Artists`, upload_status: bool):
            Creates `Artists` object if it doesn`t exist else retrieves.
            Makes relevant records in `self.content_uploaded` and `self.content_handled`

        8). `_get_or_create_genre_object(self, genre_data: dict)` -> tuple(album: `Genres`, upload_status: bool)::
            Creates `Genres` object if it doesn`t exist else retrieves.
            Makes relevant records in `self.content_uploaded` and `self.content_handled`
    """

    def __init__(self, response: dict):
        """
        Initializes MusixmatchAPIResponseHandler class instance.

        Method constructs an instance and defines 4 attributes of it:
            1). `self.response (dict)`:
                The response from Musixmatch API request.

            2). `self.content_to_insert (list)`:
                Stores extracted entities dataset from the response.

            3). `self.content_uploaded (list)`:
                Stores succesfully uploaded content objects.
                !Note that some objects could be already existing in database.
                That case would not append objects to this attribute.

            4). `self.content_handled (list)`:
                Stores all handled objects.

        Args:
            1). `response (dict)`:
                The response from Musixmatch API request.
        """

        self.response = response
        self.content_to_insert = []
        self.content_uploaded = []
        self.content_handled = []

    def search_tracks_data(self):
        """
        Extracts `track` datasets from the `self.response` and stores in `self.content_to_insert`

        Method searches for `track` keys in the `self.response` recursively and
        stores their values in `self.content_to_insert` as {'track': value}.
        """

        for key, value in self.response.items():
            if key == 'track':
                self.content_to_insert.append({'track': value})
            elif isinstance(value, dict):
                self.search_tracks_data(value)
            continue

    def upload_tracks_to_db(self):
        """
        Uploads tracks with depended entities (author, album, genres) in a database.

        Method extracts `track` datasets from `self.content_to_insert`,
        handles them and uploads using 5-8 cls methods if `track` doesn't already exist.
        Relevant records in a `self.content_uploaded` and `self.content_handled` are updated.
        """

        track_datasets = list(filter(lambda x: x.get('track'), self.content_to_insert))
        for dataset in track_datasets:
            track, status = self._get_or_create_track_object(dataset)
            if status is True:
                track.author = self._get_or_create_artist_object(dataset)[0]
                track.album = self._get_or_create_album_object(dataset)[0]
                track.genres.set([
                    self._get_or_create_genre_object(genre)[0]
                    for genre in dataset['primary_genres']['music_genre_list']
                ])
                track.save()
            continue

    def retrieve_handled_track_objects(self):
        """Returns all handled `Tracks` objects."""

        return list(filter(lambda x: isinstance(x, Tracks), self.content_handled))

    def _get_or_create_track_object(self, track_data: dict) -> tuple:
        """
        Creates `Tracks` object if it doesn`t already exist in a database otherwise retrieves.
        Updates `self.content_handled` and `self.content_uploaded` respectively with object.

        Args:
            1). `track_data (dict)`:
                A dataset that has `track_id` and `track_name` keys;

        Returns:
            `tuple(track: `Tracks`, upload_status: bool)`:
            `upload_status` is True if object wasn't existing in a database and it was uploaded otherwise False.
        """

        track, upload_status = Tracks.objects.get_or_create(
                id_musixmatch=track_data['track_id'],
                name=track_data['track_name']
            )
        self.content_handled.append({'track': track})
        if upload_status is True:
            self.content_uploaded.append({'track': track})
        return track, upload_status

    def _get_or_create_album_object(self, album_data: dict) -> tuple:
        """
        Creates `Albums` object if it doesn`t already exist in a database otherwise retrieves.
        Updates `self.content_handled` and `self.content_uploaded` respectively with object.

        Args:
            1). `album_data (dict)`:
                A dataset that has `album_id` and `album_name` keys.

        Returns:
            `tuple(track: `Albums`, upload_status: bool)`:
            `upload_status` is True if object wasn't existing in a database and it was uploaded otherwise False.
        """

        album, upload_status = Albums.objects.get_or_create(
            id_musixmatch=album_data['album_id'],
            name=album_data['album_name']
        )
        self.content_handled.append({'album': album})
        if upload_status is True:
            self.content_uploaded.append({'album': album})
        return album, upload_status

    def _get_or_create_artist_object(self, artist_data: dict):
        """
        Creates `Artists` object if it doesn`t already exist in a database otherwise retrieves.
        Updates `self.content_handled` and `self.content_uploaded` respectively with object.

        Args:
            1). `artist_data (dict)`:
                A dataset that has `artistid` and `artistname` keys;

        Returns:
            `tuple(track: `Artists`, upload_status: bool)`:
            `upload_status` is True if object wasn't existing in a database and it was uploaded otherwise False.
        """

        artist, upload_status = Artists.objects.get_or_create(
            id_musixmatch=artist_data['artist_id'],
            name=artist_data['artist_name']
        )
        self.content_handled.append({'artist': artist})
        if upload_status is True:
            self.content_uploaded.append({'artist': artist})
        return artist, upload_status

    def _get_or_create_genre_object(self, genre_data: dict) -> tuple:
        """
        Creates `Genres` object if it doesn`t already exist in a database otherwise retrieves.
        Updates `self.content_handled` and `self.content_uploaded` respectively with object.

        Args:
            1). `genre_data (dict)`:
                A dataset that has `music_genre.music_genre_id` and `music_genre.music_genre_name` keys;

        Returns:
            `tuple(track: `Genres`, upload_status: bool)`:
            `upload_status` is True if object wasn't existing in a database and it was uploaded otherwise False.
        """

        genre, upload_status = Genres.objects.get_or_create(
            id_musixmatch=genre_data['music_genre']['music_genre_id'],
            name=genre_data['music_genre']['music_genre_name']
        )
        self.content_handled.append({'genre': genre})
        if upload_status is True:
            self.content_uploaded.append({'genre': genre})
        return genre, upload_status
