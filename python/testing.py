#!/usr/bin/env python

import re
from collections import defaultdict

FILE = "adinfo_support.txt"
for line in pat_list:
    if "#" in line: l = line[:line.index("#")].strip()
    else:           l = line.strip()
    if not l.startswith("#") and len(l) != 0: vs.pat_store += (l,)
patterns  = re.compile( '|'.join( ['(%s)' % i for i in vs.pat_store] ) )

import time, sys
if sys.platform == "win32":
    timer = time.clock
else:
    timer = time.time

t0, t1 = timer(), time.clock()

pat = re.compile(r".*data.* ")

search = pat.search

# map
matches = (search(line) for line in open(FILE, "r") if "data" in line)
mapp    = (match.group(0) for match in matches if match)

# reduce
count = defaultdict(int)
for page in mapp:
    count[page] +=1

for key in sorted(count, key=count.get)[:10]:
    pass # print "%40s = %s" % (key, count[key])

print timer() - t0, time.clock() - t1

# sanity check
for key in sorted(count, key=count.get)[-10:]:
    print "%40s = %s" % (key, count[key])
