import subprocess
import shlex
import webbrowser
import threading

class Document:
    """
    Class representing a LaTeX document
    """

    def __init__(self, outfile):
        """
        Create a new document.
        :param outfile: the file path to the output .tex file
        """

        try:
            self.outfile = open(outfile,'w')
            self.out = outfile
        except:
            raise IOError('{} is not a valid output file'.format(outfile))

    def write(self, to_write):
        """
        Write to the output file
        :param to_write: the data to write.
        """

        if self.outfile is not None:
            self.outfile.write(to_write)

    def begin(self, title):
        """
        Write the document header.
        :param title: the title of the document.
        """

        if self.outfile is None:
            return

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
        """
        Write the document footer and close it.
        """

        self.write(r'\end{multicols}{3}' + '\n')
        self.write(r'\end{document}')
        self.outfile.close()

    def write_chapter(self, title, chapter):
        """
        Write a chapter to the document
        :param title: the title of the chapter
        :param chapter: the text of the chapter.
        """

        self.write(r'\chapter{' + title + '}\n')
        drop, space, rest = chapter.partition(' ')
        self.write(r'\lettrine[lines=4,findent = 2pt,nindent = -2pt]{' + drop[0] + '}{' + drop[1:len(drop)]+'} '+ rest + '\n')

    def compile(self):
        """
        Compile the document to PDF and display it.
        """

        self.end()

        #compile PDF
        devnull = open('/dev/null', 'w')
        compileDoc=subprocess.Popen(shlex.split('pdflatex -output-directory ../output/ ' + self.out), stdout=devnull)
        compileDoc.wait()

        #view PDF
        threading.Thread(target = lambda: webbrowser.open_new(self.out.replace('.tex','.pdf'))).start()

