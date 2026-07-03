from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ChatAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_unauthenticated_login_view(self):
        # GET request when not logged in should return login form
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat_app/login.html')

    def test_authenticated_login_view_redirects(self):
        # Log the user in
        self.client.login(username=self.username, password=self.password)
        # GET request when logged in should redirect to index
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('index'))

        # GET request to home/root when logged in should redirect to index
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('index'))

    def test_logout_only_allows_post(self):
        # Log the user in
        self.client.login(username=self.username, password=self.password)

        # GET request to logout should be rejected (405 Method Not Allowed)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)

        # POST request to logout should succeed and redirect to login
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_index_requires_login(self):
        # Unauthenticated access to index redirects to login
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('index')}")

        # Authenticated access to index returns 200
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
