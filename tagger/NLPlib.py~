#=====================================================================
#  File:      NLPlib.py
#  Summary:   part of speech tagger
#
#---------------------------------------------------------------------
#
#  Original Copyright (C) Mark Watson.  All rights reserved.
#  Python port by Jason Wiener (http://www.jasonwiener.com)
#
#THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
#KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
#PARTICULAR PURPOSE.
#=====================================================================

import pickle
import re
import sys

class NLPlib:
	lexHash = {}
	
	def __init__(self):
		if(len(self.lexHash) == 0):
			try:
				print "unpickle the dictionary"
				upkl = open('pickledlexicon', 'r')
				self.lexHash = pickle.load(upkl)
				upkl.close()
				print "Initialized lexHash from pickled data."
		
#				print "printing unpickled dictionary"
#				i = 0
#				for k,v in self.lexHash.iteritems():
#					if i == 100:
#						break
#					print k, ":", v
#					i = i+1
			
			except Exception, inst:
				print type(inst)
				print inst.args
	#finish - populatehash

	#start  - DEF: tokenize
	def tokenize(self,s):
		v = []
		reg = re.compile('(\S+)\s')
		m = reg.findall(s);
		
		#print m
		for m2 in m:
#			print m2
			if len(m2) > 0:
				if m2.endswith(";") or m2.endswith(",") or m2.endswith("?") or m2.endswith(")") or m2.endswith(":") or m2.endswith("."):
					v.append(m2[0:-1])
#					print "adding0: ",m2[0:-1]
				else:
					v.append(m2)
#					print "adding1: ",m2
#		print "\t",v
		return v
	#finish - DEF: tokenize

	#start  - DEF: tag
	def tag(self,words):
		ret = []
		#begin tagging
		for i in range(len(words)):
			ret.append("NN")		#the default entry
#			print "hash_key:",words[i]

			if self.lexHash.has_key(words[i]):
				ret[i] = self.lexHash[words[i]]
			else:
				if self.lexHash.has_key(words[i].lower()):
					ret[i] = self.lexHash[words[i].lower()]
		
		#apply transformational rules
		for i in range(len(words)):
			#rule 1 : DT, {VBD | VBP} --> DT, NN
			if i > 0 and ret[i-1] == "DT":
				if ret[i] == "VBD" or ret[i] == "VBP" or ret[i] == "VB":
					ret[i] = "NN"
					
			#rule 2: convert a noun to a number (CD) if "." appears in the word
			if ret[i].startswith("N"):
				if words[i].find(".") > -1:
					ret[i] = "CD"
			
			# rule 3: convert a noun to a past participle if ((string)words[i]) ends with "ed"
			if ret[i].startswith("N") and words[i].endswith("ed"):
				ret[i] = "VBN"

			# rule 4: convert any type to adverb if it ends in "ly"
			if words[i].endswith("ly"):
				ret[i] = "RB"
				
			# rule 5: convert a common noun (NN or NNS) to a adjective if it ends with "al"
			if ret[i].startswith("NN") and words[i].endswith("al"):
				ret[i] = "JJ"
				
			# rule 6: convert a noun to a verb if the preceeding work is "would"
			if i > 0 and ret[i].startswith("NN") and words[i - 1].lower() == "would":
				ret[i] = "VB"
			
			# rule 7: if a word has been categorized as a common noun and it ends with "s",
			# then set its type to plural common noun (NNS)
			if ret[i] == "NN" and words[i].endswith("s"):
				ret[i] = "NNS"
			
			# rule 8: convert a common noun to a present prticiple verb (i.e., a gerand)
			if ret[i].startswith("NN") and words[i].endswith("ing"):
				ret[i] = "VBG"
				
		return ret
	#finish - DEF: tag

print "beginning test"
#comment everything below when done testing
o = NLPlib()
s = "The mosquito bit the boy. "
s = "Tiger Woods finished the big tournament at par "
s = "The dog 's paw was bit. We blame the cat; is that fair? "
v = o.tokenize(s)
t = o.tag(v)
for i in range(len(v)):
	print v[i],"(",t[i],")"
