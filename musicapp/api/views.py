from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import JSONParser

from .serializers import UserSerializer, PlaylistSerializer, TrackSerializer
from app.models import CustomUser, Playlists, Tracks


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


def playlist_list(request):
    """
    List all code snippets, or create a new playlist.
    """
    if request.method == 'GET':
        playlists = Playlists.objects.all()
        serializer = PlaylistSerializer(playlists, many=True )
        return JsonResponse(serializer.data, safe=False)
    
    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = SnippetSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
def playlist_detail(request, pk):
    """
    Retrieve, update or delete a code playlist.
    """
    try:
        playlist = Playlists.objects.get(pk=pk)
    except Playlists.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PlaylistSerializer(playlist)
        return JsonResponse(serializer.data)

    # elif request.method == 'PUT':
    #     data = JSONParser().parse(request)
    #     serializer = SnippetSerializer(snippet, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data)
    #     return JsonResponse(serializer.errors, status=400)

    # elif request.method == 'DELETE':
    #     snippet.delete()
    #     return HttpResponse(status=204)


