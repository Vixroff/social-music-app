from django.urls import path, include

from . import views


urlpatterns = [
    path(
        '',
        views.WelcomeView.as_view(),
        name='welcome'
    ),
    path('auth/', include([
        path(
            'login/',
            views.MyLoginView.as_view(),
            name='login',
        ),
        path('', include('django.contrib.auth.urls')),
    ])),
    path('users/', include([
        path(
            '',
            views.RegistrationView.as_view(),
            name='registration',
        ),
        path(
            '<int:user_pk>',
            views.UserProfileView.as_view(),
            name='profile-view',
        ),
        path(
            '<int:user_pk/delete>',
            views.DeleteUserProfileView.as_view(),
            name='delete-profile',
        ),
        path(
            '<int:user_pk>/tracks/add',
            views.UserAddTrackView.as_view(),
            name='add-track',
        ),
        path(
            '<int:user_pk>/tracks/<int:track_pk>/delete',
            views.UserDeleteTrackView.as_view(),
            name='delete-track',
        ),
        path(
            '<int:user_pk>/playlists/like',
            views.UserLikePlaylistView.as_view(),
            name='like-playlist',
        ),
        path(
            '<int:user_pk>/playlists/<int:playlist_pk>/unlike',
            views.UserUnlikePlaylistView.as_view(),
            name='unlike-playlist',
        ),
        path(
            '<int:user_pk>/followings',
            views.UserFollowView.as_view(),
            name='follow',
        ),
        path(
            '<int:user_pk>/followings/<int:following_pk>',
            views.UserUnfollowView.as_view(),
            name='unfollow',
        ),
    ])),
    path('playlists/', include([
        path(
            '',
            views.CreatePlaylistView.as_view(),
            name='create-playlist',
        ),
        path(
            '<int:playlist_pk>',
            views.PlaylistView.as_view(),
            name='playlist-view',
        ),
        path(
            '<int:playlist_pk>/delete',
            views.DeletePlaylistView.as_view(),
            name='delete-playlist',
        ),
        path(
            '<int:playlist_pk>/comments/add',
            views.AddCommentView.as_view(),
            name='add-comment',
        ),
        path(
            '<int:playlist_pk>/comments/<int:comment_id>/delete',
            views.DeleteCommentView.as_view(),
            name='delete-comment',
        ),
        path(
            '<int:playlist>/tracks/add',
            views.AddTrackToPlaylistView.as_view(),
            name='add-track-to-playlist',
        ),
        path(
            '<int:playlist>/tracks/<int:track_id>/delete',
            views.DeleteTrackFromPlaylistView.as_view(),
            name='delete-track-from-playlist',
        ),
    ])),
    path('content/', include([
        path(
            'search',
            views.SearchView.as_view(),
            name='search',
        ),
        path(
            'top-artists',
            views.TopArtistsView.as_view(),
            name='top_artists',
        ),
        path(
            'top-tracks',
            views.TopTracksView.as_view(),
            name='top_tracks',
        ),
        path(
            'recommendations',
            views.RecommendationsView.as_view(),
            name='recommendations',
        )
    ]))      
]
