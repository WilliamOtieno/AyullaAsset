from django.urls import path
from . import views


app_name = "core"
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("portfolio/", views.PortfolioView.as_view(), name="portfolio"),
]
