# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from scraper.models import TwitterProfile
from scraper.services.TwitterScraperService import TwitterScraperService


class TwitterScraper(APIView):
    def get(self, request):
        if 'screen_name' not in request.GET:
            result = {'message': 'Falta el screen name'}
            status = HTTP_400_BAD_REQUEST
            return Response(result, status=status)

        screen_name = request.GET.get('screen_name')

        profile = self.get_profile(screen_name)
        return Response(profile)

    def get_profile(self, screen_name):
        profile = self.find_in_db(screen_name)
        if profile:
            result = self.format_data(profile)
        else:
            tss = TwitterScraperService(screen_name)
            profile = tss.scraping_twitter()
            if profile:
                profile.save()
                result = self.format_data(profile)
            else:
                result = {'message': 'No existe el perfil'}

        return result

    def find_in_db(self, screen_name):
        try:
            profile = TwitterProfile.objects.get(
                screen_name=screen_name)
        except TwitterProfile.DoesNotExist:
            profile = None
        return profile

    def format_data(self, profile):
        result = {
            'screen_name': profile.screen_name,
            'name': profile.name,
            'bio_description': profile.bio_description,
            'followers': profile.followers,
            'avatar_url': profile.avatar_url,
        }
        return result