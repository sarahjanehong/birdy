''' 
Gathering Feature Information:
Takes tokenized and tagged tweets and builds an ARFF datafile 
(Attribute-Relation File Format) that will be used to classify tweets
----------------------------------------------------------------------------------------------------
Feature extraction is basically the process of analyzing the
preprocessed data in terms of variables that are indicative of the source of the data.
----------------------------------------------------------------------------------------------------

The next n arguments represent the n classes you are using; 
classes may contain one or more .twt files joined by pluses (+). 

In order to specify the name of the class in the arff, a class may be prefaced by an optional class name followed by a colon (:)
If there is no classname, the entire class definition is taken as the class name. 
The last argument is the output arff file.

For example:
buildarff.py -500 justinbieber.twt britneyspears.twt jbbs.arff
buildarff.py pop:rihanna.twt+katyperry.twt news:bbcnews.twt+cnn.twt popvnews.arff
----------------------------------------------------------------------------------------------------
For each tweet, you need to extract 20 features and write these to the arf file. 
These features are listed in Table 3. 

Many of these involve counting tokens in a tweet that have certain characteristics that can be discerned from its tag. 

For example, counting the number of adverbs in a tweet involves counting the number of tokens that have been tagged as RB, RBR, or RBS. 

Table 4 explicitly defines some of the features in Table 3; 
these definitions are available on CDF in the directory /u/cs401/Wordlists/. 
You may copy and modify these files, but do not change their fienames. 
Be careful about capitalization; in all cases you should count both capitalized and lower case forms 
(e.g., both he and He count towards the number of third person pronouns).


When your feature extractor works, build an arf file, cnncbc.arff, that classifies CNN and CBC tweets using the first 100 tweets from each source.


TABLE 3 (20 feature)
Counts:
| First person pronouns
| Second person pronouns
| Third person pronouns
| Coordinating conjunctions
| Past-tense verbs
| Future-tense verbs
| Commas
| Colons and semi-colons
| Dashes
| Parentheses
| Ellipses
| Common nouns
| Proper nouns
| Adverbs
| wh-words
| Modern slang acroynms
| Words all in upper case (at least 2 letters long)
Average length of sentences (in tokens)
Average length of tokens, excluding punctuation tokens (in characters)
Number of sentences


Table 4:
First person:
I, me, my, mine, we, us, our, ours
Second person:
you, your, yours, u, ur, urs
Third person:
he, him, his, she, her, hers, it, its, they, them, their, theirs
Future Tense:
'll, will, gonna, going+to+VB
Common Nouns:
NN, NNS
Proper Nouns:
NNP, NNPS
Adverbs:
RB, RBR, RBS
wh-words :
WDT, WP, WP$, WRB
Modern slang acronyms:
smh, fwb, lmfao, lmao, lms, tbh, ro, wtf, b, wyd, lylc, brb, atm, imao, sml, btw,
bw, imho, fyi, ppl, sob, ttyl, imo, ltr, thx, kk, omg, ttys, afn, bbs, cya, ez, f2f, gtr,
ic, jk, k, ly, ya, nm, np, plz, ru, so, tc, tmi, ym, ur, u, sol



'''
import sys









def feature():
  return
  


  
  

if __name__ == '__main__':
  if len(sys.argv) < 2:
    exit("Not enough arguments: requires .twt file and output ARFF file")

  else:
    prog = sys.argv.pop(0)
    arff = sys.argv.pop() # the output file
    
    # determine no. of tweets from each .twt that'll be used to build the arff
    if sys.argv[0][0] == '-':
      limit = int(sys.argv[0][1:]) 
      sys.argv.pop(0) 
    else:
      limit = -1
    
    for arg in sys.argv:
      fn = arg.split(':')
      if len(fn) > 1:
	_class = fn.pop(0) #get classname if specified

      twt = fn[0].split('+')
      for i in twt
	
      
	
      
      
      
      #buildarff.py -500 justinbieber.twt britneyspears.twt jbbs.arff
  #buildarff.py pop:rihanna.twt+katyperry.twt news:bbcnews.twt+cnn.twt popvnews.arff