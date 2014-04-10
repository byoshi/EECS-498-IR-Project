import collections, re, sys, os
from parse import tokenizeIndividualDocument


def bagOfWords():
	texts = ['John likes to watch movies. Mary likes too.',
	  'John also likes to watch football games.']
	bagsofwords = [ collections.Counter(re.findall(r'\w+', txt))
	           for txt in texts]
	bagsofwords[0]
	Counter({'likes': 2, 'watch': 1, 'Mary': 1, 'movies': 1, 'John': 1, 'to': 1, 'too': 1})
	bagsofwords[1]
	Counter({'watch': 1, 'games': 1, 'to': 1, 'likes': 1, 'also': 1, 'John': 1, 'football': 1})
	sumbags = sum(bagsofwords, collections.Counter())
	sumbags
	Counter({'likes': 3, 'watch': 2, 'John': 2, 'to': 2, 'games': 1, 'football': 1, 'Mary': 1, 'movies': 1, 'also': 1, 'too': 1})
 
def main():
	if len(sys.argv) != 3:
		print "usage: ./bow.py [documents directory path] [stopwords file]"

	directory = sys.argv[1]
	stopwords_file = sys.argv[2]

	file_to_tf_dict = {}
	for dirpath, dirnames, filenames in os.walk(directory):
		for f in filenames:
			cur_file = open(directory + "/" + f, 'r')
			file_to_tf_dict[f] = tokenizeIndividualDocument(cur_file, stopwords_file)

	for filename, tf_dict in file_to_tf_dict:
		print "Current file:", filename
		for token, tf in tf_dict.iteritems():
			print token, tf

if __name__ == '__main__':
	main()