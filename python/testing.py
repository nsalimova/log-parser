#!/usr/bin/env python

import re, mmap, contextlib
from collections import defaultdict, namedtuple
import time, sys

#i = 0
#def check(x):
#    global i
#    i = i + 1

## not fully vetted
#def read_in_chunks(file_object, chunk_size=1024*1024):
#    """Lazy function (generator) to read a file piece by piece.
#    Default chunk size: 1k."""
#    while True:
#        data = file_object.read(chunk_size)
#        if not data:
#            break
#        yield data

pat_store = ()
idx,opened_fd,closed_fd,kw_match= ( [], [], [], [] )
sshd_lc, sshd_matches = [], []
afd = {}



# ================ testing

months = dict(jan=1,feb=2,mar=3,apr=4,may=5,jun=6,jul=7,aug=8,sep=9,oct=10,nov=11,dec=12)

def convert_time2(string, year=None):
    if year is None: year = time.gmtime()[0]
    mon,d,t = string.split(" ")
    h,m,s   = t.split(":")
    mon     = months[mon.lower()]
    tt      = [year, mon,d,h,m,s,0,0,0]
    tt      = tuple([int(v) for v in tt])
    ts      = int(time.mktime(tt))
    tt      = time.gmtime(ts)
    return (ts,tt,string)

def time_calc( i, timestamp, times ):

    if ( i == 0 ): #first line

        #times                   += ( mktime( strptime( timestamp, "%b %d %H:%M:%S" ) ), )
        times                   += ( mktime(convert_time2(timestamp)[1]), )

        return timestamp

    elif ( i != 0 ):
        try:
            times, timestamp

            #times               += ( mktime( strptime( timestamp, "%b %d %H:%M:%S" ) ), )
            times                   += ( mktime(convert_time2(timestamp)[1]), )
            duration            = timedelta( seconds=( times[-1]-times[0] ) )
            d                   = datetime( 1,1,1 ) + duration

            return ( timestamp, d )
        except:
            pass

# =======================


with open('adinfo_support.txt', 'r+') as f, open('pat_file', 'r') as pat_list:
    for line in pat_list:
        if "#" in line: l = line[:line.index("#")].strip()
        else:           l = line.strip()
        if not l.startswith("#") and len(l) != 0: pat_store += (l,)
    patterns  = re.compile( ('|'.join( ['(%s)' % i for i in pat_store] )), re.MULTILINE )
    pattern = re.compile(r'(.*DEBUG.*sshd.*Authentication for user \'.*|.*DEBUG.*dzdo.*Authentication for user \'.*|.*DEBUG <main> daemon.ipcserver Accepted new lrpc2 client on.*|.*DEBUG <main> daemon.ipcserver lrpc client disconnected.*)',
                     re.DOTALL | re.IGNORECASE | re.MULTILINE)





# ~1.5sec
    matches = []
    times = []
    time_gap, time_lc = [], []
    x = 0
    i = 0
    for (line_count, line) in enumerate(f):
        if line.strip(): timestamp = line.strip()[0:15] 
        try:
            times += ( mktime(convert_time2(timestamp)[1]), )
            last_time = times[-1]
            gap = (last_time - x)
            if ( i == 0 ):
                log_start = time_calc( i, timestamp, times )
            else:
                if ( x == last_time ):
                    pass
                elif ( x < last_time and gap > 4 ):
                    time_gap.append( int(gap) )
                    time_lc.append( line_count )
                x = last_time
            i += 1
     
            
        except:
            timestamp = None


        if ( line.find("Accepted new lrpc2 client on <fd:") ) >= 0:
            fd_open         = line.split(" ")[13].lstrip("<fd:").rstrip(">'")
            opened_fd.append( fd_open )
            afd[fd_open] = "OPEN"

        if ( line.find("lrpc client disconnected normally ") ) >= 0:
            fd_close    = line.split(" ")[12].lstrip("<fd:").rstrip(">\n'")
            afd[fd_close] = "CLOSE"


        if "adclient" in line:
            line = line.split("adclient")
            #fields = [line[i] for i in range(5, 20)] 
            fields = line[1]
            #print(fields)
            if re.match(patterns, fields):
                m = line
                matches.append( m )
                pass

## ~1.8sec
#    groups = (patterns.match(line) for line in f)
#    tuples = (g.groups() for g in groups if g)
#
#    for t in tuples:
#        #print(t)
#        pass

## ~1.8sec
#    for line in f:
#        fields = line.split('\t')
#        #mapp = list(map(check,fields))
#        mapp = map(lambda z: z * 2, fields)
#        for r in mapp:
#            if re.match(patterns, r):
#                pass 

## ~2.1sec
#
#    matches = []
#    #try:
#    for l in f:
#        if re.match(patterns, l):
#            m = l
#            matches.append( m )
#            pass
#    #except:
#    #    pass


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
