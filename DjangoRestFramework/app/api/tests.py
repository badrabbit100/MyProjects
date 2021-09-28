import datetime
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from .models import Album, Photo, Tag


class UserRegistrationTest(APITestCase):
    def setUp(self):
        # Create testing User for validation unique users
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL for testing
        self.test_create_url = reverse('register_user')

    def test_register_user(self):
        """ Ensure we can create a new user  """

        data = {
            'username': 'NewUser',
            'email': 'NewUserEmail@user.com',
            'password': 'Somepassword1'
        }
        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_register_user_with_short_password(self):
        """ Ensures user is not created for password lengths less than 8 """

        data = {
            'username': 'NewUser',
            'email': 'NewUserEmail@user.com',
            'password': 'Some'
        }

        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_register_user_with_no_password(self):
        data = {
            'username': 'NewUser',
            'email': 'NewUserEmail@user.com',
            'password': ''
        }

        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_register_user_with_too_long_username(self):
        data = {
            'username': 'NewUser' * 35,
            'email': 'NewUserEmail@user.com',
            'password': 'Somepassword1'
        }

        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_register_user_with_no_username(self):
        data = {
            'username': '',
            'email': 'NewUserEmail@user.com',
            'password': 'Somepassword1'
        }

        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_register_user_with_preexisting_username(self):
        data = {
            'username': 'testuser',
            'email': 'NewUserEmail@user.com',
            'password': 'Somepassword1'
        }

        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_register_user_with_preexisting_email(self):
        data = {
            'username': 'NewUser',
            'email': 'test@example.com',
            'password': 'Somepassword1'
        }

        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_register_user_with_invalid_email(self):
        data = {
            'username': 'NewUser',
            'email': 'NewUserEmail',
            'passsword': 'Somepassword1'
        }

        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_register_user_with_no_email(self):
        data = {
            'username': 'NewUser',
            'email': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.test_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)


class AlbumsTests(APITestCase):
    """
    This class include testing of Albums API (GET, POST)
    Testing get Album list and create new albums
    """

    def setUp(self):
        self.test_user = User.objects.create_user('Author', 'test@example.com', 'Testpassword1')
        self.test_album = Album.objects.create(album_name='Test_album', author=self.test_user)

        self.test_user_other = User.objects.create_user('Author2', 'test2@example.com', 'Testpassword1')
        self.test_album2 = Album.objects.create(album_name='Test_album', author=self.test_user_other)

        # URL for testing
        self.test_create_url = reverse('albums')
        # Login Client for testing
        self.client.force_login(user=self.test_user)

    def response_hanlder(self,  data_request, field, test_status):
        response = self.client.post(self.test_create_url, data_request, format='json')
        self.assertEqual(response.status_code, test_status)
        self.assertEqual(Album.objects.filter(author=self.test_user).count(), 1)
        self.assertEqual(len(response.data[field]), 1)

    def test_create_new_album(self):
        """ Ensure we can create a new Album  """

        data = {
            'album_name': 'NewAlbum',
            'author': self.test_user.id
        }
        response = self.client.post(self.test_create_url, data, format='json')

        self.assertEqual(Album.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['album_name'], data['album_name'])
        self.assertEqual(response.data['author'], data['author'])

    def test_get_album_lists_of_owner(self):
        """ Ensure we can get Album list User Only without other users  """

        data = {}
        response = self.client.get(self.test_create_url, data, format='json')

        self.assertEqual(Album.objects.filter(author=self.test_user).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author'], self.test_user.id)

    def test_create_new_album_with_preexisting(self):
        """ Ensure we can not create new Album with preexisting """

        data = {
            'album_name': 'Test_album',
            'author': self.test_user.id
        }
        self.response_hanlder(data_request=data, field='album_name', test_status=status.HTTP_400_BAD_REQUEST)

    def test_create_new_album_too_long_album_name(self):
        """ Ensure we can not create new Album with too long name """

        data = {
            'album_name': 'Test_album' * 35,
            'author': self.test_user.id
        }

        self.response_hanlder(data_request=data, field='album_name', test_status=status.HTTP_400_BAD_REQUEST)

    def test_create_new_album_without_album_name(self):
        """ Ensure we can not create new Album without album name """

        data = {
            'album_name': '',
            'author': self.test_user.id
        }

        self.response_hanlder(data_request=data, field='album_name', test_status=status.HTTP_400_BAD_REQUEST)

    def test_create_new_album_without_author(self):
        """ Ensure we can not create new Album with too long name """

        data = {
            'album_name': 'NewAlbum',
            'author': ''
        }

        self.response_hanlder(data_request=data, field='author', test_status=status.HTTP_400_BAD_REQUEST)

    def test_create_new_album_with_string_in_author_field(self):
        """ Ensure we can not create new Album with non-integer value in Author field """

        data = {
            'album_name': 'NewAlbum',
            'author': 'randomstring'
        }

        self.response_hanlder(data_request=data, field='author', test_status=status.HTTP_400_BAD_REQUEST)


class AlbumDetailsTests(APITestCase):
    """ This class include testing of Album Details API (GET, PUT, DELETE)"""

    def setUp(self):
        self.test_user = User.objects.create_user('Author', 'test@example.com', 'Testpassword1')
        self.test_album = Album.objects.create(album_name='Test_album', author=self.test_user)
        self.new_date = self.test_album.date_created + datetime.timedelta(days=2)
        self.test_user_other = User.objects.create_user('Author2', 'test2@example.com', 'Testpassword2')
        self.test_album_other_user = Album.objects.create(album_name='Test_album2', author=self.test_user_other)

        # URL for testing
        self.test_detail_url = reverse('album_detail', kwargs={'pk': self.test_album.id})
        self.test_detail_url_other_user = reverse('album_detail', kwargs={'pk': self.test_album_other_user.id})

        # Login Client for testing
        self.client.force_login(user=self.test_user)

    def test_get_one_album(self):
        """ Ensure we can get all album fields from model, exclude Album-ID """

        data = {}
        response = self.client.get(self.test_detail_url, data, format='json')
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['album_name'], self.test_album.album_name)
        self.assertEqual(response.data['author'], self.test_user.id)
        response_date = response.data['date_created'].split('.')[0]
        self.assertEqual(response_date, self.test_album.date_created.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(response.data['total_photos'], str(self.test_album.total_photos))

    def test_update_album_name_and_date_created_field(self):
        """ Ensure we can update album name and can not update date_created field in album """
        data = {
            'album_name': 'NewAlbum',
            'author': self.test_user.id,
            'date_created': self.new_date,
        }

        response = self.client.put(self.test_detail_url, data, format='json')
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['album_name'], data['album_name'])
        self.assertEqual(response.data['author'], data['author'])
        self.assertNotEqual(response.data['date_created'].split('.')[0], self.new_date.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_update_preexisting_album_name_other_user(self):
        """ Ensure we can not update existing album name of other user """

        data = {
            'album_name': 'NewAlbum2',
            'author': self.test_user.id
        }
        response = self.client.put(self.test_detail_url_other_user, data, format='json')
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_album_name_without_name(self):
        """ Ensure we can not update existing album name without new name """

        data = {
            'album_name': ' ',
            'author': self.test_user.id
        }
        response = self.client.put(self.test_detail_url, data, format='json')
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['album_name']), 1)

    def test_update_album_name_with_incorrect_author_id(self):
        """ Ensure we can not update existing album name with incorrect author_id """

        data = {
            'album_name': 'NewAlbum',
            'author': 'random_id'
        }
        response = self.client.put(self.test_detail_url, data, format='json')
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data['author'], data['author'])

    def test_update_album_name_without_author_id(self):
        """ Ensure we can not update existing album name without author_id """

        data = {
            'album_name': 'NewAlbum',
            'author': ''
        }
        response = self.client.put(self.test_detail_url, data, format='json')
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data['author'], data['author'])

    def test_delete_album(self):
        """ Ensure we can delete Album """

        data = {}
        response = self.client.delete(self.test_detail_url, data, format='json')
        self.assertEqual(Album.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_album_other_user(self):
        """ Ensure we can not delete Album of other user """

        data = {}
        response = self.client.delete(self.test_detail_url_other_user, data, format='json')
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PhotosTests(APITestCase):
    """
    This class include testing of Photo API (GET, POST)
    Testing GET LIST photos and CREATE new photo
    """

    def setUp(self):
        self.test_user = User.objects.create_user('Author', 'test@example.com', 'Testpassword1')
        self.test_album = Album.objects.create(album_name='Test_album', author=self.test_user)
        self.test_photo = Photo.objects.create(
            photo_name='Test_Photo',
            album=self.test_album,

        )

        self.test_user_other = User.objects.create_user('Author2', 'test2@example.com', 'Testpassword1')
        self.test_album2 = Album.objects.create(album_name='Test_album', author=self.test_user_other)

        # URL for testing
        self.test_create_url = reverse('albums')
        # Login Client for testing
        self.client.force_login(user=self.test_user)

    def test_create_new_album(self):
        """ Ensure we can create a new Album  """

        data = {
            'album_name': 'NewAlbum',
            'author': self.test_user.id
        }
        response = self.client.post(self.test_create_url, data, format='json')

        self.assertEqual(Album.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['album_name'], data['album_name'])
        self.assertEqual(response.data['author'], data['author'])

'''
    def test_get_album_lists_of_owner(self):
        """ Ensure we can get Album list User Only without other users  """

        data = {}
        response = self.client.get(self.test_create_url, data, format='json')

        self.assertEqual(Album.objects.filter(author=self.test_user).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author'], self.test_user.id)

    def test_create_new_album_with_preexisting(self):
        """ Ensure we can not create new Album with preexisting """

        data = {
            'album_name': 'Test_album',
            'author': self.test_user.id
        }
        self.response_hanlder(data_request=data, field='album_name', test_status=status.HTTP_400_BAD_REQUEST)

    def test_create_new_album_too_long_album_name(self):
        """ Ensure we can not create new Album with too long name """

        data = {
            'album_name': 'Test_album' * 35,
            'author': self.test_user.id
        }

        self.response_hanlder(data_request=data, field='album_name', test_status=status.HTTP_400_BAD_REQUEST)

    def test_create_new_album_without_album_name(self):
        """ Ensure we can not create new Album without album name """

        data = {
            'album_name': '',
            'author': self.test_user.id
        }

        self.response_hanlder(data_request=data, field='album_name', test_status=status.HTTP_400_BAD_REQUEST)

    def test_create_new_album_without_author(self):
        """ Ensure we can not create new Album with too long name """

        data = {
            'album_name': 'NewAlbum',
            'author': ''
        }

        self.response_hanlder(data_request=data, field='author', test_status=status.HTTP_400_BAD_REQUEST)

    def test_create_new_album_with_string_in_author_field(self):
        """ Ensure we can not create new Album with non-integer value in Author field """

        data = {
            'album_name': 'NewAlbum',
            'author': 'randomstring'
        }

        self.response_hanlder(data_request=data, field='author', test_status=status.HTTP_400_BAD_REQUEST)
'''