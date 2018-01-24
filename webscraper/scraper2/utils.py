# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from scraper.models import TwitterProfile


class Profile(object):

    @staticmethod
    def get_by_screen_name(screen_name):
        try:
            result = TwitterProfile.objects.get(screen_name=screen_name)
        except TwitterProfile.DoesNotExist:
            result = None
        return result

    @staticmethod
    def get_list():
        result = list(TwitterProfile.objects.all())
        return result


class DataFormatter(object):

    @staticmethod
    def get_data_404_not_found():
        result = dict(
            status_code=HTTP_404_NOT_FOUND,
            message='Profile not found')
        return result

    @classmethod
    def get_format_data(self, data):
        format_result = []
        for profile in data:
            element = self.get_format_profile(profile)
            format_result.append(element)

        result = dict(data=format_result, status_code=HTTP_200_OK)
        return result

    @staticmethod
    def get_format_profile(profile):
        result = dict(
            screen_name=profile.screen_name,
            name=profile.name,
            bio_description=profile.bio_description,
            followers=profile.followers,
            avatar_url=profile.avatar_url
        )
        return result