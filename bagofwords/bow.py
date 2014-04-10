import collections, re, sys, os, bz2
from parse import tokenizeWiki


def bagOfWords(tf_dict_list, k_means_filename):
	all_words = []
	tf_list_list = []

	#Build a list of all tokens
	for tf_dict in tf_dict_list:
		for token in tf_dict.keys():
			if token not in all_words:
				all_words.append(token)
	print "Vocab size =", len(all_words)

	k_means_file = open(k_means_filename, 'w')
	file_bow = ""
	# words_str = ""
	# for word in all_words:
	# 	words_str += word
	# 	words_str += " "

	# words_str += "\n"
	# k_means_file.write(words_str)

	#Create and print bow vectors
	for tf_dict in tf_dict_list:
		for word in all_words:
			if word in tf_dict.keys():
				file_bow += str(tf_dict[word])
			else:
				file_bow += "0"
			file_bow += " "

		k_means_file.write(file_bow[0:len(file_bow)-1] + "\n")
		tf_list_list.append(file_bow[0:len(file_bow)-1] + "\n")
		file_bow = ""
	k_means_file.close()
	return tf_list_list
 
def main():
	if len(sys.argv) != 4:
		print "usage: ./bow.py [wiki file] [stopwords file] [k-means output filename]"
		sys.exit(1)

	wiki_file_name = sys.argv[1]
	stopwords_file = sys.argv[2]
	k_means_filename = sys.argv[3]

	wiki_file = open(wiki_file_name, "r")
	tf_dict_list = tokenizeWiki(wiki_file.read(), stopwords_file)
	# file_to_tf_dict = {}
	# for dirpath, dirnames, filenames in os.walk(directory):
	# 	for f in filenames:
	# 		cur_file = open(directory + "/" + f, 'r')
	# 		file_to_tf_dict[f] = tokenizeIndividualDocument(cur_file.read(), stopwords_file)
	# 		cur_file.close()

	bagOfWords(tf_dict_list, k_means_filename)

if __name__ == '__main__':
	main()
