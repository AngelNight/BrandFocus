# -*- coding: utf-8 -*-

from pretreatment_string import pretreatmenting_string

def generate_array_of_post_words(posts):
	result_array = []
	for post in posts:
		words_in_post = pretreatmenting_string(post.text)
		result_array.append(words_in_post)
	return result_array

def initialize_vector(words_in_post, dictionary):
	vector = [0] * len(dictionary)
	for word in words_in_post:
		if word in dictionary:
			vector[dictionary[word]] = 1
	return vector
	
def initialize_vectors_array(array_with_words_of_posts, dictionary):
	vectors = []
	print()
	for words_in_post in array_with_words_of_posts:
		vectors.append(initialize_vector(words_in_post, dictionary))
	return vectors

def write_vectors_to_file(vectors, path_to_file):
	with open(path_to_file, 'w', encoding = 'utf-8') as file:
		file.write(str(vectors))
		file.close()

"""
EXAMPLE USAGE:

posts = [
			['ага', 'так'],
			['не', 'потому'],
			['кукуку', 'вавава', 'лолололо']
	    ]

dictionary = open('data/dictionary.txt', 'r', encoding = 'utf-8')
vectors = initialize_vectors_array(posts, eval(dictionary.read()))
dictionary.close()
print(vectors)
write_vectors_to_file(vectors, 'data/vectors.txt')

"""
