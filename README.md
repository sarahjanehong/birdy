There are two parts to this project, twtt.py and buildarff.py

1. Preprocessing, tokenizing, and tagging parts-of-speech
-------------------------------------------------------------------------------
twtt.py takes in unprocessed tweets and removes noise by
- removing all HTML tags and attributes
- convert HTML character codes to ASCII equivalent (e.g. "&lt;" is changed to "<")
- all URLs are removed
- @ and # tags are removed
- each sentence in each tweet in on a new line
- each tweet is delimited with '|'
- ellipsis (...) and combinations of ! and ? are not split (e.g. "?!?!?!?!???")
- each token, including punctuation and clitics, is separated by a space (e.g. "we've" changed to "we 've")
- tagging each token with its part-of-speech

To run twtt.py, from the terminal, type:
```python twtt.py TWEETS OUTPUT```

where ...
- TWEETS is the input file containing tweets (unprocessed) from Twitter from a particular user
- OUTPUT is the output file (*.twt) where each tweet is parsed, tokenized and tagged

e.g. 
```python justinbieber justinbieber.twt```



2. Feature extraction
-------------------------------------------------------------------------------
buildarff.py takes .twt files to build an ARFF datafile. The produced ARFF datafile gathers feature information that will be used for the classification of tweets. 

The features computed for each .twt files are the number of
- first person pronouns
- second person pronouns
- third person pronouns
- coordinating conjunctions
- past-tense verbs
- future-tense verbs
- commas
- colons and semi-colons
- dashes
- parentheses
- common nouns
- proper nouns
- adverbs
- wh-words
- slang
- all-caps

as well as the average length of sentences for a tweet, the average length of tokens, and the number of sentences in a tweet.

The WEKA machine learning package will be used to classify tweets given the .arff files.


To run buildarff.py, from the terminal, type:
```python buildarff.py -X CLASS:FILE CLASS:FILE+FILE+FILE ... OUTPUT```

where ...
- X denotes the number of tweets to read; exclude this if you wish to read all the tweets from each FILE
- CLASS denotes the class (optional, else takes the file name)
- FILE is the parsed, tokenized and tagged file (.twt) produced from twtt.py; if there is more than one file for a given class, this is denoted by a + in between each file
- OUTPUT the generated arff file (*.arff)

e.g. ```python buildarff.py pop:justinbeiber.twt+katyperry.twt+ladygaga.twt news:cnn.twt+bbcnews.twt+nytimes.twt POPvsNEWS.arff```
