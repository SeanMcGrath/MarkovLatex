from lib.markovUtilities import TextGenerator
from lib.texUtilities import Document as doc
import PyQt4

corpus = open('necro.txt', 'r')
textGen = TextGenerator(corpus)
d = doc(r'../output/output.tex')
d.begin(r'The {} of {}'.format(textGen.short(),textGen.short()))
d.writeChapter(textGen.title(),textGen.chapter())
d.compile()
