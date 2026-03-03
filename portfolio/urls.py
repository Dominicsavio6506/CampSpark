from django.urls import path
from .views import portfolio_page
from django.urls import include

urlpatterns = [
    path("", portfolio_page, name="portfolio_page"),
    path("portfolio/", include("portfolio.urls")),

]
