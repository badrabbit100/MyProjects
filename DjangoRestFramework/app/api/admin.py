from django.contrib import admin
from .models import Album, Tag, Photo


admin.site.register(Album)
admin.site.register(Tag)
admin.site.register(Photo)
