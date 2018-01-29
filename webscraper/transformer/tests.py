# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from transformer.Transformer import Transformer


class TransformerTest(TestCase):

    def setUp(self):
        self.transformer = Transformer()
        self.key = ['attr1', 'attr2', 'attr3']

    def test_transform_data(self):
        objects = self.get_objects()
        result = self.transformer.transform_data(
            objects[2], self.key)
        self.assertEqual('CC', result['attr1'])
        self.assertEqual(5.88, result['attr2'])
        self.assertFalse(result['attr3'])

    def test_get_transformed_data(self):
        objects = self.get_objects()
        result = self.transformer.get_transformed_data(
            objects, self.key)
        self.assertIn('data', result)
        self.assertEqual(3, len(result['data']))
        self.assertEqual('B', result['data'][1]['attr1'])
        self.assertFalse(result['data'][2]['attr3'])

        sample1 = objects[0]
        result = self.transformer.get_transformed_data(
            sample1, self.key)
        self.assertIn('data', result)
        self.assertEqual('a', result['data']['attr1'])
        self.assertEqual('b', result['data']['attr2'])
        self.assertEqual(5, result['data']['attr3'])

    def get_objects(self):
        sample1 = SampleTestClass('a', 'b', 5)
        sample2 = SampleTestClass('B', True, '12')
        sample3 = SampleTestClass('CC', 5.88, False)
        return (sample1, sample2, sample3)


class SampleTestClass(object):

    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3