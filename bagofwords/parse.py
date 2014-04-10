#!/usr/bin/python
import sys
import re
from random import randint
import os.path
import string
from stemmer import PorterStemmer
import collections

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
  dictlist = getWordsFromDictionary(dict)
  for word in stopwords:
    if word in dictlist:
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

def stemWords(dict):
  ps = PorterStemmer()
  dictlist = getWordsFromDictionary(dict)
  for word in dictlist:
    stemmed_word = ps.stem(word, 0, len(word)-1)
    if word != stemmed_word:
      if stemmed_word in dict:
        dict[stemmed_word] += dict[word]
      else:
        dict[stemmed_word] = dict[word]
      del dict[word]

def updateDict(dict, updatingDict):
  for key, value in dict.iteritems():
    if key in updatingDict:
      updatingDict[key] += value
    else:
      updatingDict[key] = value

def tokenizeDocuments(directory, stopwordFilename):
  allTokensDict = {}
  for dirpath, dirnames, filenames in os.walk(directory):
    for f in filenames:
      text = removeSGML(directory + f)
      dictOfTokens = tokenize(text)
      updateDict(dictOfTokens, allTokensDict)
  
  listOfStopwords = readStopWords(stopwordFilename)
  removeStopWords(allTokensDict, listOfStopwords)
  stemWords(allTokensDict)
  return allTokensDict

def tokenizeIndividualDocument(doc, stopwords):
  doc = removeSGML(doc)
  docTokensDict = tokenize(doc)
  removeStopWords(docTokensDict, stopwords)
  stemWords(docTokensDict)
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
  for meta in articles_meta:
    if re.search("title", meta) is not None:
      cur_title_index = meta.index("title")
      cur_title_end_index = meta.index(">")
      cur_title = meta[cur_title_index + 7:cur_title_end_index - 1]
      article_names_file.write(cur_title + "\n");
      tf_dicts_list.append(tokenizeIndividualDocument(articles[article_index], stopwords))
      article_index += 1

  return tf_dicts_list

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
  
