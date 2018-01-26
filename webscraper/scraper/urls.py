from django.conf.urls import url

from scraper.views import TwitterProfileDetail, TwitterProfileList

urlpatterns = [
    url(r'^profiles/$', TwitterProfileList.as_view()),
    url(r'^profiles/(?P<screen_name>[\w\-]+)/$', TwitterProfileDetail.as_view()),
]