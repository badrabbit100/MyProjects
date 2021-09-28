from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.room_view, name='start_view'),
    path("play/<room_code>", views.play_view, name="play_view"),
    path("quit/<str:room_code>", views.quit_view, name='quit'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

