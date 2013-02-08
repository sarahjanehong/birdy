# TWeet Tokenize and Tag (TWTT)
import re
import sys
sys.path.append('./tagger') # to use NLPlib
import NLPlib as nlp
from helper import * # helper funcions

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
  symbols = ['.', '!', '?']
  processed = tweet.rstrip()
  for sym in symbols:
    processed = edit_line_r(processed, sym, '\n')
  return processed

def space(tweet):
  ''' Returns a tweet with spaces between punctuation '''
  regex = '(?P<prefix>\w+?)(?P<end>!+|\?+|\.+)' # ..., !!, ?? will be kept together, but spaced from whatever is before it
  while len(re.findall(regex, tweet)) > 0:
    match = re.search(regex, tweet)
    replace = match.group('prefix') + ' ' + match.group('end')
    tweet = re.sub(regex, replace, tweet, 1)
  return tweet

def tokenize(tweet):
  '''Returns a tweet where each token is separated by a space '''
  tweet = re.sub("'(?!t)", " '", tweet)
  return re.sub("n't", " n't", tweet)
  
def tag(tweet):
  '''Returns a string where each token is tagged using NLPlib in the form of:
  Meet/VB me/PRP today/NN at/IN the/DT FEC/NN in/IN DC/NN at/IN 4/NN ./.
  '''
  tagger = nlp.NLPlib()
  sentences = tweet.rstrip().split('\n')
  processed = ''
  for i in range(len(sentences)): #go through each sentence in a tweet
    sent = sentences[i].strip().split(' ')
    tags = tagger.tag(sent)
    tagged = []
    for i in range(len(tags)):
      tagged.append(sent[i] + '/' + tags[i]) #tag each token in the sentence
    processed += ' '.join(tagged) + '\n' #join into a processed tweet
  return '|\n' + processed.rstrip() + '\n'
  
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
    line = space(line)
    line = tokenize(line)
    line = tag(line)
    processed.write(line)
    
  processed.write('|')
  raw.close()
  processed.close()
  

if __name__ == '__main__':
  raw_file = sys.argv[1]
  processed_file = sys.argv[2]
  twtt(raw_file, processed_file)
  print "finished processing and tagging tweets"

