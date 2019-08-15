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
	x = "tld"
	val = record[x]
	weights[x] = 1
	scores[x] = 0
	print x + ": " + val

	if (val == "com") or (val == "org") or (val == "net") or (val == "edu") or (val == "gov"):
		scores[x] = 1 * weights[x]
	
	# AGE
	x = "domain_age_days"
	val = record[x]
	weights[x] = 10
	scores[x] = 0
	print x + ": " + val

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
		mult = 1

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
	
	num_val = score/weight
	
	print "final score: %4u / %4u" % (score, weight)
	print "num val: %11u" % (num_val)
	
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

