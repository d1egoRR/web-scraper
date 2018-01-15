# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from scraper.models import TwitterProfile


class TwitterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterProfile
        fields = (
            'id', 'screen_name', 'bio_description', 'followers', 'avatar_url')