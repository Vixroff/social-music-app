from rest_framework import serializers

from app.models import CustomUser, Tracks, Playlists


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'url', 
            'username', 
            'email',
            'date_joined',
            'is_staff',
        ]


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    creator = UserSerializer()

    class Meta:
        model = Playlists
        fields = '__all__'
