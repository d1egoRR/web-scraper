# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from bs4 import BeautifulSoup

from django.test import TestCase
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.test import APIClient

from scraper.models import TwitterProfile
from scraper.services.TwitterScraperService import TwitterScraperService
from scraper.views import TwitterScraper


class TwitterScraperTest(TestCase):

    fixtures = ['twitter_profiles.json']

    def setUp(self):
        self.twitter_scraper = TwitterScraper()

    def test_api_get_profile(self):
        client = APIClient()
        response = client.get('/api/twitter/1.0/get_profile/')
        result = json.loads(response.content)
        self.assertEqual(HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Falta el screen name', result['message'])

        # esto se encuentra en la DB
        params = {'screen_name': 'prueba'}
        response = client.get('/api/twitter/1.0/get_profile/', params)
        result = json.loads(response.content)
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(560, result['followers'])

    def test_get_profile(self):
        screen_name = 'prueba'
        result = self.twitter_scraper.get_profile(screen_name)
        self.assertEqual('prueba', result['screen_name'])
        self.assertEqual(560, result['followers'])

        screen_name = 'userNoExiste'
        result = self.twitter_scraper.find_in_db(screen_name)
        self.assertIsNone(result)

    def test_format_data(self):
        profile = TwitterProfile.objects.get(screen_name='prueba')
        result = self.twitter_scraper.format_data(profile)
        self.assertIn('screen_name', result)
        self.assertIn('followers', result)

        expected_result = {
            'screen_name': profile.screen_name,
            'name': profile.name,
            'bio_description': profile.bio_description,
            'followers': profile.followers,
            'avatar_url': profile.avatar_url,
        }

        self.assertEqual(expected_result, result)

    def test_find_in_db(self):
        screen_name = 'prueba'
        result = self.twitter_scraper.find_in_db(screen_name)
        self.assertEqual('prueba', result.screen_name)
        self.assertEqual(560, result.followers)

        screen_name = 'userNoExiste'
        result = self.twitter_scraper.find_in_db(screen_name)
        self.assertIsNone(result)


class TwitterScraperServiceTest(TestCase):
    def setUp(self):
        self.service = TwitterScraperService()

    def set_valid_html_soup(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        self.service.soup = soup

    def set_invalid_html_soup(self):
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, 'lxml')
        self.service.soup = soup

    def test_error_profile(self):
        self.set_valid_html_soup()
        result = self.service.error_profile()
        self.assertFalse(result)

        html = self.get_error_html()
        soup = BeautifulSoup(html, 'lxml')
        self.service.soup = soup
        result = self.service.error_profile()
        self.assertTrue(result)

    def test_get_name(self):
        self.set_valid_html_soup()
        result = self.service.get_name()
        self.assertEqual('Juan Perez', result)

        self.set_invalid_html_soup()
        result = self.service.get_name()
        self.assertIsNone(result)

    def test_get_followers(self):
        self.set_valid_html_soup()
        result = self.service.get_followers()
        self.assertEqual('201 k', result)

        self.set_invalid_html_soup()
        result = self.service.get_followers()
        self.assertIsNone(result)

    def test_get_avatar_url(self):
        self.set_valid_html_soup()
        result = self.service.get_avatar_url()
        self.assertEqual('http://mysite', result)

        self.set_invalid_html_soup()
        result = self.service.get_avatar_url()
        self.assertIsNone(result)

    def test_get_bio_description(self):
        self.set_valid_html_soup()
        result = self.service.get_bio_description()
        self.assertEqual('Ejemplo de Bio descripcion', result)

        self.set_invalid_html_soup()
        result = self.service.get_bio_description()
        self.assertIsNone(result)

    def get_html(self):
        html = """
               <html>
                 <head></head>
                 <body>
                   <img class='ProfileAvatar-image ' src='http://mysite'/>
                   <a
                     class='fullname ProfileNameTruncated-link
                     u-textInheritColor js-nav'>
                     Juan Perez
                   </a>
                   <li class='ProfileNav-item ProfileNav-item--followers'>
                     <span class='ProfileNav-value'>201 k</span>
                   </li>
                    <p class='ProfileHeaderCard-bio u-dir' dir='ltr'>
                      Ejemplo de Bio descripcion
                    </p>
                 </body>
               </html>
               """
        return html

    def get_error_html(self):
        html = """
               <html>
                 <head></head>
                 <body>
                   <div class='errorpage-body-content'>Error</div>
                 </body>
               </html>
               """
        return html