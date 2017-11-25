import datetime
import re
import time
import vk_api
import Stemmer
from .base_reviews import ParserReviews


class Vk_ParserReviews(ParserReviews):
    # __SERVICE_KEY__ = '41116ebc41116ebc41116ebcf3414ed8f34411141116ebc1b09d63d02220e5586386c94'
    # __SERVICE_KEY__ = 'e475eca0e475eca0e475eca028e449b634ee475e475eca0be635e2f7c43279f77aa1f9c'
    __SERVICE_KEY__ = '5790dcef5790dcef5790dcef4757cf6a0c557905790dcef0d89f79bcb448fccdcd020cb'

    def get_reviews(self, tags, count):
        vk_session = vk_api.VkApi(token=self.__SERVICE_KEY__)
        vk = vk_session.get_api()

        reviews = []
        for tag in tags:
            time.sleep(0.5)
            response = vk.newsfeed.search(
                q='\"{}\"'.format(tag), extended=True, count=count)
            reviews_tag = self._get_reviews_by_tag(response, tag)
            # print('---- {} ----'.format(tag))
            reviews.extend(reviews_tag)

        return reviews

    def _get_reviews_by_tag(self, response, tag):
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
        d = dict.fromkeys(['name', 'post_link', 'text',
                           'photo_link', 'date', 'temp_id', 'social_id'])

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
