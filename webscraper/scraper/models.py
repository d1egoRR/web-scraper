# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class TwitterProfile(models.Model):
    screen_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    bio_description = models.CharField(max_length=300, null=True, blank=True)
    followers = models.CharField(max_length=10, null=True, blank=True)
    avatar_url = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Twitter Profile"
