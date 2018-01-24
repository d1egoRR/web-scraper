# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from scraper2.utils import DataFormatter, Profile
#from scraper.services.TwitterScraperService import TwitterScraperService


class TwitterProfileList(APIView):

    def get(self, request):
        profile_list = Profile.get_list()
        result = DataFormatter.get_format_data(profile_list)
        return Response(result)


class TwitterProfileDetail(APIView):

    def get(self, request, screen_name):
        profile = Profile.get_by_screen_name(screen_name)
        if profile is None:
            result = DataFormatter.get_data_404_not_found()
        else:
            format_result = DataFormatter.get_format_profile(profile)
            result = dict(data=format_result, status_code=HTTP_200_OK)
        return Response(result, status=result['status_code'])