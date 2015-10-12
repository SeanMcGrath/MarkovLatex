#!/usr/bin/env python

from markovLatex.markov import TextGenerator
from markovLatex.tex import Document as doc
from random import randint
import argparse, sys

def main(args):

	parser = argparse.ArgumentParser(description="Access the Will of the Gods from the command line.")
	parser.add_argument('files', type=str, nargs='+', help='one or more input text files')
	parser.add_argument('-c','--chapters', type=int, help='The number of chapters in the output text')
	args = parser.parse_args(args)

	corpus = []
	for arg in args.files:
		try:
			corpus.append(open(arg, 'r'))
		except Exception as e:
			print(e)

	if corpus:
		try:
			d = doc(r'../output/output.tex')
			textGen = TextGenerator(corpus)
			title = textGen.title()
			print('\nBEHOLD:\n\n')
			print('THE GODS HAVE SMILED UPON US THIS DAY\n\n')
			print('THEY PASS ON TO YOU THIS HOLY TEXT:\n\n')
			print(title + '\n\n')
			print('SPREAD ITS MIGHTY WORD THROUGHOUT THE LAND')
			d.begin(title)
			for i in range(0, args.chapters or randint(10,20)):
				d.write_chapter(textGen.title(),textGen.chapter())
			d.compile()
		except Exception as e:
			print(e)
			return 1

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
