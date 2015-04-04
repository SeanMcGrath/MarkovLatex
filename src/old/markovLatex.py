###############################

#Markov Chain Generation

###############################

import sys
import subprocess
import shlex
import string
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

def generate_short(dict_coup):

	li = [key for key in dict_coup.keys() if key[0][0].isupper() and key[0][-1] not in EOS]

	short = []

	short.append(choice(li))

	short_str = ' '.join(short)

	exclude = set(string.punctuation)
	return ''.join(ch for ch in short_str if ch not in exclude)

def start_doc(outfile,c):

	#Preamble
	outfile.write(r'\documentclass[10pt]{book}' +'\n')
	outfile.write(r'\usepackage{multicol}' +'\n')
	outfile.write(r'\usepackage{graphics}\usepackage{lmodern}\usepackage{rotating}\usepackage{yfonts}\usepackage[T1]{fontenc}' +'\n')
	outfile.write(r'\usepackage{lettrine}'+'\n')
	outfile.write(r'\usepackage[papersize={8.25in,10.75in},left=0.5in,right=0.5in,top=0.5in,bottom=0.5in]{geometry}'+'\n')
	outfile.write(r'\setcounter{collectmore}{-1}' +'\n')
	#outfile.write(r'\renewcommand{\LettrineFontHook}{\fontfamily{baroqueinitials}}')

	#Title Page
	outfile.write(r"\begin{document}" +'\n')
	outfile.write(r'{\begin{center}' + r'\vspace{10cm}')
	outfile.write(r'\Huge{The ' + generate_short(c) + ' of ' + generate_short(c) + r'}\end{center}}')
	outfile.write(r'\clearpage')
	

def end_doc(outfile):

	#close LaTeX, close file
	outfile.write(r"\end{document}")
	outfile.close()

#START

#build Dictionaries
corpus = open('necro.txt','r')

text = corpus.read().split()
d = build_triplet_dict(text)
f = build_couplet_dict(text)
q = build_quartet_dict(text)

#open .tex file for writing
doc = open('holee.tex','w')
start_doc(doc,f)

#Chapter Loop
for i in range(1,5):

	verses= 0
	doc.write(r"\begin{multicols}{3}")
	doc.write('\n')
	doc.write(r"\chapter{The " + generate_short(f) + ' of ' + generate_short(f) +'}\n')
	start = generate_sentence(d,f,q)
	drop, space, rest= start.partition(' ')
	doc.write(r'\lettrine[lines=4,findent = 2pt,nindent = -2pt]{' + drop[0] + '}{' + drop[1:len(drop)]+'}' + ' '+ rest + ' ')
	#Paragraphs
	for i in range(1,randint(20,60)):
		if i > 1:
			doc.write(r'$^{' + str(i) + '}$\n')

		#Sentences
		for j in range(1,randint(5,12)):

			#flip = False

			#if randint(0,10) < 2:
			#	flip = True

			#if flip:
			#	doc.write(r'\begin{turn}{180}')

			doc.write(generate_sentence(d,f,q) + ' ')

			#if flip:
			#	doc.write(r'\end{turn}')
			verses = verses +1

		doc.write('\n')
		doc.write('\n')

	doc.write(r"\end{multicols}")
	doc.write('\n')
	doc.write(r"\clearpage")
	doc.write('\n')

#close file
end_doc(doc)

#compile PDF
proc=subprocess.Popen(shlex.split('pdflatex holee.tex'))
proc.communicate()
