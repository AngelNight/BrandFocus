import datetime
import http
import re
import requests
import time
import Stemmer
from .base_reviews import ParserReviews


class Vk_ParserReviews(ParserReviews):
    # __SERVICE_KEY__ = '41116ebc41116ebc41116ebcf3414ed8f34411141116ebc1b09d63d02220e5586386c94'
    # __SERVICE_KEY__ = 'e475eca0e475eca0e475eca028e449b634ee475e475eca0be635e2f7c43279f77aa1f9c'
    __SERVICE_KEY__ = '5790dcef5790dcef5790dcef4757cf6a0c557905790dcef0d89f79bcb448fccdcd020cb'
    _VK_VERSION_  = '5.67'
    RPS_DELAY = 0.2

    def __init__(self):
        self.http = requests.Session()
        self.http.headers.update({
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                          'Gecko/20100101 Firefox/52.0'
        })

        self.last_request = 0.0

    def get_reviews(self, tags, count, use_geo=False):
        self.use_geo = use_geo

        reviews = []
        for tag in tags:         
            response = self._vk_newsfeed_search(
                q='\"{}\"'.format(tag), extended=True, count=count)
            reviews_tag = self._get_reviews_by_tag(response, tag)
            reviews.extend(reviews_tag)

        return reviews

    def _vk_newsfeed_search(self, **values):
        values['access_token'] = self.__SERVICE_KEY__
        values['v'] = self._VK_VERSION_

        if self.use_geo:
            values['latitude'] = 57.6309858
            values['longitude'] = 39.8408914

        delay = self.RPS_DELAY - (time.time() - self.last_request)

        if delay > 0:
            time.sleep(delay)

        response = self.http.post(
                'https://api.vk.com/method/newsfeed.search',
                values
            )

        self.last_request = time.time()

        if response.ok:
            response = response.json()
            return response['response']
        else:
            return None
        
    def _get_reviews_by_tag(self, response, tag):
        if response is None:
            return None

        stemmer = Stemmer.Stemmer('russian')
        tags = stemmer.stemWords(tag.split())

        reviews = []
        for post in response['items']:
            if post['post_type'] != 'post':
                continue

            if post['from_id'] > 0:
                profile = self._get_profile_by_id(
                    response['profiles'], post['from_id'])
            else:
                profile = self._get_profile_by_id(
                    response['groups'], abs(post['from_id']))

            post_info = self._get_post_info(post, profile)

            if(re.match(r'^[^а-яА-Я]*$', post_info['text'])):
                continue

            post_text = post_info['text'].lower()
            for word in tags:
                if word not in post_text:
                    break
            else:
                reviews.append(post_info)

        return reviews

    def _get_post_info(self, post, profile):
        d = {}

        d['social_id'] = 0

        d['text'] = post['text']
        d['date'] = self._datetime_from_unixtime(post['date'])

        if post['from_id'] > 0:
            first_name = profile['first_name']
            last_name = profile['last_name']
            d['name'] = " ".join([first_name, last_name])
        else:
            d['name'] = profile['name']

        d['photo_link'] = profile['photo_100']
        d['post_link'] = self._get_post_link(
            screen_name=profile['screen_name'], user_id=post['owner_id'], post_id=post['id'])
        d['photo_post_link'] = self._get_photo_link_post(post.get('attachments'))

        d['temp_id'] = '{}_{}'.format(post['owner_id'], post['id'])

        return d

    def _datetime_from_unixtime(self, value):
        return datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d')

    def _get_post_link(self, user_id, screen_name, post_id):
        return "https://vk.com/{}?w=wall{}_{}".format(screen_name, user_id, post_id)

    def _get_profile_by_id(self, profiles, user_id):
        for profile in profiles:
            if profile['id'] == user_id:
                return profile
    
    def _get_photo_link_post(self, attachments):
        if attachments is None:
            return ''
        
        for attach in attachments:
            if attach['type'] == 'photo':
                return attach['photo'].get('photo_604', '')
        else:
            return ''
