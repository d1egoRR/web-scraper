# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
            error='not_found',
            message='Profile does not exists')
        return result

    @classmethod
    def get_format_data(self, data):
        result = []
        for profile in data:
            element = self.get_format_profile(profile)
            result.append(element)
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