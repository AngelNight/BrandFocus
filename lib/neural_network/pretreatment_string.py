# -*- coding: utf-8 -*-

import os
import re
import numpy as np
import Stemmer

def pretreatmenting_string(input_data):
	stemmer_rus = Stemmer.Stemmer('russian')
	word_list = stemmer_rus.stemWords(re.sub(r'[^а-я\s]+|[\d]+', '', input_data.lower().
				replace('-', '')).strip().split())
	return remove_small_word_in_string(word_list)


def remove_small_word_in_string(words):
	words_for_remove = []
	for i in range(0, len(words)):
		if len(words[i]) < 2:
			words_for_remove.append(words[i])
	for word in words_for_remove:
		words.remove(word)
	return words
	