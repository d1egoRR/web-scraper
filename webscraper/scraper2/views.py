# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from scraper.models import TwitterProfile
from scraper.services.TwitterScraperService import TwitterScraperService


class TwitterProfileList(APIView):

    def get(self, request):
        profile_list = self.get_profiles()
        result = self.format_data(profile_list)
        result['status_code'] = HTTP_200_OK
        return Response(result)

    def get_profiles(self):
        profile_list = TwitterProfile.objects.all()
        return profile_list

    def format_data(self, profile_list):
        data = []
        for profile in profile_list:
            element = dict(
                screen_name=profile.screen_name,
                name=profile.name,
                bio_description=profile.bio_description,
                followers=profile.followers,
                avatar_url=profile.avatar_url
            )
            data.append(element)
        result = dict(data=data)
        return result


class TwitterProfileDetail(APIView):

    def get(self, request, screen_name):
        print screen_name
        profile = self.get_profile(screen_name)
        result = self.format_data(profile)
        result['status_code'] = HTTP_200_OK
        return Response(result)

    def get_profile(self, screen_name):
        try:
            profile = TwitterProfile.objects.get(
                screen_name=screen_name)
        except TwitterProfile.DoesNotExist:
            raise Http404
        return profile

    def format_data(self, profile):
        element = dict(
            screen_name=profile.screen_name,
            name=profile.name,
            bio_description=profile.bio_description,
            followers=profile.followers,
            avatar_url=profile.avatar_url
        )
        result = dict(data=[element])
        return result