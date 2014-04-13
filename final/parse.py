#!/usr/bin/env python
import sys
import re
from random import randint
import os.path
import string
import collections
from math import log10

all_words = []
all_words_set = set()
dictionary = {}
stopwords = set()
contractions = {
  'can\'t' : 'cannot',
  'could\'ve' : 'could have',
  'couldn\'t' : 'could not',
  'didn\'t' : 'did not',
  'doesn\'t' : 'does not',
  'don\'t' : 'do not',
  'hadn\'t' : 'had not',
  'hasn\'t' : 'has not',
  'haven\'t' : 'have not',
  'how\'d' : 'how did',
  'how\'ll' : 'how will',
  'I\'m' : 'I am',
  'I\'ve' : 'I have',
  'isn\'t' : 'is not',
  'let\'s' : 'let us',
  'might\'ve' : 'might have',
  'must\'ve' : 'must have',
  'needn\'t' : 'need not',
  'shan\'t' : 'shall not',
  'should\'ve' : 'should have',
  'shouldn\'t' : 'should not',
  'there\'ve' : 'there have',
  'they\'re' : 'they are',
  'they\'ve' : 'they have',
  'wasn\'t' : 'was not',
  'we\'ll' : 'we will',
  'we\'re' : 'we are',
  'we\'ve' : 'we have',
  'weren\'t' : 'were not',
  'where\'d' : 'where did',
  'won\'t' : 'will not',
  'would\'ve' : 'would not',
  'you\'re' : 'you are',
  'you\'ve' : 'you have'
}

contractions_expr = re.compile('(%s)' % '|'.join(contractions.keys()))

def readStopWords(filename):
  stopwords_file = open(filename, 'r')
  text = stopwords_file.read()
  return text.split()


def getWordsFromDictionary(dict):
  dictlist = []
  for key, value in dict.iteritems():
    dictlist.append(key)

  return dictlist


def removeStopWords(dict, stopwords):
  for word in stopwords:
    if word in dict.keys():
      del dict[word]


def expand_contractions(s):
  def replace(match):
    return contractions[match.group(0)]
  return contractions_expr.sub(replace, s)


def removeSGML(text):
  return re.sub('<[^>]*>', '', text)


def tokenize(text):
  tokenDict = {}
  text = re.sub('[\(){}?!+=*"]', '', text)

  #Remove colon at end of words
  text = re.sub('(?<!\d):', '', text)

  #Expand contractions
  text = expand_contractions(text)

  #Remove periods that are not decimals
  text = re.sub('\.(?!d)', '', text)

  #Remove double hyphens
  text = re.sub('(--)', '', text)

  #Replace forward slash with space
  text = re.sub('/', ' ', text)

  #Remove comma after number if followed by whitespace
  text = re.sub('(?<=\d)[,-](?=\s)', '', text)

  #Replace possessives
  text = re.sub('\'s', ' \'s', text)

  #Remove commas after words
  text = re.sub('(?<=\w)+,', '', text)

  #Remove standalone commas
  text = re.sub('(?<=\s)[,-](?=\s)', '', text)

  #Remove single quotes that are not possessive
  text = re.sub('\'(?!s)', '', text)

  #Removes single quotes from words that begin with 's
  text = re.sub('\'s(?=\w)', '', text)

  #Remove hyphens and commas before and after words and numbers
  text = re.sub('(?<=\s)[,-](?=\w|\d)', '', text)
  text = re.sub('(?<=\w|\d)[,-](?=\s)', '', text)

  #Remove hyphen followed by comma
  text = re.sub('-,', '', text)

  for word in text.rsplit():
    if word in tokenDict:
      tokenDict[word] += 1
    else:
      tokenDict[word] = 1
  return tokenDict


def getSubset(subset_num, subset_size):
  subset_dict = {}
  for i in range(subset_size):
    word = all_words[randint(0, len(all_words))]
    if word in subset_dict:
      subset_dict[word] = subset_dict[word] + 1
    else:
      subset_dict[word] = 1

  print "V value of subset", subset_num, ":", len(subset_dict)
  print "n value of subset", subset_num, ":", subset_size


def updateDict(dict, updatingDict):
  for key, value in dict.iteritems():
    if key in updatingDict:
      updatingDict[key] += value
    else:
      updatingDict[key] = value


def tokenizeIndividualDocument(doc, stopwords):
  doc = removeSGML(doc)
  docTokensDict = tokenize(doc)
  listOfStopwords = readStopWords(stopwords)
  removeStopWords(docTokensDict, listOfStopwords)
  return docTokensDict


def tokenizeWiki(wiki_file, stopwords):
  tf_dicts_list = []
  articles = re.split("</doc>", wiki_file)
  articles_meta = []
  
  #Get meta data from articles
  for article in articles:
    articles_meta.append(re.split("\n", article.lstrip())[0])

  article_names_file = open("article_names.txt", 'w')
  article_index = 0
  df_terms = []
  names = []
  for meta in articles_meta:
    if re.search("title", meta) is not None:
      cur_title_index = meta.index("title")
      cur_title_end_index = meta.index(">")
      cur_title = meta[cur_title_index + 7:cur_title_end_index - 1]
      article_names_file.write(cur_title + "\n");
      names.append(re.sub(" ", "_", cur_title))
      doc_tf_dict = tokenizeIndividualDocument(articles[article_index], stopwords)
      tf_dicts_list.append(doc_tf_dict)
      df_terms.extend(doc_tf_dict.keys())
      article_index += 1
      print "Processing", article_index, "/", len(articles_meta) - 1

  print "Tokenization...Done"

  doc_frequency = collections.Counter(df_terms)

  # doc_frequency = {}
  # tf_dict_idx = 1
  # for tf_dict in tf_dicts_list:
  #   for term in tf_dict.keys():
  #     if term in doc_frequency.keys():
  #       doc_frequency[term] += 1
  #     else:
  #       doc_frequency[term] = 1
  #   print "df calc:", tf_dict_idx, "/", len(tf_dicts_list)
  #   tf_dict_idx += 1

  print "df...Done"

  i = 0
  for tf_dict in tf_dicts_list:
    for term, tf in tf_dict.iteritems():
      tf_dict[term] = tf * log10(article_index/doc_frequency[term])\

    print "Processing", i, "/", len(tf_dicts_list)
    i += 1

  print "tfidf...Done"
  return tf_dicts_list, doc_frequency.keys(), names

if __name__ == '__main__':
  directory = "/afs/umich.edu/user/b/y/byoshi/eecs498/hw2/cranfieldDocs/"#raw_input("Enter cranfieldDocs directory path: ")
  stopwords_path = "/afs/umich.edu/user/b/y/byoshi/eecs498/hw2/stopwords.txt"#raw_input("Enter stopwords text file path: ")
  readStopWords(stopwords_path)
  formatter = string.Formatter()
  dictionary = tokenizeDocuments(directory, stopwords_path)
  
  
  for key, value in sorted(dictionary.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)
  
  print "Total # of words in collection: ", sum(dictionary.values())
  print "Vocabulary size: ", len(dictionary)
  
