#!/usr/bin/env python

import re
from collections import defaultdict, namedtuple
import time, sys

i = 0
def check(x):
    global i
    i = i + 1

pat_store = ()

with open('adinfo_support.txt', 'r') as f, open('pat_file', 'r') as pat_list:
    for line in pat_list:
        if "#" in line: l = line[:line.index("#")].strip()
        else:           l = line.strip()
        if not l.startswith("#") and len(l) != 0: pat_store += (l,)
    patterns  = re.compile( '|'.join( ['(%s)' % i for i in pat_store] ) )

    
## ~1.8sec
#    for line in f:
#        fields = line.split('\t')
#        #mapp = list(map(check,fields))
#        mapp = map(lambda z: z * 2, fields)
#        for r in mapp:
#            if re.match(patterns, r):
#                pass 



# ~1.5sec
    matches = []
    for line in f:
        if "adclient" in line:
            line = line.split("adclient")
            #fields = [line[i] for i in range(5, 20)] 
            fields = line[1]
            #print(fields)
            if re.match(patterns, fields):
                m = line
                matches.append( m )
                pass




## 2+sec
#    search = patterns.search
#
#    # map
#    matches = (search(line) for line in f if "data" in line or "red" in line)
#    mapp    = (match.group(0) for match in matches if match)
#
#    # reduce
#    count = defaultdict(int)
#    for page in mapp:
#        count[page] +=1
#
#    #for key in sorted(count, key=count.get)[:10]:
#    #    pass # print "%40s = %s" % (key, count[key])
#
#
#    # sanity check
#    for key in sorted(count, key=count.get)[-10:]:
#        print ("%40s = %s" % (key, count[key]))
