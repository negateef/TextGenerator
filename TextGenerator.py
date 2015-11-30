from GetCorpus import download_corpus
from CalculateStatistics import dump_statistics, decode_statistics
from random import randint


class Generator(object):
    def __init__(self, words, double_words, triple_words):
        self.words = words
        self.double_words = double_words
        self.triple_words = triple_words

    def generate_text(self, file_path='text.txt', length=100):
        text_file = open(file_path, 'w')
        text_file.write('\t')
        for index in xrange(length):
            line = self.generate_line()
            text_file.write(line.encode('utf-8') + ' ')
            if randint(0, 5) == 0:
                text_file.write('\n\t')
        text_file.close()

    def generate_line(self):
        words_list = []
        first_word = self.words[randint(0, len(self.words) - 1)]
        words_list.append(first_word[0].upper() + first_word[1:])
        if first_word[-1] == u'.':
            return ' '.join(words_list)

        second_index = randint(0, len(self.double_words[first_word]) - 1)
        second_word = self.double_words[first_word][second_index]
        words_list.append(second_word)
        if second_word[-1] == u'.':
            return ' '.join(words_list)

        while True:
            first_word = words_list[-2].lower()
            second_word = words_list[-1].lower()

            non_empty = (first_word, second_word) in self.triple_words
            if non_empty:
                third_index = randint(0, len(self.triple_words[(first_word, second_word)]) - 1)
                third_word = self.triple_words[(first_word, second_word)][third_index]
            else:
                third_word = self.words[randint(0, len(self.words) - 1)]
            words_list.append(third_word)

            if third_word[-1] == u'.':
                break

        return ' '.join(words_list)


def main():
    download_corpus(folder_path='corpus/', overwrite=False, output=True)
    dump_statistics(folder_path='corpus/', overwrite=False, output=True)
    words, double_words, triple_words = decode_statistics(output=True)

    generator = Generator(words, double_words, triple_words)
    generator.generate_text(file_path='generated_text.txt', length=5000)

if __name__ == "__main__":
    main()
