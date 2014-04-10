import bz2
from parse import tokenizeWiki

f = "train.bz2"

source_file = bz2.BZ2File(f, "r")
tokenizeWiki(source_file.read(), "stopwords.txt")

# for line in source_file:
# 	print line

