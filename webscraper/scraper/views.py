# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from scraper.models import TwitterProfile
from scraper.serializers import TwitterProfileSerializer
from scraper.services.TwitterProfileScraper import TwitterProfileScraper


class TwitterProfileList(APIView):
    def get(self, request):
        profiles = TwitterProfile.objects.all()
        result = TwitterProfileSerializer(profiles, many=True)
        return Response(result.data)

class TwitterProfileDetail(APIView):
    def get(self, request, screen_name):
        status_code = None
        try:
            profile = TwitterProfile.objects.get(screen_name=screen_name)
        except TwitterProfile.DoesNotExist:
            scraper = TwitterProfileScraper(screen_name)
            profile = scraper.get_profile()
            if profile is None:
                error = {
                    'type': settings.NOT_FOUND_ERROR,
                    'message': settings.NOT_FOUND_MESSAGE
                    }
                result = dict(error=error)
                status_code = HTTP_404_NOT_FOUND
                return Response(result, status=status_code)
            else:
                profile = TwitterProfile.objects.create(
                    screen_name=profile['screen_name'],
                    name=profile['name'],
                    bio_description=profile['bio_description'],
                    followers=profile['followers'],
                    avatar_url=profile['avatar_url']
                    )
                result = TwitterProfileSerializer(profile)
        else:
            result = TwitterProfileSerializer(profile)

        return Response(result.data, status=status_code)