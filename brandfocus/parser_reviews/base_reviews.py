from abc import abstractmethod


class ParserReviews:
    @abstractmethod
    def get_reviews(self, tags, count, use_geo=False):
        """ Получить список отзывов """
