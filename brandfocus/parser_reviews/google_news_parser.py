import requests
import json
from .base_reviews import ParserReviews


class GoogleNews_ParserReviews(ParserReviews):
    __API_KEY__ = '732cfb86dd784386960528b3da76bbd8'
    __URL__ = 'https://newsapi.org/v2/everything?source=google-news&q={}&language=ru&apiKey={}'

    def get_reviews(self, tags, count):
        single_tags_query = '+OR+'.join(tag for tag in tags if tag.isalnum())
        multi_tags = [tag for tag in tags if not tag.isalnum()]

        multi_tags_res = []
        for tag in multi_tags:
            q = '+AND+'.join(tag.split())
            multi_tags_res.append('({})'.format(q))
        multi_tags_query = '+OR+'.join(multi_tags_res)

        if multi_tags_query:
            query = '{}+OR+{}'.format(single_tags_query, multi_tags_query)
        else:
            query = single_tags_query

        response = requests.get(self.__URL__.format(query, self.__API_KEY__))

        result = json.loads(response.content.decode('utf-8'))

        if result == None:
            return []

        try:
            articles = result['articles']
        except:
            return []

        reviews = []
        for article in articles:
            reviews.append(self._get_article_info(article))

        return reviews

    def _get_article_info(self, article):
        d = {}

        d['social_id'] = 2
        d['name'] = article['source'].get('name')
        d['post_link'] = article['url']
        d['text'] = '\n'.join([article['title'], article['description']])
        d['photo_link'] = article['urlToImage']
        d['date'] = self._get_date(article['publishedAt'])
        name = article['author'] if article['author'] else d['name']
        d['temp_id'] = '_'.join([name, article['title']])

        return d

    def _get_date(self, date):
        date = date[:10].split('-')
        return '-'.join(date)
