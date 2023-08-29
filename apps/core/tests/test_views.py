from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from ..views import HomeView, PortfolioView


class CoreViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test.user', password=get_random_string(12))

    def test_home_view(self):
        url = reverse('core:index')
        request = self.factory.get(url)
        request.user = self.user

        response = HomeView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')

    def test_portfolio_view_authenticated(self):
        url = reverse('core:portfolio')
        request = self.factory.get(url)
        request.user = self.user

        response = PortfolioView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Portfolio')

    def test_add_coin_to_portfolio(self):
        coin_id = "bitcoin"        
        url = f"{reverse('core:portfolio')}?coin_id={coin_id}"
        request = self.factory.get(url)
        request.user = self.user

        response = PortfolioView.as_view()(request)

        self.assertEqual(response.status_code, 200) 

