from django.test import TestCase
from django.urls import reverse
from .. import views


class TestCoreURLs(TestCase):
    def test_home_url_resolves(self):
        url = reverse("core:index")
        self.assertEqual(url, "/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "index.html"
        )  # Check if the correct template is used
        self.assertIsInstance(
            response.context["view"], views.HomeView
        )  # Check if the correct view is used

    def test_portfolio_url_resolves(self):
        url = reverse("core:portfolio")
        self.assertEqual(url, "/portfolio/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(
            response, "portfolio.html"
        )  # Check if the correct template is used
