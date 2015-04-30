import string
from random import choice
import itertools

EOS = ['.','!','?']

class TupleDictionary:

	def __init__(self, couplets, triplets, quartets, source = None, *args):

		self.source = source
		self.couplets = couplets
		self.triplets = triplets
		self.quartets = quartets

class DictionaryBuilder():

	def __init__(self, corpus, *args):

		temp = [file.read().split() for file in corpus] # split files to lines
		self.corpus = [item for sublist in temp for item in sublist] # Flatten list of lists

	def buildQuartets(self, corpus):

		quartets = {}
		for i, word in enumerate(corpus):
			try:
				first, second, third, fourth = corpus[i], corpus[i+1], corpus[i+2], corpus[i+3]
			except IndexError:
				break
			key = (first,second,third)
			if key not in quartets:
				quartets[key] = []

			if fourth not in quartets[key]:
				quartets[key].append(fourth)

		return quartets

	def buildTriplets(self, corpus):

		triplets = {}
		for i, word in enumerate(self.corpus):
			try:
				first, second, third = corpus[i], corpus[i+1], corpus[i+2]
			except IndexError: break
			key = (first,second)
			if key not in triplets:
				triplets[key] = []

			triplets[key].append(third)

		return triplets

	def buildCouplets(self, corpus):

		couplets = {}
		for i, word in enumerate(self.corpus):
			try:
				first, second = corpus[i], corpus[i+1]
			except IndexError:
				break
			key = first
			if key not in couplets:
				couplets[key] = []

			couplets[key].append(second)

		return couplets

	def getDictionary(self):

		return TupleDictionary(
			self.buildCouplets(self.corpus),
			self.buildTriplets(self.corpus),
			self.buildQuartets(self.corpus),
			self.corpus)

class TextGenerator:

	def __init__(self, corpus, *args):

		self.tuples = DictionaryBuilder(corpus).getDictionary()

	def sentence(self):

		quartets = self.tuples.quartets
		triplets = self.tuples.triplets
		couplets = self.tuples.couplets

		li = [key for key in quartets.keys() if key[0][0].isupper() and key[0][-1] not in EOS and len(key) > 1]
		key = choice(li)
		li = []

		first, second,third = key
		li.append(first)
		li.append(second)
		li.append(third)

		while True:
			try:
				if len(quartets[key]) > 1:
					fourth = choice(quartets[key])
				else:
					fourth = choice(triplets[(second,third)])
			except KeyError:
				try:
					fourth = choice(triplets[(second,third)])
				except KeyError:
					try:
						fourth = choice(couplets[third])
					except KeyError:
						fourth = choice(couplets.keys())
			li.append(fourth)
			if fourth[-1] in EOS:
				break

			key = (second, third,fourth)
			first,second,third = key

		return ' '.join(li)

	def short(self):

		li = [key for key in self.tuples.couplets.keys() if key[0][0].isupper() and key[0][-1] not in EOS]

		short = []
		short.append(choice(li))
		short_str = ' '.join(short)
		exclude = set(string.punctuation)

		return ''.join(ch for ch in short_str if ch not in exclude)

	def paragraph(self, sentences = choice(range(3,15))):

		par = []
		for i in range(0,sentences):
			par.append(self.sentence())

		return ' '.join(par)

	def chapter(self, paragraphs = choice(range(10,100))):

		chapter = []
		for i in range(0,paragraphs):
			chapter.append(self.paragraph())

		return '\n\n'.join(chapter)

	def title(self):

		return r'The {} of {}'.format(self.short(),self.short())