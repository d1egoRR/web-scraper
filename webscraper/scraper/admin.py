# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from scraper.models import TwitterProfile


class TwitterProfileAdmin(admin.ModelAdmin):
    list_display = [
        'screen_name', 'name', 'bio_description',
        'followers', 'avatar_url']
    list_filter = ['screen_name']


admin.site.register(TwitterProfile, TwitterProfileAdmin)