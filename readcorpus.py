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
	
	# TLD
	tld = record["tld"]
	print "tld: " + tld

	#for record in urldata:
 
		# Do something with the URL record data...
		#print (record["url"])
		#results.write(record["url"] + "\n")

	corpus.close()
	results.close()

if __name__ == "__main__":
	main(sys.argv[1:])

