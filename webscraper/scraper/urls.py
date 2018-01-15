from django.conf.urls import url

from scraper.views import TwitterScraper

urlpatterns = [
    url(r'^get_profile/', TwitterScraper.as_view(), name='twittescraper'),
]