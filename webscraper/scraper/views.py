# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_504_GATEWAY_TIMEOUT)
from rest_framework.views import APIView

from scraper.models import TwitterProfile
from scraper.serializers import TwitterProfileSerializer
from scraper.services.TwitterProfileScraper import TwitterProfileScraper


ERRORS = {
    HTTP_404_NOT_FOUND: settings.ERROR_404,
    HTTP_504_GATEWAY_TIMEOUT: settings.ERROR_504
}


class TwitterProfileList(APIView):
    def get(self, request):
        profiles = TwitterProfile.objects.all()
        result = TwitterProfileSerializer(profiles, many=True)
        return Response(result.data)

class TwitterProfileDetail(APIView):
    def get(self, request, screen_name):
        status_code = None
        profile = self.get_object(screen_name)
        if profile is None:
            scraper = TwitterProfileScraper(screen_name)
            if scraper.connection_status == HTTP_504_GATEWAY_TIMEOUT:
                result = dict(error=ERRORS[HTTP_504_GATEWAY_TIMEOUT])
                status_code = HTTP_504_GATEWAY_TIMEOUT
            else:
                profile = scraper.get_profile()
                if profile is None:
                    result = dict(error=ERRORS[HTTP_404_NOT_FOUND])
                    status_code = HTTP_404_NOT_FOUND
                else:
                    profile = self.save_profile(profile)
                    result = TwitterProfileSerializer(profile)
                    result = result.data
                    status_code = HTTP_201_CREATED
        else:
            result = TwitterProfileSerializer(profile)
            result = result.data
        return Response(result, status=status_code)

    def get_object(self, screen_name):
        try:
            profile = TwitterProfile.objects.get(screen_name=screen_name)
        except TwitterProfile.DoesNotExist:
            profile = None
        return profile

    def save_profile(self, data):
        profile = TwitterProfile.objects.create(
            screen_name=data['screen_name'],
            name=data['name'],
            bio_description=data['bio_description'],
            followers=data['followers'],
            avatar_url=data['avatar_url']
            )
        return profile