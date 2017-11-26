from .google_news_parser import GoogleNews_ParserReviews
from .twitter_parser import Twitter_ParserReviews
# from .unique_reviews import unique_reviews
from .vk_parser import Vk_ParserReviews


def get_reviews(tags, count=100, use_geo=False):
    """Return reviews from social networks

    tags - tags for search

    count - number of posts from one social network
    """
    vk = Vk_ParserReviews()
    twitter = Twitter_ParserReviews()
    google_news = GoogleNews_ParserReviews()

    reviews = []
    reviews.extend(vk.get_reviews(tags, count, use_geo))
    reviews.extend(twitter.get_reviews(tags, count))
    reviews.extend(google_news.get_reviews(tags, count))

    return reviews
