###############################

#Markov Chain Generation

###############################

import sys
from pprint import pprint
from random import choice, randint

EOS = ['.','!','?']

def build_quartet_dict(corpus):

	dict = {}
	for i, word in enumerate(corpus):
		try:
			first, second, third, fourth = corpus[i], corpus[i+1], corpus[i+2], corpus[i+3]
		except IndexError:
			break
		key = (first,second,third)
		if key not in dict:
			dict[key] = []

		if fourth not in dict[key]:
			dict[key].append(fourth)

	return dict

def build_triplet_dict(corpus):

	dict = {}
	for i, word in enumerate(corpus):
		try:
			first, second, third = corpus[i], corpus[i+1], corpus[i+2]
		except IndexError:
			break
		key = (first,second)
		if key not in dict:
			dict[key] = []

		dict[key].append(third)

	return dict

def build_couplet_dict(corpus):

	dict = {}
	for i, word in enumerate(corpus):
		try:
			first, second = corpus[i], corpus[i+1]
		except IndexError:
			break
		key = first
		if key not in dict:
			dict[key] = []

		dict[key].append(second)

	return dict

def generate_sentence(dict_trip, dict_coup,dict_quart):

	li = [key for key in dict_quart.keys() if key[0][0].isupper() and key[0][-1] not in EOS and len(key) > 1]

	key = choice(li)

	li = []

	first, second,third = key
	li.append(first)
	li.append(second)
	li.append(third)
	while True:
		try:
			if len(dict_quart[key]) > 1:
				fourth = choice(dict_quart[key])
			else:
				fourth = choice(dict_trip[(second,third)])
		except KeyError:
			try:
				fourth = choice(dict_trip[(second,third)])
			except KeyError:
				try:
					fourth = choice(dict_coup[third])
				except KeyError:
					fourth = choice(dict_coup.keys())
		li.append(fourth)
		if fourth[-1] in EOS:
			break

		key = (second, third,fourth)
		first,second,third = key

	return ' '.join(li)

corpus = open('necro.txt','r')

text = corpus.read().split()
d = build_triplet_dict(text)
f = build_couplet_dict(text)
q = build_quartet_dict(text)
print 

for i in range(1,10):
	print str(randint(1,100))+ '. ' + generate_sentence(d,f,q)