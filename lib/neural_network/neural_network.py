# -*- coding: utf-8 -*-

import catboost
import psycopg2 as pg
from generate_vectors import initialize_vectors_array
from generate_vectors import write_vectors_to_file

import Stemmer

# Пути к фалам
DATA_DIR = 'data/'
DIR_WITH_MODELS = DATA_DIR + 'models/'
FILE_WITH_VECTORS =  DATA_DIR + 'vectors.txt'
DICTIONARY_PATH =  DATA_DIR + 'dictionary.txt'
FILE_WITH_RANK_MODEL = DIR_WITH_MODELS + 'rank_model/rank_model'

VALUE_FOR_NEUTRAL_RANK = 0.18718411

def calculating_rating():
    data_from_db = _read_id_and_post_text_from_db()
    reviews_id, reviews_text = _initialize_arrays_with_id_and_text_of_reviews(data_from_db)
    dictionary = open(DICTIONARY_PATH, 'r', encoding = 'utf-8')
    vectors = initialize_vectors_array(reviews_text, eval(dictionary.read()))
    dictionary.close()
    write_vectors_to_file(vectors, FILE_WITH_VECTORS)
    reviews_rank = _initialize_reviews_rank()
    print(reviews_rank)
    #_update_rating(reviews_id, reviews_rank)

def _initialize_reviews_rank(path_to_rank_model, reviews_text):
    model = CatBoost()
    model.load_model(fname = FILE_WITH_RANK_MODEL)
    reviews_rank = []
    result_rank =  model.predict(reviews_text, 'RawFormulaVal')
    rounded_neutral_rank = round(VALUE_FOR_NEUTRAL_RANK, 6)
    for rank in result_rank:
        round_rank = round(rank, 6)
        if rounded_rank > rounded_neutral_rank:
            reviews_rank.append(1)
        elif rounded_rank < rounded_neutral_rank:
            reviews_rank.append(-1)
        else:
            reviews_rank.append(0)
    return reviews_rank


def _initialize_arrays_with_id_and_text_of_reviews(data_from_db):
    reviews_text = []
    reviews_id = []
    for review_id, review_text in data_from_db:
        reviews_id.append(review_id)
        reviews_text.append(review_text)
    return reviews_id, reviews_text

def _read_id_and_post_text_from_db():
    conn = pg.connect(database="brand_focus", user="test_user", password="postgres", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT reviews.reviews_id, reviews.reviews_text FROM reviews")
    results = cursor.fetchall()
    conn.close()
    return results # [(1, 'sometext'), (2, 'anothertext'), .......]

def _update_rating(reviews_id, reviews_rank):
    conn = pg.connect(database="brand_focus", user="test_user", password="postgres", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    for i in range(1, len(reviews_id)):
        cursor.execute("UPDATE reviews SET reviews_rank = ? WHERE reviews_id = ?",
                      (reviews_id[i], reviews_rank[i]))
    conn.commit()
    conn.close()


def calculating_rating():
    data_from_db = _read_id_and_post_text_from_db()
    reviews_text = []
    reviews_id = []
    for review_id, review_text in data_from_db:
        reviews_id.append(review_id)
        reviews_text.append(review_text)
    dictionary = open(DICTIONARY_PATH, 'r', encoding = 'utf-8')
    vectors = initialize_vectors_array(reviews_text, eval(dictionary.read()))
    write_vectors_to_file(vectors, FILE_WITH_VECTORS)
    dictionary.close()
    #_update_rating()


print(_read_id_and_post_text_from_db())
calculating_rating()

"""
posts = [
			['ага', 'так'],
			['не', 'потому'],
			['кукуку', 'вавава', 'лолололо']
	    ]

dictionary = open(DICTIONARY_PATH, 'r', encoding = 'utf-8')
vectors = initialize_vectors_array(posts, eval(dictionary.read()))
dictionary.close()
print(vectors)
write_vectors_to_file(vectors, FILE_WITH_VECTORS)

"""