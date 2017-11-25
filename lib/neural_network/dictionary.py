# -*- coding: utf-8 -*-

import os
import re
import operator
from pretreatment_string import pretreatmenting_string
import numpy as np
import Stemmer
from pandas import read_csv

BAD_RANK_FOR_WORD = 5
MAX_WORDS_IN_DICT = 50000

# Функция для загрузки данных из файла
def load_data(path_to_file):
	return read_csv(path_to_file, encoding = 'utf-8', sep = ';', usecols = [3], header = None)

# Функция для форматирования строки для словаря
def format_string(string):
	# Вырезать предлоги
	return re.sub(r'[^а-я\s]+|[\d]+', '', string.lower()).strip()

# Создает/записывает в конец файла словарь
def write_dictionary(data_set, path_to_file, start_index, end_index):
	stemmer_rus = Stemmer.Stemmer('russian')
	word_list = pretreatmenting_string(data_set[start_index : end_index].to_string(index = False))
	word_list_hash = format_word_list(generate_word_list_hash(word_list))
	with open(path_to_file, 'w', encoding = 'utf-8') as file:
		file.write(str(indexing_word_list(word_list_hash)))
		file.close()

# Генерирует словарь, где ключ - это СЛОВО
# { "word" : 201123 }
def generate_word_list_hash(word_list):
	word_list_hash = {}
	for i in range(0, len(word_list)):
		if not word_list[i] in word_list_hash:
			word_list_hash[word_list[i]] = 1
		else:
			word_list_hash[word_list[i]] += 1

	word_list_hash = remove_small_word_in_string(word_list_hash)
	sorted_list = sorted(word_list_hash.items(), key=operator.itemgetter(1))
	sorted_list.reverse()
	return dict((key, value) for key, value in sorted_list)

def format_word_list(word_list):
	key_for_remove = []
	for word in word_list:
		if len(word_list) > MAX_WORDS_IN_DICT:
			break
		else:
			if word_list[word] < BAD_RANK_FOR_WORD:
				key_for_remove.append(word)
	for key in key_for_remove:
		word_list.pop(str(key), None)
	return word_list

def indexing_word_list(word_list):
	indexed_word_list = {}
	index = 0
	for word in word_list:
		indexed_word_list[word] = index
		index += 1
	return indexed_word_list

# Remove the small words in a string
def remove_small_word_in_string(word_list):
	key_for_remove = []
	for word in word_list:
		if len(word) < 2:
			key_for_remove.append(word)
	for key in key_for_remove:
		word_list.pop(str(key), None)
	return word_list


# Read the dictionary file
def read_dictionary(path_to_file):
	dictionary_file = open(path_to_file, 'r', encoding = 'utf-8')
	word_list = eval(dictionary_file.read())
	dictionary_file.close()
	return word_list

# Delete a last char in the file
def remove_last_char_in_file(path_to_file):
	with open(path_to_file, 'rb+') as file:
			file.seek(-1, os.SEEK_END)
			file.truncate()
			file.close()
