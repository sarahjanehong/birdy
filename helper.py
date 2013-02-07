''' Helper Functions for twtt.py'''

# adds \n after sym occurs in tweet
def new_line(tweet, sym):
  words = tweet.split(' ')
  processed = ''
  for i in range(len(words)):
    index = words[i].rfind(sym)
    if index != -1 and (words[i] not in abbrev_english or words[i] not in pn_abbrev_english):
      processed += words[i][:index+1] + '\n' + words[i][index+1:] + ' '
    else:
      processed += words[i] + ' '
  return processed

# parse the text files containing popular abbreviations
def strip_new_line(words):
  L = []
  for word in words:
    index = word.find('\n')
    L.append(word[:index])
  return L
  
abbrev_english = strip_new_line(open('./abbrev.english', 'r').readlines())
pn_abbrev_english = strip_new_line(open('./pn_abbrev.english', 'r').readlines())