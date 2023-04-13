from django.test import Client, TestCase
from django.urls import reverse

from app.models import CustomUser, Tracks, Playlists


class CreatePlaylistViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_playlist')
        self.user = CustomUser.objects.create(
            username='test1',
            email='test@test.test'
        )
        self.user.set_password('test123test')
        self.user.save()
        self.tracks = [
            Tracks.objects.create(name='testtrack1', id_musixmatch=1),
            Tracks.objects.create(name='testtrack2', id_musixmatch=2),
            Tracks.objects.create(name='testtrack3', id_musixmatch=3)
        ]
        self.user.added_tracks.set(self.tracks)

    def test_request_get_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('login') + '?next=' + self.url, response.url)

    def test_request_get_authenticated_user(self):
        self.client.login(username=self.user.username, password='test123test')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_request_post_authenticated_user(self):
        self.client.login(username=self.user.username, password='test123test')
        response = self.client.post(
            self.url,
            {
                'name': 'playlist_test_name',
                'creator': self.user.id,
                'tracks': [self.tracks[0].id, self.tracks[1].id]
            },
            follow=True
        )
        self.assertRedirects(response, reverse('profile'), status_code=302, target_status_code=200)
        self.assertEqual(1, Playlists.objects.count())
