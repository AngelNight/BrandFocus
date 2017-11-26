# -*- coding: utf-8 -*-

from catboost import CatBoost
from lib.neural_network.post_preprocessing import getPostVector
import os
import psycopg2 as pg
import random
from brandfocus.models import Firm, Social, Review, Rank, Tag

# General path
ABS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
DATA_DIR = ABS_PATH + 'data/'
DIR_WITH_MODELS = DATA_DIR + 'models/'
FILE_WITH_VECTORS = DATA_DIR + 'vectors.txt'

# Rank model
RANK_MODEL = DIR_WITH_MODELS + 'rank_model/rank_model'
DICTIONARY_RANK_MODEL = DIR_WITH_MODELS + 'rank_model/wdict.txt'

# Ad model
AD_MODEL = DIR_WITH_MODELS + 'ad_model/ad_model'
DICTIONARY_AD_MODEL = DIR_WITH_MODELS + 'ad_model/ad_dict.txt'

# Ad model
SPAM_MODEL = DIR_WITH_MODELS + 'spam_model/spam_model'
DICTIONARY_SPAM_MODEL = DIR_WITH_MODELS + 'spam_model/spam_dict.txt'

# Values for the ranks
VALUE_FOR_POST = 0.18718411
VALUE_FOR_SPAM = 0.09083112
VALUE_FOR_AD = 0.06383575

post_model = CatBoost()
post_model.load_model(fname=RANK_MODEL)

ad_model = CatBoost()
ad_model.load_model(fname=AD_MODEL)

spam_model = CatBoost()
spam_model.load_model(fname=SPAM_MODEL)

def calculating_rating():
    data_from_db = _read_id_and_post_text_from_db()
    reviews_id, reviews_text = _initialize_arrays_with_id_and_text_of_reviews(data_from_db)
    reviews_rank = []
    for post in reviews_text:
        ad_vector = getPostVector(post, 'ad')
        spam_vector = getPostVector(post, 'spam')
        post_vector = getPostVector(post, 'post')
        # result_post = random.uniform(-1, 1)
        # result_ad = random.uniform(-1, 1)
        # result_spam = random.uniform(-1, 1)
        result_post = post_model.predict([post_vector], 'RawFormulaVal')
        result_ad = ad_model.predict([ad_vector], 'RawFormulaVal')
        result_spam = spam_model.predict([spam_vector], 'RawFormulaVal')
        reviews_rank.append(_initialize_rank(result_post, result_ad, result_spam))
    _update_rating(reviews_id, reviews_rank)

def _initialize_rank(post, ad, spam):
    if round(spam[0], 6) > round(VALUE_FOR_SPAM, 6) and round(ad[0], 6) > round(VALUE_FOR_AD, 6):
        return -100
    elif round(post[0], 6) > round(VALUE_FOR_POST, 6):
        return 1
    elif round(post[0], 6) < round(VALUE_FOR_POST, 6):
        return -1
    else:
        return 0

def _initialize_arrays_with_id_and_text_of_reviews(data_from_db):
    reviews_text = []
    reviews_id = []
    for review in data_from_db:
        reviews_id.append(review[0])
        reviews_text.append(review[1])
    return reviews_id, reviews_text

def _read_id_and_post_text_from_db():
    conn = pg.connect(database="postgres", user="postgres", password="qwerty", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM review WHERE rank=2")
    results = cursor.fetchall()
    conn.close()
    return results

def _update_rating(reviews_id, reviews_rank):
    conn = pg.connect(database="postgres", user="postgres", password="qwerty", host="127.0.0.1", port="5432")
    cursor = conn.cursor()
    for i in range(0, len(reviews_id)):
        cursor.execute("""UPDATE review SET rank = %s WHERE id = %s""",
                       (reviews_rank[i], reviews_id[i]))
    conn.commit()
    conn.close()
