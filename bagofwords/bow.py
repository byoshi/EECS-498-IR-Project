import collections, re, sys, os, bz2
from parse import tokenizeWiki


def bagOfWords(tf_dict_list, k_means_filename, all_words):
	print "Vocab size =", len(all_words)
	tf_list_list = [[0]*len(all_words)]*len(tf_dict_list)

	# k_means_file = open(k_means_filename, 'w')
	# file_bow = ""
	# words_str = ""
	# for word in all_words:
	# 	words_str += word
	# 	words_str += " "

	# words_str += "\n"
	# k_means_file.write(words_str)

	#Create and print bow vectors
	i = 0
	for tf_dict in tf_dict_list:
		j = 0
		for word in all_words:
			if word in tf_dict:
				# k_means_file.write(str(tf_dict[word]))
				tf_list_list[i][j] = tf_dict[word]
				# file_bow += str(tf_dict[word])
			else:
				# k_means_file.write('0')
				tf_list_list[i][j] = 0
				# file_bow += "0"
			# file_bow += " "

			# k_means_file.write(' ')
			# tf_list_list.append(' ')
			j += 1

		# k_means_file.write('\n')
		# tf_list_list[i].append('\n')

		# k_means_file.write(file_bow[0:len(file_bow)-1] + "\n")
		# tf_list_list.append(file_bow[0:len(file_bow)-1] + "\n")
		# k_means_file.write("%d" % tf_list_list[i])
		# file_bow = ""
		i += 1
		print "Saving vectors", i, "/", len(tf_dict_list)

	# k_means_file.close()
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
	# file_to_tf_dict = {}
	# for dirpath, dirnames, filenames in os.walk(directory):
	# 	for f in filenames:
	# 		cur_file = open(directory + "/" + f, 'r')
	# 		file_to_tf_dict[f] = tokenizeIndividualDocument(cur_file.read(), stopwords_file)
	# 		cur_file.close()

	bagOfWords(tf_dict_list, k_means_filename, all_words)

if __name__ == '__main__':
	main()
