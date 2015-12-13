#!/usr/bin/python

import argparse
from string import ascii_lowercase
from itertools import ifilter, imap

def mutator(word):
    """Generator for all valid mutations of a word"""
    for i in range(len(word)):
        for c in ascii_lowercase:
            yield word[:i] + c + word[i+1:]

def flood_scan(seed, destination, words):
    """Flood fill that stores the parent-nodes in 'words' dict"""
    border = [seed]
    while border:
        new_border = []
        for word in border:
            new_neighbors = ifilter(lambda x: x in words and words[x] is None,
                                mutator(word))
            for neighbor in new_neighbors:
                #print neighbor
                words[neighbor] = word
                if neighbor == destination:
                    return True
                new_border.append(neighbor)
        border = new_border
        #print "border: " + str(border)
    return False

def find_path(start, end, words):
    if not flood_scan(end, start, words):
        return
    words[end] = None
    path = []
    while start is not None:
        path.append(start)
        start = words[start]
    return path

def load_words(dict_filename, length):
    with open(dict_filename) as dict_file:
        dict_stripped = imap(lambda x: x.strip(), dict_file)
        dict_filtered = ifilter(lambda x: len(x)==length, dict_stripped)
        words = dict((x, None) for x in dict_filtered)
        return words

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

    words = load_words(args.dict, len(args.start))

    for word in (args.start, args.end):
        if not word in words:
            print "{} is not a word.".format(word)
            exit(1)

    wordpath = find_path(args.start, args.end, words)
    if wordpath is not None:
        for word in wordpath:
            print word
    else:
        print "No path found."

if __name__ == '__main__':
    main()
