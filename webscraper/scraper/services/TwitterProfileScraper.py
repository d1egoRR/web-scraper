# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import requests

from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser

from rest_framework.status import (HTTP_200_OK,
                                   HTTP_504_GATEWAY_TIMEOUT)


class TwitterProfileScraper(object):

    def __init__(self, screen_name=None):
        self.screen_name = screen_name
        self.parser = SafeConfigParser()
        self.parser.read(
            os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
        self.connection_status = None
        self.set_soup()

    def set_soup(self):
        if self.screen_name:
            url = self.parser.get('config', 'base_url') + self.screen_name
            try:
                response = requests.get(url)
            except requests.ConnectionError:
                self.connection_status = HTTP_504_GATEWAY_TIMEOUT
            else:
                self.soup = BeautifulSoup(response.text, 'lxml')
                self.connection_status = HTTP_200_OK
        else:
            self.soup = None

    def get_profile(self):
        if self.soup:
            if self.profile_not_found():
                result = None
            else:
                result = self.scrape()
        else:
            result = None
        return result

    def profile_not_found(self):
        tags = self.get_tags('error')
        return len(tags) > 0

    def scrape(self):
        screen_name = self.screen_name
        name = self.get_name()
        bio_description = self.get_bio_description()
        followers = self.get_followers()
        avatar_url = self.get_avatar_url()
        result = dict(
            screen_name=screen_name,
            name=name,
            bio_description=bio_description,
            followers=followers,
            avatar_url=avatar_url
            )
        return result

    def get_tags(self, section):
        tag, class_ = self.get_elements(section)
        return self.soup.find_all(tag, class_=class_)

    def get_elements(self, section):
        tag = self.parser.get(section, 'tag')
        class_ = self.parser.get(section, 'class')
        return tag, class_

    def get_name(self):
        tags = self.get_tags('fullname')
        if len(tags):
            result = tags[0].string.replace('\n', '').strip()
        else:
            result = None
        return result

    def get_bio_description(self):
        tags = self.get_tags('bio-description')
        if len(tags):
            text = tags[0].get_text().strip().replace('\n', '').split(' ')
            text = [t for t in text if t != '']
            result = ' '.join(text)
        else:
            result = None
        return result

    def get_followers(self):
        result = None
        tags_li = self.get_tags('followers-li')
        tag, class_ = self.get_elements('followers-span')
        for li in tags_li:
            span_tags = li.find_all(tag, class_=class_)
            if len(span_tags):
                result = span_tags[0].string.replace('.', '')
                break
        return result

    def get_avatar_url(self):
        tags = self.get_tags('avatar')
        if len(tags):
            result = tags[0]['src']
        else:
            result = None
        return result