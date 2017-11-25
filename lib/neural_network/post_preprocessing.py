# -*- coding: utf-8 -*- python 3.6.3

import re
import Stemmer
from dictionary import read_dictionary

LINK_REPLACE = ''      #'[link]'
USENAME_REPLACE = ''   #'[username]'
HASHTAG_REPLACE = ''   #'[hashtag]'
MIN_WORD_LEN = 2

PATH_TO_DICT_OF_RANK_MODEL = 'data/models/rank_model/wdict.txt'

stemmer = Stemmer.Stemmer('russian')

wdict = read_dictionary(PATH_TO_DICT_OF_RANK_MODEL)
wdictLen = len(wdict)

def preprocessPost (post):
	'''
	Replace links, preprocess hashtags/smiles, to lowercase, etc.
	'''
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
	
	# process smiles
	
	
	# remove digits, non word symbols
	arr = []
	reg = '([а-я]+)'
	for a in [LINK_REPLACE, USENAME_REPLACE, HASHTAG_REPLACE]:
		if len(a):
			reg += '|(' + a.replace('[', '\[').replace(']', '\]') + ')'
	for m in re.finditer(reg, post):
		# append only if "long" word
		if len(m.group(0)) > MIN_WORD_LEN - 1:
			arr.append(m.group(0))
	
	# stemm all words
	arr = stemmer.stemWords(arr)
	
	return ' '.join(arr)
	
def getPostVector (post):
	post = preprocessPost(post)
	
	postarr = ['0'] * wdictLen
	t = post.split()
	for i in t:
		if i in wdict:
			postarr[wdict[i]] = '1'
	return postarr
