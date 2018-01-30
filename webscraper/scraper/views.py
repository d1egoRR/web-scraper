# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from scraper.models import TwitterProfile
from scraper.services.TwitterProfileScraper import TwitterProfileScraper
from scraper.utils import ProfileTransformer


class TwitterProfileList(APIView):
    def get(self, request):
        profiles = tuple(TwitterProfile.objects.all())
        transformer = ProfileTransformer()
        result = transformer.get_transformed_data(profiles)
        return Response(result)


class TwitterProfileDetail(APIView):
    def get(self, request, screen_name):
        status_code = None
        transformer = ProfileTransformer()
        try:
            profile = TwitterProfile.objects.get(screen_name=screen_name)
        except TwitterProfile.DoesNotExist:
            scraper = TwitterProfileScraper(screen_name)
            profile = scraper.get_profile()
            if profile is None:
                result = transformer.get_data_404()
                status_code = HTTP_404_NOT_FOUND
            else:
                profile = TwitterProfile.objects.create(
                    screen_name=profile['screen_name'],
                    name=profile['name'],
                    bio_description=profile['bio_description'],
                    followers=profile['followers'],
                    avatar_url=profile['avatar_url']
                    )
                result = transformer.get_transformed_data(profile)
        else:
            result = transformer.get_transformed_data(profile)

        return Response(result, status=status_code)