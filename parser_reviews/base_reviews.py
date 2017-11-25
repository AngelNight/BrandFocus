from abc import abstractmethod


class ParserReviews:
    @abstractmethod
    def get_reviews(self, tags, count):
        """ Получить список отзывов """
