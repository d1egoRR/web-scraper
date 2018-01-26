# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import requests

from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser
from scraper.models import TwitterProfile


class TwitterProfileScraper(object):

    def __init__(self, screen_name=None):
        self.screen_name = screen_name
        self.parser = SafeConfigParser()
        self.parser.read(
            os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
        self.set_soup()

    def set_soup(self):
        if self.screen_name:
            url = self.parser.get('config', 'base_url') + self.screen_name
            response = requests.get(url)
            self.soup = BeautifulSoup(response.text, 'lxml')
        else:
            self.soup = None

    def get_profile(self):
        if self.soup:
            if self.profile_not_found():
                result = None
            else:
                result = self.scrape()
                result.save()
        else:
            result = None
        return result

    def profile_not_found(self):
        tags = self.get_tags('error')
        return len(tags) > 0

    def scrape(self):
        result = TwitterProfile()
        result.screen_name = self.screen_name
        result.name = self.get_name()
        result.bio_description = self.get_bio_description()
        result.followers = self.get_followers()
        result.avatar_url = self.get_avatar_url()
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