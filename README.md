# Text Generator 
This is a text generator, using Markov chains approach. Markov chain is a sequence of random events in which the future doesn't depend on the past. Our generator will generate a new word based on the knowledge of the previous two.

* GetCorpus.py: Script to download the training corpus to hard drive. It downloads given number of pages from website http://tululu.org/ (only russian language). NOTE: size of text is quite big, so you might need to decrease the NUMBER_OF_PAGES constant to 10

* CalculateStatistics.py: Makes a statistics about the occurences of single words, pair of words and triple of words. Caches everything to file

* TextGenerator: Generates a text with given number of sentences.
