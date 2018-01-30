# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Transformer(object):

    def __init__(self, keys):
        self.keys = keys

    def get_transformed_data(self, data):
        if type(data) == tuple:
            transformed_data = []
            for _object in data:
                transformed = self.transform_data(_object)
                transformed_data.append(transformed)
        else:
            transformed_data = self.transform_data(data)
        result = dict(data=transformed_data)
        return result

    def transform_data(self, _object):
        result = {}
        for _key in self.keys:
            result[_key] = getattr(_object, _key, '')
        return result