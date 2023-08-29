from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from ...core.models import ReferralCode
from ..views import LoginView, LogoutView, SignUpView


class TestAuthViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.referral_code = ReferralCode.objects.create(user=self.user, code="TESTCODE")

    def test_login_view_get(self):
        request = self.factory.get(reverse('authentication:login'))
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Submit')

    def test_login_view_post_valid_user(self):
        request = self.client.post(reverse('authentication:login'), {'username': 'testuser', 'password': 'testpass'})
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('core:portfolio'))  # Assuming redirect to portfolio
  
    def test_signup_view_get(self):
        request = self.factory.get(reverse('authentication:signup'))
        response = SignUpView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Submit')

    def test_signup_view_post_valid_code(self):
        request = self.factory.post(reverse('authentication:signup'), {'username': 'newuser', 'code': 'TESTCODE', 'password1': 'newpass', 'password2': 'newpass'})
        response = SignUpView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('core:portfolio'))  # Assuming redirect after successful signup

    def test_signup_view_post_invalid_code(self):
        request = self.factory.post(reverse('authentication:signup'), {'username': 'newuser', 'code': 'INVALIDCODE', 'password1': 'newpass', 'password2': 'newpass'})
        response = SignUpView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('core:portfolio'))  # Assuming redirect after unsuccessful signup

