#!/usr/bin/python

import json, sys, getopt, os

def usage():
	print("Usage: %s --file=[filename]" % sys.argv[0])
	sys.exit()

def main(argv):

	file=''
 
	myopts, args = getopt.getopt(sys.argv[1:], "", ["file="])
 
	for o, a in myopts:
		if o in ('-f, --file'):
			file=a
		else:
			usage()

	if len(file) == 0:
		usage()
 
	corpus = open(file)
	urldata = json.load(corpus, encoding="latin1")

	results = open('results','w')

	print urldata[0]
	
	record = urldata[0]
	
	scores = dict()
	weights = dict()

	
	# TLD
	tld = record["tld"]
	weights["tld"] = 1
	scores["tld"] = 0
	print "tld: " + tld

	if (tld == "com") or (tld == "org") or (tld == "net") or (tld == "edu") or (tld == "gov"):
		scores["tld"] = 1 * weights["tld"]
		
	#print all subscores
	for sub in scores:
		print "scores[" + sub +"]: %4u / %4u" % (scores[sub], weights[sub])
	
	# combine all scores
	score = 0
	weight = 0
	
	n = len(scores)
	for sub in scores:
		score += scores[sub]
		weight += weights[sub]
	
	print "final score: %4u / %4u" % (score, weight)
	
	

	#for record in urldata:
 
		# Do something with the URL record data...
		#print (record["url"])
		#results.write(record["url"] + "\n")

	corpus.close()
	results.close()

if __name__ == "__main__":
	main(sys.argv[1:])

