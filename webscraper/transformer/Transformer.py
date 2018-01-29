# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Transformer(object):

    def get_transformed_data(self, data, key_list):
        if type(data) == tuple:
            result = {'data': []}
            for _object in data:
                transformed = self.transform_data(_object, key_list)
                result['data'].append(transformed)
        else:
            transformed = self.transform_data(data, key_list)
            result = dict(data=transformed)
        return result

    def transform_data(self, _object, key_list):
        result = {}
        for _key in key_list:
            result[_key] = getattr(_object, _key, '')
        return result