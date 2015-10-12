import string
from random import choice

EOS = ['.','!','?']
PUNCTUATION = set(string.punctuation)

class TupleDictionary:
    """
    Container for couplet, triplet and quartet dictionaries
    along with the text from which they were generated.
    """

    def __init__(self, couplets, triplets, quartets, source = None, *args):

        self.source = source
        self.couplets = couplets
        self.triplets = triplets
        self.quartets = quartets


class DictionaryBuilder:
    """
    Factory class for building TupleDictionary objects from text files.
    """

    def __init__(self, corpus):
        """
        Constructor

        :param corpus: a list of plain-text files.
        """

        temp = [file.read().split() for file in corpus] # split files to lines
        self.corpus = [item for sublist in temp for item in sublist] # Flatten list of lists

    @property
    def quartets(self):
        """
        The dictionary of four-word strings in the corpus that begin with the key string.
        """

        quartets = {}
        for i, word in enumerate(self.corpus):
            try:
                first, second, third, fourth = self.corpus[i], self.corpus[i+1], self.corpus[i+2], self.corpus[i+3]
            except IndexError:
                break
            key = (first,second,third)
            if key not in quartets:
                quartets[key] = []

            if fourth not in quartets[key]:
                quartets[key].append(fourth)

        return quartets

    @property
    def triplets(self):
        """
        The dictionary of four-word strings in the corpus that begin with the key string.
        """

        triplets = {}
        for i, word in enumerate(self.corpus):
            try:
                first, second, third = self.corpus[i], self.corpus[i+1], self.corpus[i+2]
            except IndexError: break
            key = (first,second)
            if key not in triplets:
                triplets[key] = []

            triplets[key].append(third)

        return triplets

    @property
    def couplets(self):
        """
        The dictionary of four-word strings in the corpus that begin with the key string.
        """

        couplets = {}
        for i, word in enumerate(self.corpus):
            try:
                first, second = self.corpus[i], self.corpus[i+1]
            except IndexError:
                break
            key = first
            if key not in couplets:
                couplets[key] = []

            couplets[key].append(second)

        return couplets

    def build(self):

        return TupleDictionary(self.couplets, self.triplets, self.quartets, self.corpus)

class TextGenerator:
    """
    Generates pseudorandom text of arbitrary length from the input text files.
    """

    def __init__(self, corpus):
        """
        Constructor
        :param list of plain-text files form which to pull text:
        :return:
        """

        self.tuples = DictionaryBuilder(corpus).build()

    def sentence(self):
        """
        Generate a pseudorandom sentence.
        :return: A sentence string.
        """

        quartets = self.tuples.quartets
        triplets = self.tuples.triplets
        couplets = self.tuples.couplets

        li = [key for key in quartets.keys() if key[0][0].isupper() and key[0][-1] not in EOS and len(key) > 1]
        key = choice(li)
        li = []

        first, second, third = key
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
            first, second, third = key

        return ' '.join(li)

    def capital(self):
        """
        Select a capitalized word form the corpus.
        :return: a single capitalized word.
        """

        keys = [key for key in self.tuples.couplets.keys() if key[0][0].isupper() and key[0][-1] not in EOS]
        short = [choice(keys)]
        short_str = ' '.join(short)
        return ''.join(ch for ch in short_str if ch not in PUNCTUATION)

    def paragraph(self, sentences = choice(range(3,15))):
        """
        Generate a pseudorandom paragraph.
        :param sentences: The numer of sentences in the paragraph.
        :return: A paragraph of text.
        """

        par = [self.sentence() for i in range(0, sentences)]
        return ' '.join(par)

    def chapter(self, paragraphs = choice(range(10,100))):
        """
        Generate a pseudorandom chapter of a book.
        :param paragraphs: The number of paragraphs in the chapter.
        :return: a chapter of text
        """

        chapter = [self.paragraph() for i in range(0, paragraphs)]
        return '\n\n'.join(chapter)

    def title(self):
        """
        Generate a pseudorandom title.
        :return: a title.
        """

        return r'The {} of {}'.format(self.capital(), self.capital())