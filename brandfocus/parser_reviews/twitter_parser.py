import time
import twitter
from .base_reviews import ParserReviews


class Twitter_ParserReviews(ParserReviews):
    __CONSUMER_KEY__ = 'VUk8dXukBXCxlLU15FjTSGJFW'
    __CONSUMER_SECRET__ = 'crUwUC4WWCbUDkr0ZnWmBDPSW2lgmVdfduY8D9pztschzC8XDv'
    __ACCESS_TOKEN_KEY__ = '934117279188639746-3weCkBvUmwXIXrru5VCy29SCEVsWQhs'
    __ACCESS_TOKEN_SECRET__ = 'YcwxWkxtgY0uXeS8jVxl2DpSPOb3jKBeSBdMBi7lg1AbS'

    __QUERY_TEMPLATE__ = "q={}&count={}&result_type=recent&lang=ru&tweet_mode=extended"

    def get_reviews(self, tags, count, use_geo=False):
        api = twitter.Api(
            consumer_key=self.__CONSUMER_KEY__,
            consumer_secret=self.__CONSUMER_SECRET__,
            access_token_key=self.__ACCESS_TOKEN_KEY__,
            access_token_secret=self.__ACCESS_TOKEN_SECRET__)

        single_tags = '+OR+'.join(tag for tag in tags if tag.isalnum())
        multi_tags = [tag for tag in tags if not tag.isalnum()]

        reviews = []

        if single_tags:
            query = self.__QUERY_TEMPLATE__.format(single_tags, count)
            reviews.extend(self._get_tweets(query, api))

        for tag in multi_tags:
            time.sleep(0.3)
            query = self.__QUERY_TEMPLATE__.format(tag, count)
            reviews.extend(self._get_tweets(query, api))

        return reviews

    def _get_tweets(self, query, api):
        reviews = []

        response = api.GetSearch(raw_query=query)
        for tweet in response:
            reviews.append(self._get_tweet_info(tweet))

        return reviews

    def _get_tweet_info(self, tweet):
        d = {}

        d['social_id'] = 1
        d['name'] = tweet.user.name
        d['post_link'] = self._get_post_link(tweet.user.screen_name, tweet.id)
        d['text'] = tweet.full_text
        d['photo_link'] = tweet.user.profile_image_url
        d['date'] = self._get_date(tweet.created_at)
        d['temp_id'] = tweet.id_str

        return d

    def _get_post_link(self, screen_name, post_id):
        return 'https://twitter.com/{}/status/{}'.format(screen_name, post_id)

    def _get_date(self, twitter_date):
        return time.strftime('%Y-%m-%d', time.strptime(twitter_date, '%a %b %d %H:%M:%S +0000 %Y'))
