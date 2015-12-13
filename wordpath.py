#!/usr/bin/python

import argparse
from string import ascii_lowercase
from itertools import ifilter, imap

class WordPathFinder:
    """Class for finding word paths between two equally long words by exchanging
        one character at a time"""
    def __init__(self, dict_filename, length):
        with open(dict_filename) as dict_file:
            dict_stripped = imap(lambda x: x.strip().lower(), dict_file)
            dict_filtered = ifilter(lambda x: len(x)==length, dict_stripped)
            self.__words = dict((x, None) for x in dict_filtered)
        self.__is_clear = True

    def find(self, start, end):
        self.__clear()
        if not self.__flood_scan(end, start):
            return None
        self.__words[end] = None
        path = []
        while start is not None:
            path.append(start)
            start = self.__words[start]
        return path

    def has_word(self, word):
        return word in self.__words

# private methods
    def __flood_scan(self, seed, destination):
        """Flood fill that stores the parent-nodes in 'words' dict"""
        self.__is_clear = False
        border = [seed]
        while border:
            new_border = []
            for word in border:
                new_neighbors = ifilter(lambda x: x in self.__words and
                    self.__words[x] is None, WordPathFinder.__mutator(word))
                for neighbor in new_neighbors:
                    #print neighbor
                    self.__words[neighbor] = word
                    if neighbor == destination:
                        return True
                    new_border.append(neighbor)
            border = new_border
            #print "border: " + str(border)
        return False

    def __clear(self):
        if self.__is_clear:
            return
        for w in self.__words:
            self.__words[w] = None
        self.__is_clear = True

    @staticmethod
    def __mutator(word):
        """Generator for all valid mutations of a word"""
        for i in range(len(word)):
            for c in ascii_lowercase:
                yield word[:i] + c + word[i+1:]


def parse_args():
    parser = argparse.ArgumentParser(
        description='''Calculate the word path from one word to another by
            changing one character at a time.''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('start', help='the word to start with')
    parser.add_argument('end', help='the word to end with')
    parser.add_argument('--dict', default="/usr/share/dict/words",
                        help='dictionary file to use')
    return parser.parse_args()

def main():
    args = parse_args()

    if len(args.start) != len(args.end):
        print "Words are not of equal length!"
        exit(1)

    wpf = WordPathFinder(args.dict, len(args.start))

    for word in (args.start, args.end):
        if not wpf.has_word(word):
            print "{} is not a word.".format(word)
            exit(1)

    wordpath = wpf.find(args.start, args.end)
    if wordpath is not None:
        for word in wordpath:
            print word
    else:
        print "No path found."

if __name__ == '__main__':
    main()
