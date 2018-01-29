# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from scraper.models import TwitterProfile
from scraper.services.TwitterProfileScraper import TwitterProfileScraper
from scraper.utils import DataFormatter


class TwitterProfileList(APIView):

    def get(self, request):
        profiles = list(TwitterProfile.objects.all())
        result = DataFormatter.get_format_data(profiles)
        return Response(result)


class TwitterProfileDetail(APIView):

    def get(self, request, screen_name):
        status_code = None
        try:
            profile = TwitterProfile.objects.get(screen_name=screen_name)
        except TwitterProfile.DoesNotExist:
            profile = None

        if profile is None:
            scraper = TwitterProfileScraper(screen_name)
            profile = scraper.get_profile()
            if profile is None:
                result = DataFormatter.get_data_404_not_found()
                status_code = HTTP_404_NOT_FOUND
            else:
                profile = TwitterProfile.objects.create(
                    screen_name=profile['screen_name'],
                    name=profile['name'],
                    bio_description=profile['bio_description'],
                    followers=profile['followers'],
                    avatar_url=profile['avatar_url']
                    )
                result = DataFormatter.get_format_profile(profile)
                result = dict(data=result)
        else:
            result = DataFormatter.get_format_profile(profile)
            result = dict(data=result)

        return Response(result, status=status_code)