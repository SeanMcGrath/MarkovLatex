from lib.markovUtilities import TextGenerator
from lib.texUtilities import Document as doc
import sys

def main(args):

	if not args:
		print('Usage: BibleGen INFILE [OUTFILE]')
		return 1
	else:
		try:
			corpus = open(args[0], 'r')
		except:
			print(args[0] + ' is not a valid input file.')
			return 1

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
			d.writeChapter(textGen.title(),textGen.chapter())
			d.compile()
		except Exception as e:
			print(e)
			return 1

		return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))