#!/usr/bin/python

import argparse
from string import ascii_lowercase
from itertools import ifilter, imap


class NotAWordError(Exception): pass
class LengthError(Exception): pass

class WordPathFinder:
    """Class for finding word paths between two equally long words by exchanging
        one character at a time"""

    def __init__(self, dict_filename, length):
        with open(dict_filename) as dict_file:
            dict_stripped = imap(lambda x: x.strip().lower(), dict_file)
            dict_filtered = ifilter(lambda x: len(x)==length, dict_stripped)
            self.__words = dict((x, None) for x in dict_filtered)
        self.__is_clear = True
        self.__length = length

    def find(self, start, end):
        for w in (start, end):
            if len(w) != self.__length:
                raise LengthError("'{}' has wrong length".format(w))
            if w not in self.__words:
                raise NotAWordError("'{}' is not a word".format(w))
        self.__clear()
        if not self.__flood_scan(end, start):
            return None
        self.__words[end] = None
        path = []
        while start is not None:
            path.append(start)
            start = self.__words[start]
        return path

    ### private methods ###
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

    wpf = WordPathFinder(args.dict, len(args.start))

    try:
        wordpath = wpf.find(args.start, args.end)
    except (NotAWordError, LengthError) as e:
        print "Error: " + str(e)
        exit(1)

    if wordpath is not None:
        print '\n'.join(wordpath)
    else:
        print "No path found."

if __name__ == '__main__':
    main()
