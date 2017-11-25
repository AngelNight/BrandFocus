# -*- coding: utf-8 -*- python 3.6.3

import re
import os
import Stemmer

# General path
ABS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
DATA_DIR = ABS_PATH + 'data/'
DIR_WITH_MODELS = DATA_DIR + 'models/'

# Rank model
RANK_MODEL = DIR_WITH_MODELS + 'rank_model/rank_model'
DICTIONARY_RANK_MODEL = DIR_WITH_MODELS + 'rank_model/wdict.txt'

# Ad model
AD_MODEL = DIR_WITH_MODELS + 'ad_model/ad_model'
DICTIONARY_AD_MODEL  = DIR_WITH_MODELS + 'ad_model/ad_dict.txt'

# Ad model
SPAM_MODEL = DIR_WITH_MODELS + 'spam_model/spam_model'
DICTIONARY_SPAM_MODEL  = DIR_WITH_MODELS + 'spam_model/spam_dict.txt'

MIN_WORD_LEN = 2

stemmer = Stemmer.Stemmer('russian')

post_data_file = open(DICTIONARY_RANK_MODEL, 'r', encoding = 'utf-8')
post = eval(post_data_file.read())
post_data_file.close()

ad_data_file = open(DICTIONARY_AD_MODEL, 'r', encoding = 'utf-8')
ad = eval(ad_data_file.read())
ad_data_file.close()

spam_data_file = open(DICTIONARY_SPAM_MODEL, 'r', encoding = 'utf-8')
spam = eval(spam_data_file.read())
spam_data_file.close()

# init words dict (take from words.txt)
dicts = [post,spam,ad] # 0 - for posts, 1 - for spam, 2 - for ad
post_dict_len = [len(post), len(spam), len(ad)]

def getIndex (type):
	d = {
		'post': 0,
		'spam': 1,
		'ad': 2,
	}
	return d[type]
	
def preprocessPost (post, type='post'):
	'''
	Replace links, preprocess hashtags/smiles, to lowercase, etc.
	'''
	if type == 'spam' or type == 'ad':
		LINK_REPLACE = '[link]'       #'[link]'
		USENAME_REPLACE = ''          #'[username]'
		HASHTAG_REPLACE = '[hashtag]' #'[hashtag]'
		DIGITS_REPLACE = '[digit]'    #'[digit]'
	else:
		LINK_REPLACE = ''      #'[link]'
		USENAME_REPLACE = ''   #'[username]'
		HASHTAG_REPLACE = ''   #'[hashtag]'
		DIGITS_REPLACE = ''    #'[digit]'
	
	# to lower
	post = post.lower()
	
	# replace linesbreaks, tabs, etc.
	post = post.replace('\n', ' ').replace('\r', '')
	post = post.replace('\t', ' ')
	post = ' '.join(post.split())
	
	# replace url to '[link]' string
	post = re.sub(r'http[s]?:\/\/(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', LINK_REPLACE, post)
	
	# replace usernames
	post = re.sub(r'@([\wа-я0-9_\-]+)', USENAME_REPLACE, post)
	
	# replace hashtags
	post = re.sub(r'#([\wа-я0-9_\-]+)', HASHTAG_REPLACE, post)
	
	if type == 'spam' or type == 'ad':
		# replace digits
		post = re.sub(r'([0-9_\-\.]{2,})', DIGITS_REPLACE, post)
		
	# process smiles
	
	
	# remove digits, non word symbols
	arr = []
	reg = '([а-я]+)'
	for a in [LINK_REPLACE, USENAME_REPLACE, HASHTAG_REPLACE, DIGITS_REPLACE]:
		if len(a):
			reg += '|(' + a.replace('[', '\[').replace(']', '\]') + ')'
	for m in re.finditer(reg, post):
		# append only if "long" word
		if len(m.group(0)) > MIN_WORD_LEN - 1:
			arr.append(m.group(0))
	
	# stemm all words
	arr = stemmer.stemWords(arr)
	
	return ' '.join(arr)
	
def getPostVector (post, type='post'):
	index = getIndex(type)
	post = preprocessPost(post, type)
	
	postarr = ['0'] * post_dict_len[index]
	t = post.split()
	for i in t:
		if i in dicts[index]:
			postarr[dicts[index][i]] = '1'
	return postarr