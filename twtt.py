# TWeet Tokenize and Tag (TWTT)
# Ellipsis (i.e., `...'), and other kinds of multiple punctuation 
#  (e.g., `!!!') are not split.
#
# Each token, including punctuation and clitics, is separated by spaces.
#   - Clitics are contracted forms of words, such as n't, that are concatenated 
#     with the previous word.
#   - Note that the possessive 's has its own tag and is distinct from the 
#     clitic 's, but nonetheless must be separated by a space; likewise, the 
#     possessive apostrophe on plurals must be separated.
#
# Each token is tagged with its part-of-speech.
#   - A tagged token consists of a word, the `/' symbol, and the tag 
#    (e.g., dog/NN). See below for information on how to use the tagging module.
#    The tagger can make mistakes.
#
# Between each tweet is the pipe symbol '|', which occurs on its own line.
#   - Pipes are supposed to occur at the beginning and end of each normalized file

import re
import sys
sys.path.append('./tagger') # to use NLPlib
import NLPlib as nlp

# some popular html character codes
d = {'&amp;':'&', 
    '&quot;':'"', 
    '&apos;':"'",
    '&lt;':'<', 
    '&gt;':'>', 
    '&cent':'cent',
    '&pound;':'pound', 
    '&yen;':'yen', 
    '&euro;':'euro', 
    '&sect;':'section',
    '&copy;':'copyright',
    '&reg;':'registered trademark',
    '&trade;':'trademark'
  }

# parse the text files containing popular abbreviations
def strip_new_line(words):
  L = []
  for word in words:
    index = word.find('\n')
    L.append(word[:index])
  return L
  
abbrev_english = strip_new_line(open('./abbrev.english', 'r').readlines())
pn_abbrev_english = strip_new_line(open('./pn_abbrev.english', 'r').readlines())
 

def remove_html(tweet):
  ''' Returns a string (tweet) with all html tags and attributes removed
  tweet: a single tweet (type str)
  '''
  return re.sub(r'<.*?>', '', tweet)

def convert_to_ascii(tweet):
  '''Returns a string (tweet) where all html character codes (i.e., &...;) are 
  replaced with an ASCII equivalent. 
  tweet: a single tweet (type str)
  '''
  while len(re.findall(r'&\w+;', tweet)) > 0: # while there exists the pattern "&...;"
    for key in d:
      if re.search(key, tweet): # convert html code to ascii
	tweet = re.sub(key, d[key], tweet)
  return tweet
  
def remove_links(tweet):
  ''' Returns a string (tweet) with all URLs removed
  (i.e., tokens beginning with http or www) are removed.
  URLs do not contain spaces. So, the end of a link must be followed by a space or EOL
  '''
  return re.sub(r'((http|https|ssh|ftp|www)|\w+\.\w+).*?( |$)', '', tweet, flags=re.IGNORECASE) #http, Http, HTTP, ssh, ftp, www, etc.
  
def remove_twitter_tags(tweet):
  '''Returns a string (tweet) where the first character in Twitter user 
  names (@) and hash tags (#) are removed.
  '''
  regex = '(@|#)(?P<tag_name>\w+)(?P<end>.*?( |$))'
  while len(re.findall(regex, tweet)) > 0:
    match = re.search(regex, tweet) #finds the first occurence of the regex in tweet
    replace = match.group('tag_name') + match.group('end')
    tweet = re.sub(regex, replace, tweet, 1)
  return tweet
 
def separate_sentences(tweet):
  '''Returns a string where each sentence within a tweet is on its own line.
  Requires detecting End-of-Sentence punctuation.
  '''
  words = tweet.split(' ')
  processed = ''
  for i in range(len(words)):
    period = words[i].find('.')
    exclaim = words[i].find('!')
    question = words[i].find('?')
    if period != -1 and (words[i] not in abbrev_english or words[i] not in pn_abbrev_english):
      processed += words[i] + '\n'
    elif exclaim != -1 or question != -1:
      processed += words[i] + '\n'
    else:
      processed += words[i] + ' '

  return '|\n' + processed.rstrip() + '\n'

  
def tokenize(tweet):
  '''Returns a tweet where each token is separated by a space
  '''

  return
  
 
def twtt(raw_file, processed_file):
  ''' Takes a file contain raw tweets (raw_file), processes each tweet, 
  and saves it in an output file (processed_file)
  raw_file: the input raw tweet file (.txt)
  processed_file: the output tokenized and tagged tweet file (.twt) 
  '''
  raw = open(raw_file, 'r')
  processed = open(processed_file, 'w')
  for line in raw:
    line = remove_html(line) #html removed
    line = convert_to_ascii(line) #html character codes changed to ascii 
    line = remove_links(line) #urls removed
    line = remove_twitter_tags(line) #hash tags and @-tags removed
    line = separate_sentences(line)
    line = tokenize(line)
    processed.write(line)
  processed.write('|')  
  raw.close()
  processed.close()
  

if __name__ == '__main__':
  raw_file = sys.argv[1]
  processed_file = sys.argv[2]
  twtt(raw_file, processed_file)
  print "finished processing and tagging file"

