#=====================================================================
#  File:      MakeLex.py
#  Summary:   create a binary lexicon file.
#
#---------------------------------------------------------------------
#  Original Copyright (C) Mark Watson.  All rights reserved.
#  Python port by Jason Wiener (http://www.jasonwiener.com)
#
#THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
#KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
#PARTICULAR PURPOSE.
#=====================================================================

import pickle
#need to declare the has in the topmost of the class
d = {}

def returnkeyval(j,line):
	try:
		terms = line.split()
		#print "t>",terms
		for i in range(len(terms)):
			#break after the first symbol
			if i == 1:
				break
			d[terms[i]] = terms[i+1]
			#print j,">>(", len(terms), ")", terms[i], ":", terms[i+1]

		#print "::",line, "::"
		return d
		
	except Exception, inst:
		print type(inst)
		print inst.args


try:
	f = open('lexicon.txt', 'r')
	i = 0
	for line in f:
		#if i == 100:
		#	break
		returnkeyval(i,line)
		i = i + 1
	f.close()
	
	print "dictionary is ", len(d)
	#for k,v in d.iteritems():
	#	print k, v
		
	print "pickling the dictionary"
	pkl = open('pickledlexicon', 'w')
	pickle.dump(d, pkl)
	pkl.close()

except Exception, inst:
	print type(inst)
	print inst.args
