MarkovLatex
===========

A set of utilities for gererating pseudorandom text via Markov chain and incorporating this text into LaTeX documents.

`markovLatex.markov` contains the TextGenerator class, which takes in a list of text files and exposes methods for generating sentences, paragraphs, and chapters of random text.

`markovLatex.tex` contains the Document class, which contains methods for interacting with and compiling a `.tex` file.

Two scripts are included - `markovGen`, which generates random text from input text files and prints it to stdout, and `bibleGen`, which is a little more fun. Feed `biblegen` a list of text files, and watch as it assembles then into a holy book for your new religion.


Copyright Sean McGrath 2015, issued freely under the MIT license.
