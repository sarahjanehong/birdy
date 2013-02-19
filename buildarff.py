''' 
Gathering Feature Information:
Takes tokenized and tagged tweets and builds an ARFF datafile 
(Attribute-Relation File Format) that will be used to classify tweets
------------------------------------------------------------------------------
e.g. Weather ARFF file
@relation weather

@attribute outlook {sunny, overcast, rainy}
@attribute temperature numeric
@attribute humidity numeric
@attribute windy {TRUE, FALSE}
@attribute play {yes, no}

@data
sunny,85,85,FALSE,no
sunny,80,90,TRUE,no
overcast,83,86,FALSE,yes
rainy,70,96,FALSE,yes
rainy,68,80,FALSE,yes
rainy,65,70,TRUE,no
overcast,64,65,TRUE,yes
sunny,72,95,FALSE,no
sunny,69,70,FALSE,yes
rainy,75,80,FALSE,yes
sunny,75,70,TRUE,yes
overcast,72,90,TRUE,yes
overcast,81,75,FALSE,yes
rainy,71,91,TRUE,no
'''

import sys
import re
from helper import *

first = open('./word_rules/First-person', 'r').read().replace('\n', '/|')
second = open('./word_rules/Second-person', 'r').read().replace('\n', '/|')
third = open('./word_rules/Third-person', 'r').read().replace('\n', '/|')
slang = open('./word_rules/Slang', 'r').read().replace('\n', '/|')
# emoticons = open('./Emoticons', 'r').read().replace('\n', '/|')

features = [
  ['first_person numeric', first],
  ['second_person numeric', second],
  ['third_person numeric', third],
  ['conjunct numeric', '/CC'],
  ['past_tense_verb numeric', '/VBD'],
  # simple future - www.englishpage.com/verbpage/simplefuture.html
  ['furture_tense_verb numeric', "will/MD|'ll/MD|going/VBG to/TO \w+/VB|gonna/VBG \w+/VB"], 
  ['commas numeric', ',/'],
  ['colons_semicolons numeric', '\:/|\;/'],
  ['dashes numeric', '-/|w+?-w+?/'],
  ['parentheses numeric', '\(/\(|\)/\)'],
  ['ellipses numeric', '.\.\./:|\.*?/CD'],
  ['common_nouns numeric', '/NN|/NNS'],
  ['proper_nouns numeric', '/NNP|/NNPS'],
  ['adverbs numeric', '/RBR|/RB|/RBS'],
  ['wh_words numeric', '/WDT|/WP|/WP$|/WRB'],
  ['slang numeric', slang],
  #'emoticons numeric' : emoticons,
  ['uppercase numeric', '[A-Z]{2,}'], # all uppercase (at least 2 letters long)
  ['avg_sentence_len numeric'],
  ['avg_token_len numeric'],
  ['count_sentences numeric']
]

def avg_sentence_len(tweet, arff):
  ''' Writes the average number of tokens in each sentence of a tweet into ARFF file '''
  num_token = 0
  num_sent = 0
  sentences = tweet.split('\n')
  for sentence in sentences:
    tokens = sentence.split()
    for token in tokens:
      token = token.split('/')
      num_token += 1
    num_sent += 1
  if num_sent != 0: #ensure no division by zero
    avg = num_token / num_sent
    arff.write(str(avg) + ',')
  else:
    arff.write('0,')    
  
def avg_token_len(tweet, arff):
  ''' Writes the average number of characters in each token of a tweet into ARFF file '''
  num_chars = 0
  num_tokens = 0
  sentences = tweet.split()
  for token in sentences:
    token = token.split('/')
    if len(token) > 2 and token[0].isalpha():
      num_chars += len(token[0])
      num_tokens += 1
  if num_tokens != 0: #ensure no division by zero
    avg = num_chars / num_tokens
    arff.write(str(avg) + ',')
  else:
    arff.write('0,')
  
def count_sentences(tweet, arff):
  ''' Writes the number of sentences in a tweet into ARFF file '''
  sentences = tweet.split('\n')
  arff.write(str(len(sentences)) + ',')

def count_features(tweet, arff):
  ''' Writes the number of occurences (counts) for each feature
  for a tweet into ARFF file'''
  for feature in features:
    if len(feature) == 2:
      regex = feature[1]
      count = len(re.findall(regex, tweet, re.IGNORECASE))
      arff.write(str(count) + ',')

def write_relation(arff, name):
  ''' Writes the relation name for the ARFF file '''
  relation = name + '\n\n' #takes arff filename as name of the relation
  arff.write('@relation ' + relation)

def write_attr(arff):
  ''' Writes the attributes (keys of the features dictionary) for the ARFF file '''
  for feature in features:
    arff.write('@attribute ' + feature[0] + '\n')

def write_attr_class(arff):
  ''' Writes the attribute class for the ARFF file '''
  arff.write('@attribute class {')
  for i in range(len(_class)):
    if i == len(_class)-1: 
        arff.write(_class[i])
    else:
      arff.write(_class[i] + ', ')
  arff.write('} \n\n')

def write_data(arff):
  ''' Writes the data for the ARFF file '''
  arff.write('@data\n')
  for f in _tweets: #for each key (twt files) from _tweets
    twt = open(f, 'r')
    str_twt = twt.read()[2:] #reads entire file, and removes beginning pipe '|' delimiter
    tweets = str_twt.split('\n|\n')
    
    if limit > 0: #checks for read limit on file
      if limit < len(tweets):
	       tweets = tweets[:limit]
      else:
	       print "limit out of bounds"
	
    for tweet in tweets: #aggregating counts for each feature on each tweet
      count_features(tweet, arff)
      avg_sentence_len(tweet, arff)
      avg_token_len(tweet, arff)
      count_sentences(tweet, arff)
      arff.write(_tweets[f] + '\n')

if __name__ == '__main__':
  if len(sys.argv) < 2:
    exit("Not enough arguments: requires .twt file and output ARFF file")
  else:
    _class = []
    _tweets = {}
    prog = sys.argv.pop(0)
    f = sys.argv.pop() #output file
    
    # determine number of tweets from each .twt that'll be used to build the arff
    if sys.argv[0][0] == '-':
      limit = int(sys.argv[0][1:]) 
      sys.argv.pop(0) 
    else:
      limit = -1

    # go through each twt
    for arg in sys.argv:
      inputs = arg.split(':')
      if len(inputs) > 1:
        _class.append(inputs.pop(0)) #get classname if specified
      else:
        _class.append(inputs[0]) #entire class defn is classname
        
      twts = inputs[0].split('+')
      for t in twts:
        _tweets[t] = _class[-1] #add filename as key with class as the value

    arff = open(f, 'w')
    write_relation(arff, f.split('.')[0])
    write_attr(arff)
    write_attr_class(arff)
    write_data(arff)
    arff.close()
