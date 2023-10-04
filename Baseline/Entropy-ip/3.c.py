#!/usr/bin/env python
#
# Generates reduced IPv6 addresses out of an Entropy/IP model
#
# Note that this code is probably not the fastest possible. For larger tasks it might
# be reasonable to optimize it first, or use a different Bayes Net technique.
#
# Mind the different terminology vs. the paper.
# Runs in python2. Requires toposort (https://pypi.python.org/pypi/toposort)
#
# Copyright (c) 2015-2016 Akamai Technologies, Inc.
# See file "LICENSE" for licensing information.
# Author: Pawel Foremski
#

import sys,os
import argparse
import toposort
import random
from Alias_Prefix import *
# p = argparse.ArgumentParser(description='Entropy/IP: generate reduced IPv6 addrs')
# p.add_argument('cpd', help='file with the Bayes net model (output a4-bayes.sh)')
# p.add_argument('-n', type=int, default=10, help='number of IPs to generate')
# args = p.parse_args()

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def read_segments(src):
	segments = []
	sname = None
	sbits = []
	scodes = []

	for line in src:
		d = line.split()
		if line[0].isalpha():
			# new segment - save old first
			if sname: segments.append({"name": sname, "start": sbits[0], "stop": sbits[1], "codes": scodes})
			sname = d[0][:-1]
			sbits = [int(x) for x in d[2].split('-')]
			scodes = []
		elif line[0] == ' ':
			scodes.append(d[0])
		elif line[0] == '*':
			r = [int(x,16) for x in d[1].split('-')]
			scodes.append((r[0], r[1]))
		else: raise Exception("parse error: " + line)

	segments.append({"name": sname, "start": sbits[0], "stop": sbits[1], "codes": scodes})
	return segments

def decode(val, s):
	
	vlen = (s["stop"] - s["start"]) / 4
	C = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", \
	     "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", \
	     "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

	# decode
	if letters:
		code = C.index(val)
	else:
		code = int(val) - 1
	if code >= len(s["codes"]): return "?" * vlen

	# just static value?
	val = s["codes"][code]
	if type(val) == str: return val

	# draw from range of values
	# FIXME: to be precise, we would have to avoid drawing the value below from any of the ranges
	# defined in previous segment values; that is, if any of the segment values with lower code
	# defines a range, we should remove it from the random choice below; anyway, we assume the error
	# introduced by this simplified, inaccurate procedure is acceptable for our current applications
	num = random.randint(val[0], val[1])
	fmt1 = "%0" + str(vlen) + "x"
	return fmt1 % num




# prefix_num = 464
# prefix_num = 449
prefix_num = 1

# num = [100,1000,5000,10000]
num = [5000]
budgets = [prefix_num*i for i in num]
file = '/home/chengdaguo/ipv6/Baseline/Entropy-ip/dataset3/'


cpd = file+'cpd'
analysis =  file+'analysis'

letters = False
colons = True
debug = False


for budget in budgets:

	custom_file = file+'{}/'.format(budget)
	reduced_ipv6 = custom_file+'reduced_ipv6.txt'
	ipv6_output = custom_file+'ipv6.txt'
	makedirs(custom_file)
	n = int(budget*1.1)

	## c1: generate reduced IPv6 addresses
	# read CPDs
	CPD = eval(open(cpd).read())

	# topological sort of graph dependencies
	order = toposort.toposort_flatten({k:set(v['pars']) for k,v in CPD.iteritems()})
	print ("# " + ", ".join(sorted(order)))

	# open output file
	# os.makedirs(os.path.dirname(output))
	f = open(reduced_ipv6, 'w')
	# generate!
	i = 0
	while n <= 0 or i < n:
		i += 1
		chosen = {}
		vals = {}

		for V in order:
			vertex = CPD[V]

			# query the CPD wrt evidence
			query = tuple([chosen[P] for P in vertex['pars']])
			if query in vertex['cpds']:
				pd = vertex['cpds'][query]
			else:
				pd = {None: vertex['cpds'][None]}

			# take random selection
			cprob = random.random()
			ks = set(range(len(vertex['vals'])))
			for k,prob in pd.iteritems():
				if k == None: continue
				cprob -= prob
				if cprob <= 0: break
				else: ks.remove(k)
			else:
				# choose randomly from not specified so far
				if len(ks) > 0:
					k = random.choice(list(ks))
				else:
					k = random.choice(range(len(vertex['vals'])))

			# translate and store
			vals[V] = vertex['vals'][k]
			chosen[V] = k

		# print (",".join([vals[k] for k in sorted(vals.keys())]))
		f.write(",".join([vals[k] for k in sorted(vals.keys())]) + '\n')

	######
	# c2: generate  IPv6 addresses
	segments = read_segments(open(analysis))


	# os.makedirs(os.path.dirname(output),exist_ok=True)
	f = open(ipv6_output, 'w')

	for line in open(reduced_ipv6):
		if line[0] == '#': continue
		codes = []

		if letters:
			vals = line.strip()
		else:
			vals = line.strip().split(',')

		for val,segment in zip(vals, segments):
			if debug:
				codes.append("%s%s=%s\t" % (segment["name"], val, decode(val, segment)))
			else:
				codes.append(decode(val, segment))

		full = "".join(codes)
		if colons and not debug:
			# print (":".join([full[x:x+4] for x in range(0, 32, 4)]))
			f.write(":".join([full[x:x+4] for x in range(0, 32, 4)]) + '\n')
		else:
			# print (full)
			f.write(full + '\n')






	origin_samples = open(ipv6_output).readlines()

	# add_samples = open(output+'/ipv6_1.txt').readlines()
	# origin_samples += add_samples

	origin_samples = set(origin_samples)
	print(len(origin_samples))
	if len(origin_samples) >= budget:
		origin_samples = random.sample(origin_samples,budget)
	origin_samples = [get_entire_ipv6(x.strip()) for x in origin_samples]

	file_updata = custom_file+'ipv6_budget.txt'
	f1 = open(file_updata,'w')
	f1.write('\n'.join(origin_samples))
	f1.close()


	scan(custom_file,file_updata)
