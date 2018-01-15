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

    def error_profile(self):
        class_error = self.parser.get('class', 'error')
        div_tags = self.soup.find_all('div', class_=class_error)
        return len(div_tags) > 0

    def get_name(self):
        try:
            class_fullname = self.parser.get('class', 'fullname')
            a_tags = self.soup.find_all('a', class_=class_fullname)
            result = a_tags[0].string.replace('\n', '').strip()
        except:
            result = None

        return result

    def get_bio_description(self):
        try:
            class_bio = self.parser.get('class', 'bio_description')
            p_tags = self.soup.find_all('p', class_=class_bio)
            text = p_tags[0].get_text().strip().replace('\n', '').split(' ')
            text = [t for t in text if t != '']
            result = ' '.join(text)
        except:
            result = None

        return result

    def get_followers(self):
        result = None
        try:
            class_li_followers = self.parser.get('class', 'li_followers')
            class_span_followers = self.parser.get('class', 'span_followers')
            li_tags = self.soup.find_all('li', class_=class_li_followers)
            for li in li_tags:
                span_tags = li.find_all('span', class_=class_span_followers)
                if len(span_tags):
                    result = span_tags[0].string.replace('.', '')
                    break
        except:
            result = None

        return result

    def get_avatar_url(self):
        try:
            class_avatar = self.parser.get('class', 'img_avatar')
            img_tags = self.soup.find_all('img', class_=class_avatar)
            result = img_tags[0]['src']
        except:
            result = None

        return result