# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from transformer.Transformer import Transformer


class ProfileTransformer(Transformer):

    def __init__(self):
        keys = [
            'screen_name', 'name', 'bio_description',
            'followers', 'avatar_url'
        ]
        self._object = 'Twitter Profile'
        super(ProfileTransformer, self).__init__(keys)

    def get_data_404(self):
        result = {
            'error': {
                'type': settings.NOT_FOUND_ERROR,
                'message': settings.NOT_FOUND_MESSAGE.format(self._object)
            }
        }
        return result