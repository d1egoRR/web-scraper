# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class DataFormatter(object):

    @staticmethod
    def get_data_404_not_found():
        result = {
            'error': {
                'type': 'not_found',
                'message': 'Profile does not exists'
            }
        }
        return result

    @classmethod
    def get_format_data(self, data):
        profiles = []
        for profile in data:
            element = self.get_format_profile(profile)
            profiles.append(element)
        result = dict(data=profiles)
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