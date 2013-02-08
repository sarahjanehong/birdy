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

import string
import re
import sys


def write_relation(arff, name):
  relation = name + '\n\n' # takes arff filename as name of the relation
  arff.write('@relation ' + relation)

def write_attr(arff, features):
  for f in features:
    arff.write('@attribute ' + f[0] + '\n')

def write_attr_class(arff, features):
  arff.write('@attribute classes {')
  for i in range(len(_class)):
    if i == len(_class)-1: 
        arff.write(_class)
    else:
      arff.write(_class[c] + ', ')
  arff.write('} \n\n')

def write_data(arff):
  arff.write('@data\n\n')
  files = iter(_tweets) #gets the keys (twt files) from _tweets
  for twt in files:
      twtfile = open(twt, 'r')
      # split file by tweets in order to apply limit
      # get rid of starting "|\n"
      tweets = twtfile.read()[2:].split('\n|\n')
      if limit > 0:
        if limit < len(twt):
          tweets = tweets[:limit]
        else:
          print "limit out of bounds"

      for t in tweets:
          for f in features:
              if len(f) > 2:
                  f[1](t, arff, f[2])
                  arff.write(',')
              else:
                  f[1](t, arff)
                  arff.write(',')
              
          # write class name
          arff.write(twts[twt] + '\n')



if __name__ == '__main__':
  if len(sys.argv) < 2:
    exit("Not enough arguments: requires .twt file and output ARFF file")

  else:
    _class = []
    _tweets = {}
    prog = sys.argv.pop(0)

    # determine no. of tweets from each .twt that'll be used to build the arff
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

    f = sys.argv.pop() #output file
    arff = open(f, 'w')
    write_relation(arff, f.split('.')[0])
    write_attr(arff)
    write_attr_class(arff)
    write_data(arff)



      