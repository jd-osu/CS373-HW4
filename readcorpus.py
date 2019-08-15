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
	
	# TLD
	tld = record["tld"]
	scores["tld"] = 5
	print "tld: " + tld

	if (tld == "com") or (tld == "org") or (tld == "net") or (tld == "edu") or (tld == "gov"):
		tld_score += 1
		
	#print all subscores
	for subscore in scores:
		print "subscore: " + subscore
	
	
	
	# combine all scores
	#total = 0
	#n = len(scores)
	#for subscore in scores:
	#	total += subscore
	
	#final_score = 

	#for record in urldata:
 
		# Do something with the URL record data...
		#print (record["url"])
		#results.write(record["url"] + "\n")

	corpus.close()
	results.close()

if __name__ == "__main__":
	main(sys.argv[1:])

