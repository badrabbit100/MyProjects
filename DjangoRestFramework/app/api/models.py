from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
import os


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def validate_photo_extension(value):
    """ Validate Photo format and file size before save in """

    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.jpeg']
    valid_size = 5242880
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file type')
    if value.size > valid_size:
        raise ValidationError('Unsupported file size. Max-size is 5 Mb')


class Album(models.Model):
    """ This is Album model define album name, author name and date of album created """

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    album_name = models.CharField(max_length=50, verbose_name='Album Name')
    total_photos = models.DecimalField(max_digits=8, decimal_places=0, verbose_name='Total Photos', default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')

    def __str__(self):
        return '{}'.format(self.album_name)


class Tag(models.Model):
    """ Tag model define name tag and owner of tags """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    tag_name = models.CharField(max_length=50, verbose_name='Tag Name')

    def __str__(self):
        return '{}'.format(self.tag_name)


class Photo(models.Model):
    """ This model keep album name, tag, photo name and date created """

    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='Album')
    tag = models.ManyToManyField(Tag, verbose_name='Tag')
    photo_name = models.CharField(max_length=500, verbose_name='Name of Photo')
    photo = models.ImageField(upload_to='photo', verbose_name='Photo', null=True, validators=[validate_photo_extension])
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')

    def __str__(self):
        return 'Album: {} | Photo: {} | Tag: {}'.format(self.album, self.photo_name, self.tag)
