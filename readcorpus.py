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
		mult = 1
	else:
		mult = .5
	
	scores[x] = round(mult * weights[x])
	
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

	scores[x] = round(mult * weights[x])
	
	# IPS
	x = "ips"
	val = len(record[x]) if record[x] else 0
	weights[x] = 10
	scores[x] = 0
	print x + ": " + str(val)

	if (val == 0):
		mult = 0
	else:
		mult = .5

	scores[x] = round(mult * weights[x])
	
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

	scores[x] = round(mult * weights[x])

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

	scores[x] = round(mult * weights[x])
	
	# QUERY
	x = "query"
	val = (int(str(record[x]).count("="))) if record[x] else None
	weights[x] = 10
	scores[x] = 0
	print x + ": " + str(val)

	if ((val == None) or (val <= 3)):
		mult = .5
	else:
		mult = .25

	scores[x] = round(mult * weights[x])
	
	# NUMBER OF DOMAIN TOKENS
	x = "num_domain_tokens"
	val = record[x]
	weights[x] = 5
	scores[x] = 0
	print x + ": " + str(val)

	if (val <= 4):
		mult = .5
	else:
		mult = .3

	scores[x] = round(mult * weights[x])

	# HOST CHARACTERISTICS
	x = "host"
	val = record[x]
	weights[x] = 10
	scores[x] = 0
	print x + ": " + str(val)

	mult = .5

	# if host contains "-"
	if val.count("-") >= 1:
		mult -= .1

	# if .com is in the middle of the host
	if val.count(".com.") >= 1:
		mult -= .1
	
	# if host is exceedingly long
	if len(val) > 15:
		mult -= .1
	if len (val) > 23:
		mult -= .1
	if len(val) > 30:
		mult -= .1
		
	# if host is significantly longer than registered domain
	if (len(val) - len(record["registered_domain"]) > 10):
		mult -= .1
	if (len(val) - len(record["registered_domain"]) > 20):
		mult -= .1
		
	if mult < 0:
		mult = 0

	scores[x] = round(mult * weights[x])
	
	# NUMBER OF PATH TOKENS
	x = "num_path_tokens"
	val = record[x]
	weights[x] = 5
	scores[x] = 0
	print x + ": " + str(val)

	if (val <= 2):
		mult = .5
	else:
		mult = .2

	scores[x] = round(mult * weights[x])	

	# PATH CHARACTERISTICS
	x = "path"
	val = record[x]
	weights[x] = 10
	scores[x] = 0
	print x + ": " + str(val)

	mult = .5

	# if path contains "//"
	if val.count("//") >= 1:
		mult -= .1

	# if path contains ".com"
	if val.count(".com") >= 1:
		mult -= .1

	# if path contains "." more than once or anywhere but in the final 5 chars
	if (val.count(".") >= 2) or (val.find(".") < (len(val) - 5)):
		mult -= .1
	
	# if path is exceedingly long
	if len(val) > 15:
		mult -= .1
	if len (val) > 23:
		mult -= .1
	if len(val) > 30:
		mult -= .1
		
	if mult < 0:
		mult = 0

	scores[x] = round(mult * weights[x])

	# PORT
	x = "port"
	val = record[x]
	weights[x] = 5
	scores[x] = 0
	print x + ": " + str(val)

	if ((val != 80) or (val != 443)):
		mult = 0
	else:
		mult = .5

	scores[x] = round(mult * weights[x])

	# KEYWORD COMBINATIONS
	x = "url"
	val = record[x]
	weights[x] = 5
	scores[x] = 0
	print x + ": " + str(val)

	keywords = ("apple", "google", "paypal", "ebay", "yahoo", "coinbase", "amazon", "microsoft")
	mult = .5
	
	for key in keywords:
		if (val.count(key) >= 1):

			#if keyword exists in URL but has no alexa rating
			if not record["alexa_rank"]:
				mult -= .1
			
			#if keyword exists in URL but domain is young
			if (record["domain_age_days"] <= 1000):
				mult -= .1
			
			#if keyword exists in path
			if record["path"]:
				if (record["path"].count(key) >= 1):
					mult -= .1
					
			#if keyword exists in query
			if record["query"]:
				if (record["query"].count(key) >= 1):
					mult -= .1
					
			#if "-"+keyword or keyword+"-" exists in URL:
			if (val.count("-" + key) >= 1) or (val.count(key + "-") >= 1):
				mult -= .1
			
	if mult < 0:
		mult = 0

	scores[x] = round(mult * weights[x])

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

