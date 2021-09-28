from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [

    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('login/', obtain_auth_token, name='login_user'),

    path('albums/', views.AlbumList.as_view(), name='albums'),
    path('album/<int:pk>/', views.AlbumDetail.as_view(), name='album_detail'),

    path('photos/', views.PhotoList.as_view(), name='photos'),
    path('photo/<int:pk>/', views.PhotoDetail.as_view(), name='photo_detail'),

    path('tags/', views.TagList.as_view(), name='tags'),
    path('tag/<int:pk>/', views.TagDetail.as_view(), name='tag_detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
