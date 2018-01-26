# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from scraper.services.TwitterProfileScraper import TwitterProfileScraper
from scraper.utils import DataFormatter, Profile


class TwitterProfileList(APIView):
    def get(self, request):
        profile_list = Profile.get_list()
        result = DataFormatter.get_format_data(profile_list)
        return Response(result)


class TwitterProfileDetail(APIView):
    def get(self, request, screen_name):
        profile = Profile.get_by_screen_name(screen_name)
        status_code = None
        if profile is None:
            scraper = TwitterProfileScraper(screen_name)
            profile = scraper.get_profile()
            if profile is None:
                result = DataFormatter.get_data_404_not_found()
                status_code = HTTP_404_NOT_FOUND
            else:
                result = DataFormatter.get_format_profile(profile)
        else:
            result = DataFormatter.get_format_profile(profile)
        return Response(result, status=status_code)