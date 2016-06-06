'''Shorty Tests'''

from django.test import TestCase, Client
from django.contrib.auth.models import User

import mock

from .models import ShortURL
from .forms import ShortURLForm
from . import views


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')
        super(UserTestCase, self).setUp()


class ModelTestCase(UserTestCase):

    def test_random_slug_generation(self):
        one = ShortURL.objects.create(redirect='http://www.google.com', user=self.user)
        two = ShortURL.objects.create(redirect='http://www.foo.com', user=self.user)
        self.assertNotEqual(one.path, two.path)
        self.assertNotEqual(one.path, '')
        self.assertNotEqual(two.path, '')


class RedirectViewTestCase(UserTestCase):

    def setUp(self):
        super(RedirectViewTestCase, self).setUp()
        ShortURL.objects.create(redirect='http://www.google.com', path='google', user=self.user, external=True)
        ShortURL.objects.create(redirect='http://www.foo.com', path='foo', user=self.user)
        self.client = Client()

    def test_missing_slug(self):
        '''Missing slugs should raise a 404'''
        response = self.client.get('/404')
        self.assertEqual(response.status_code, 404)

    def test_no_slug(self):
        '''No slug at all should redirect to admin'''
        response = self.client.get('/', HTTP_HOST='shorty.example.com')
        self.assertRedirects(response, '/admin/', host='shorty.example.com', fetch_redirect_response=False)

    def test_no_slug_no_host_header(self):
        '''No slug (and no Host header) should return a 400 Bad Request'''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_redirect_canonical_false_external_false(self):
        '''Unauthenticated clients - no settings: should simply get redirects'''
        response = self.client.get('/google')
        self.assertRedirects(response, 'http://www.google.com', fetch_redirect_response=False)
        response = self.client.get('/foo/')
        self.assertRedirects(response, 'http://www.foo.com', fetch_redirect_response=False)

    @mock.patch.object(views, 'EXTERNAL_FLAG', True)
    def test_unauthenticated_redirect_canonical_false_external_true(self):
        '''Unauthenticated clients, external access'''
        with self.settings(LOGIN_URL='/login/'):
            # External=True objects should return redirect
            response = self.client.get('/google')
            self.assertRedirects(response, 'http://www.google.com', fetch_redirect_response=False)
            # External=False objects should force login
            response = self.client.get('/foo/')
            self.assertRedirects(response, '/login/?next=/foo/', fetch_redirect_response=False)

    @mock.patch.object(views, 'CANONICAL_DOMAIN', 'http://shorty.example.com')
    def test_unauthenticated_redirect_canonical_true_external_false(self):
        '''Unauthenticated clients, no external access, canonical domain'''
        # Matching domain and scheme should redirect like usual
        response = self.client.get('/google', HTTP_HOST='shorty.example.com')
        self.assertRedirects(response, 'http://www.google.com', fetch_redirect_response=False)
        # Not matching domain should redirect to matching domain
        response = self.client.get('/google', HTTP_HOST='shorty1.example.com')
        self.assertRedirects(response, 'http://shorty.example.com/google', fetch_redirect_response=False)

    @mock.patch.object(views, 'CANONICAL_DOMAIN', 'https://shorty.example.com')
    def test_unauthenticated_redirect_canonical_https_external_false(self):
        '''Unauthenticated clients, no external access, canonical domain'''
        # Non matching schcme should redirect to matching
        response = self.client.get('/google', HTTP_HOST='shorty.example.com')
        self.assertRedirects(response, 'https://shorty.example.com/google', fetch_redirect_response=False)

    @mock.patch.object(views, 'EXTERNAL_FLAG', True)
    def test_authenticated_redirect_canonical_false_external_true(self):
        '''Authenticated clients, external access, redirects should work'''
        self.client.login(username='test', password='test')
        response = self.client.get('/foo')
        self.assertRedirects(response, 'http://www.foo.com', fetch_redirect_response=False)

    def test_preview(self):
        '''Test preview domain'''
        response = self.client.get('/google?preview=True')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("<a href='/google'>http://www.google.com</a>", response.content)
        response = self.client.get('/google?p=True')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("<a href='/google'>http://www.google.com</a>", response.content)


class AuthenticatedUITestCase(UserTestCase):

    def setUp(self):
        super(AuthenticatedUITestCase, self).setUp()
        ShortURL.objects.create(redirect='http://www.google.com', path='google', user=self.user, external=True)
        ShortURL.objects.create(redirect='http://www.foo.com', path='foo', user=self.user)
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_delete_short_url(self):
        id_short_url = ShortURL.objects.get(path='google').pk
        response = self.client.post('/admin/delete/', {'id_short_url': id_short_url})
        self.assertRedirects(response, '/admin/', fetch_redirect_response=False)
        response = self.client.post('/admin/delete/', {'id_short_url': id_short_url})
        self.assertEqual(response.status_code, 400)
