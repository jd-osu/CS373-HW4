#!/usr/bin/python

import json, sys, getopt, os
import random

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

	rec = random.randint(0, (len(urldata)-1))

	print urldata[rec]
	
	record = urldata[rec]
	
	scores = dict()
	weights = dict()
	
	# TLD
	x = "tld"
	val = record[x]
	weights[x] = 10
	scores[x] = 0
	print x + ": " + val

	if (val == "com") or (val == "org") or (val == "net") or (val == "edu") or (val == "gov"):
		scores[x] = 1 * weights[x]
	
	# AGE
	x = "domain_age_days"
	val = int(record[x])
	weights[x] = 10
	scores[x] = 0
	print x + ": " + str(val)

	if (val < 10):
		mult = 0
	elif (val < 20):
		mult = .1
	elif (val < 30):
		mult = .2
	elif (val < 90):
		mult = .3
	elif (val < 180):
		mult = .4
	elif (val < 360):
		mult = .5
	elif (val < 500):
		mult = .75
	else:
		mult = 1

	scores[x] = mult * weights[x]

	# IPS
	x = "ips"
	val = len(record[x])
	weights[x] = 10
	scores[x] = 0
	print x + ": " + str(val)

	if (val == 0):
		mult = 0
	else:
		mult = .5

	scores[x] = mult * weights[x]
	
	# ALEXA
	x = "alexa_rank"
	val = int(record[x]) if record[x] else None
	weights[x] = 10
	scores[x] = 0
	print x + ": " + str(val)

	if (val == None):
		mult = 0
	else:
		mult = float(float(1000000 - val) / float(1000000))

	scores[x] = mult * weights[x]

	# EXTENSION
	x = "file_extension"
	val = str(record[x]) if record[x] else None
	weights[x] = 10
	scores[x] = 0
	print x + ": " + str(val)

	if ((val == None) or (val != "exe")):
		mult = .5
	else:
		mult = 0

	scores[x] = mult * weights[x]
	
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
	
	num_val = float(float(score) / float(weight))
	
	print "final score: %4f / %4u" % (score, weight)
	print "num val: %11f" % (num_val)
	
	# evaluation
	eval_pt = .5
	if (num_val < eval_pt):
		mal = 1
	else:
		mal = 0
		
	print "malicious: " + str(mal)
	print "actual: " + str(record["malicious_url"])

	#for record in urldata:
 
		# Do something with the URL record data...
		#print (record["url"])
		#results.write(record["url"] + "\n")

	corpus.close()
	results.close()

if __name__ == "__main__":
	main(sys.argv[1:])

