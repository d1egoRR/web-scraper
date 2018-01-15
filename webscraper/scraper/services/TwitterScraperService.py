# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import requests

from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser
from scraper.models import TwitterProfile


class TwitterScraperService(object):

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

    def scraping_twitter(self):
        if self.soup:
            if self.error_profile():
                result = None
            else:
                result = TwitterProfile(screen_name=self.screen_name)
                result.name = self.get_name()
                result.bio_description = self.get_bio_description()
                result.followers = self.get_followers()
                result.avatar_url = self.get_avatar_url()
        else:
            result = None

        return result

    def get_tags(self, section):
        element = self.parser.get(section, 'element')
        class_ = self.parser.get(section, 'class')
        return self.soup.find_all(element, class_=class_)

    def error_profile(self):
        tags = self.get_tags('error')
        return len(tags) > 0

    def get_name(self):
        try:
            tags = self.get_tags('fullname')
            result = tags[0].string.replace('\n', '').strip()
        except:
            result = None

        return result

    def get_bio_description(self):
        try:
            tags = self.get_tags('bio_description')
            text = tags[0].get_text().strip().replace('\n', '').split(' ')
            text = [t for t in text if t != '']
            result = ' '.join(text)
        except:
            result = None

        return result

    def get_followers(self):
        result = None
        try:
            element1 = self.parser.get('followers', 'element1')
            class1 = self.parser.get('followers', 'class1')
            element2 = self.parser.get('followers', 'element2')
            class2 = self.parser.get('followers', 'class2')
            li_tags = self.soup.find_all(element1, class_=class1)
            for li in li_tags:
                span_tags = li.find_all(element2, class_=class2)
                if len(span_tags):
                    result = span_tags[0].string.replace('.', '')
                    break
        except:
            result = None

        return result

    def get_avatar_url(self):
        try:
            tags = self.get_tags('avatar')
            result = tags[0]['src']
        except:
            result = None

        return result