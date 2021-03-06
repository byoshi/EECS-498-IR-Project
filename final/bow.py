import collections, re, sys, os, bz2
from parse import tokenizeWiki


def bagOfWords(tf_dict_list, all_words):
	print "Vocab size =", len(all_words)
	tf_list_list = [[0]*len(all_words) for i in range(len(tf_dict_list))]

	#Create and print bow vectors
	i = 0
	for tf_dict in tf_dict_list:
		j = 0
		k = 0
		for word in all_words:
			if word in tf_dict:
				tf_list_list[i][j] = tf_dict[word]
			else:
				tf_list_list[i][j] = 0
				k += 1
			j += 1
		i += 1
		print "Saving vectors", i, "/", len(tf_dict_list), len(all_words) - k

	return tf_list_list
 
def main():
	if len(sys.argv) != 4:
		print "usage: ./bow.py [wiki file] [stopwords file] [k-means output filename]"
		sys.exit(1)

	wiki_file_name = sys.argv[1]
	stopwords_file = sys.argv[2]
	k_means_filename = sys.argv[3]

	wiki_file = open(wiki_file_name, "r")
	tf_dict_list, all_words = tokenizeWiki(wiki_file.read(), stopwords_file)

	bagOfWords(tf_dict_list, k_means_filename, all_words)

if __name__ == '__main__':
	main()
