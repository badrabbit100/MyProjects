from rest_framework import serializers
from api.models import Album, Photo, Tag
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework.fields import CurrentUserDefault


class AlbumSerializer(serializers.ModelSerializer):
    """ Albums serializer class """

    album_name = serializers.CharField(
        required=True,
        max_length=32,
        validators=[UniqueValidator(queryset=Album.objects.all())]
    )

    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'total_photos')


class UserSerializer(serializers.ModelSerializer):
    """ Register new user """

    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=32, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=6, max_length=100, write_only=True)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', )
        read_only_fields = ('id', 'date_created')


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """ Tag serializer class """

    tag_name = serializers.CharField(
        required=True,
        max_length=15,
        validators=[UniqueValidator(queryset=Tag.objects.all())]
    )

    def save(self):
        user = CurrentUserDefault()
        tag_name = self.validators['tan_name']

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('id', 'user')
