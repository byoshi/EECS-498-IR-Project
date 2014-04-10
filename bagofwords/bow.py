import collections, re, sys, os
from parse import tokenizeIndividualDocument


def bagOfWords():
 
def main():
	if len(sys.argv) != 3:
		print "usage: ./bow.py [documents directory path] [stopwords file]"

	directory = sys.argv[1]
	stopwords_file = sys.argv[2]

	file_to_tf_dict = {}
	for dirpath, dirnames, filenames in os.walk(directory):
		for f in filenames:
			cur_file = open(directory + "/" + f, 'r')
			file_to_tf_dict[f] = tokenizeIndividualDocument(cur_file.read(), stopwords_file)

	for filename, tf_dict in file_to_tf_dict.iteritems():
		print "Current file:", filename
		for token, tf in tf_dict.iteritems():
			print token, tf

if __name__ == '__main__':
	main()