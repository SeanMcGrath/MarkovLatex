import subprocess, shlex, webbrowser, threading

class Document:

	def __init__(self, outfile):

		try:
			self.outfile = open(outfile,'w')
			self.out = outfile
		except:
			raise IOError('{} is not a valid output file'.format(outfile))

	def write(self, toWrite):

		if self.outfile is not None:
			self.outfile.write(toWrite)

	def begin(self, title):

		#Preamble
		self.write(r'\documentclass[10pt]{book}' +'\n')
		self.write(r'\usepackage{multicol}' +'\n')
		self.write(r'\usepackage{graphics}\usepackage{lmodern}\usepackage{rotating}\usepackage{yfonts}\usepackage[T1]{fontenc}' +'\n')
		self.write(r'\usepackage{lettrine}'+'\n')
		self.write(r'\usepackage[papersize={8.25in,10.75in},left=0.5in,right=0.5in,top=0.5in,bottom=0.5in]{geometry}'+'\n')
		self.write(r'\setcounter{collectmore}{-1}' + '\n')

		#Title Page
		self.write(r'\title{' + title + '}\n')
		self.write(r'\date{}' + '\n')
		self.write(r'\begin{document}' + '\n')
		self.write(r'\maketitle' + '\n')
		self.write(r'\begin{multicols}{3}' + '\n')

	def end(self):

		#close LaTeX, close file
		self.write(r'\end{multicols}{3}' + '\n')
		self.write(r'\end{document}')
		self.outfile.close()

	def writeChapter(self, title, chapter, end=False):

		self.write(r'\chapter{' + title + '}\n')
		drop, space, rest = chapter.partition(' ')
		self.write(r'\lettrine[lines=4,findent = 2pt,nindent = -2pt]{' + drop[0] + '}{' + drop[1:len(drop)]+'} '+ rest + '\n')

	def compile(self):

		self.end()

		#compile PDF
		devnull = open('/dev/null', 'w')
		compileDoc=subprocess.Popen(shlex.split('pdflatex -output-directory ../output/ ' + self.out), stdout=devnull)
		compileDoc.wait()

		#view PDF
		threading.Thread(target = lambda: webbrowser.open_new(self.out.replace('.tex','.pdf'))).start()

