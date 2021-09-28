from api.models import Album, Photo, Tag
from api.serializers import AlbumSerializer, UserSerializer, PhotoSerializer, TagSerializer
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions


class RegisterUser(generics.CreateAPIView):
    """ Registration of user """

    model = get_user_model()
    serializer_class = UserSerializer


class AlbumList(generics.ListCreateAPIView):
    """ Return Album list """

    def get_queryset(self):
        """ Filter user albums only, restrict access to albums of other users """

        return Album.objects.all().filter(author=self.request.user)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AlbumSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ['album_name', 'total_photos']


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Return Detail of Album """

    def get_queryset(self):
        """ Filter user albums only, restrict access to albums of other users """

        return Album.objects.all().filter(author=self.request.user)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AlbumSerializer


class PhotoList(generics.ListCreateAPIView):
    """ Return Photo list """

    def get_queryset(self):
        """ Filter user photo only, restrict access to photos of other users """

        return Photo.objects.all().filter(album__author=self.request.user)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['album__album_name', 'tag__tag_name']
    ordering_fields = ['date_created', 'album']


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Return Detail of Photo """

    def get_queryset(self):
        """ Filter user photo only, restrict access to photos of other users """

        return Photo.objects.all().filter(album__author=self.request.user)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoSerializer


class TagList(generics.ListCreateAPIView):
    """ Return Tag list """

    def get_queryset(self):
        """ Filter user tags only, restrict access to tags of other users """

        return Tag.objects.all().filter(user=self.request.user)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Return Detail of Tag """

    def get_queryset(self):
        """ Filter user tags only, restrict access to tags of other users """

        return Tag.objects.all().filter(user=self.request.user)

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TagSerializer
