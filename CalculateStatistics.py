# -*- coding: utf-8 -*-

import json
import os
import re
import string
from collections import defaultdict


def dump_statistics(folder_path, overwrite=False, output=True):
    if output:
        print 'Dump started!'

    if not overwrite:
        if os.path.exists('words') and os.path.exists('double_words') and os.path.exists('triple_words'):
            if output:
                print 'Cached version found! Dump is completed!'
            return

    words = list()
    double_words = defaultdict(list)
    triple_words = defaultdict(list)

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if output:
            print file_path

        book_file = open(file_path, "r")
        text = book_file.read()

        word_list = text.decode('utf-8').lower().split()

        for index in xrange(len(word_list)):
            current_word = word_list[index]
            words.append(current_word)
            if index <= len(word_list) - 2:
                next_word = word_list[index + 1]
                double_words[current_word].append(next_word)
            if index <= len(word_list) - 3:
                next_word = word_list[index + 1]
                third_word = word_list[index + 2]
                pair = (current_word, next_word)
                triple_words[pair].append(third_word)

    words_file = open('words', 'w')
    double_words_file = open('double_words', 'w')
    triple_words_file = open('triple_words', 'w')

    words_string = json.dumps(words)
    double_words_string = json.dumps(double_words)
    triple_words_string = json.dumps(triple_words.items())

    words_file.write(words_string)
    double_words_file.write(double_words_string)
    triple_words_file.write(triple_words_string)

    words_file.close()
    double_words_file.close()
    triple_words_file.close()

    if output:
        print 'Dump is completed!'


def decode_statistics(output=True):

    if output:
        print 'Decode started!'

    try:
        words_file = open('words', 'r')
        double_words_file = open('double_words', 'r')
        triple_words_file = open('triple_words', 'r')
    except IOError as e:
        print 'Some files are missing!'
        print 'Call dump_statistics first!'

    words_string = words_file.read()
    double_words_string = double_words_file.read()
    triple_words_string = triple_words_file.read()

    words = json.loads(words_string)
    double_words = json.loads(double_words_string)
    temp_triple = dict(map(tuple, kv) for kv in json.loads(triple_words_string))
    triple_words = {k: list(v) for k, v in temp_triple.iteritems()}

    words_file.close()
    double_words_file.close()
    triple_words_file.close()

    print 'Decode finished!'

    return (words, double_words, triple_words)


def main():
    dump_statistics('corpus/', overwrite=True)

if __name__ == "__main__":
    main()
