#!/usr/bin/env python
import re, argparse, sys
from time import mktime, strftime, strptime, gmtime
from datetime import datetime, timedelta
#import operator, fileinput
#from collections import Counter
#from operator import itemgetter
#from itertools import groupby, starmap

#### Argument/other configuration
parser = argparse.ArgumentParser(description='Log parser - For internal testing purposes only (for now)')

parser.add_argument("log_file",
                        metavar="<log_file>",
#                        type=argparse.FileType('r'),
#                        default=sys.stdin,
                        help='Log file for parsing')
parser.add_argument('-o',
                        '--out',
                        metavar='<file>',
#                        nargs='?',
#                        type=argparse.FileType('w'),
#                        default=sys.stdout,
                        help='Output results to <file>')
parser.add_argument('-s',
                        '--start',
                        metavar="NUM",
                        help='Line to begin parsing (integer) - NOT IMPLEMENTED',
                        required=False)
parser.add_argument('-e',
                        '--end',
                        metavar="NUM",
                        help='Line to stop parsing; if not EOF (integer) - NOT IMPLEMENTED',
                        required=False)
parser.add_argument('-t',
                        '--keys',
                        help='Keywords to exclude. _____ delimiter - NOT IMPLEMENTED',
                        required=False)

args = parser.parse_args()




## REGEX PATTERNS FOUND IN 'pat_file'. STORED IN THE CURRENT WORKING DIRECTORY ##
## Add patterns that match *from string beginning* any lines to be returned    ##
## Commented patterns are ignored. Comments acceptable at EOL                  ##
#eg.
'''
$ cat pat_file
.*data.* # datatest
.*red.* # redtest
# .*testing.* # testing -disabled
'''

log = args.log_file
pretty = ("-" * 50)

def main(argv, input_file):
    pat_store = ()
    ## -o ##
    if args.out is not None:
        sys.stdout = open(args.out, "w")
    
    if args.log_file: #primary - "overview output"
        try:
            with open(input_file, 'r') as parse_target, open('pat_file', 'r') as pat_list: 
                for line in pat_list:
                    l = line[:line.index("#")].strip()
                    if not l.startswith("#"):
                        pat_store += (l,)
                patterns = re.compile('|'.join(['(%s)' % i for i in pat_store]))
                parse_out = parse(parse_target, patterns)
        except IOError as err:
            print("Operation failed: %s" % (err.strerror))
            sys.exit("""Error: Script execution terminated unexpectedly. 	
                \nPlease verify command integrity and dependent pattern file './pat_file' exists and is readable""")

    p = parse_out

    print("\nLog start: %s" % (p['log_start']))
    print("Log end:   %s" % (p['log_end']))
    print("Elapsed:   %d days %d hr %d min %d sec\n" %(p['elapsed']))
    print("Lines: %d" % (p['lc'])) 

    print("\n%s\nDebug information:\n%s\n" % (pretty, pretty))
    print("Irregular time gaps:")
    for gap, l in zip(p['time_gap'], p['time_lc']):
        print("Time gap: '%s seconds' on line: %s" % (gap, l))
    print("\nNSS calls: '%s' in the file: %s" % (p['nss_count'], log))
    print("PAM calls: '%s' in the file: %s\n" % (p['pam_count'], log))
    print("\n%s\nPattern detection:\n%s\n" % (pretty, pretty))
    print("Matching against patterns in ./pat_file: \n {%s}\n" % ("}, {".join(pat_store,)))
    print("Matches hidden: To display matches, please use the '-v' option.\n(Note: This may result in substantial output. Consider outputting results to a file via '-o')")
    for l, m in zip(p['m_lc'], p['matches']):
    #    print("%-*s %s" % (2, l, m))
        pass


def parse(parse_target, patterns): 
    reg = Re()
    nss_count, pam_count, i, x = (0, 0, 0, 0)
    time_chk = re.compile(r'^([A-Za-z]{3} [0-9]{2} [0-9]{2}[:]?[0-9:]+.*)$')
    times, time_gap, time_lc, matches, m_lc = ([], [], [], [], [])
    for line_count, line in enumerate(parse_target, 1):
        timestamp = line.strip()[0:15]
        try:
            reg.match(time_chk, line)
            times += (mktime(strptime(timestamp, "%b %d %H:%M:%S")), )
            last_time = times[-1]
            gap = (last_time - x)
            if i == 0: #first log entry
                log_start = time_calc(i, timestamp, times) #yank timestamp as "Log start"
            else:
                if x == last_time:
                    #print("equals %s" % (timestamp))
                    pass
                elif x < last_time and gap > 60:
                    time_gap.append(int(gap))
                    time_lc.append(line_count)
                x = last_time
            i += 1
        except:
            timestamp = None
        ## Primary matching from patterns contained in patterns tuple ##
        if reg.match(patterns, line):
            m_lc.append(line_count)
            matches.append(reg.m.group(0))
            ## Fringe-case pattern matching / occurrence count - Currently demo for NSS/PAM count logic ##
            if 'data' in reg.m.group(0):
                nss_count += 1
            if 'red'  in reg.m.group(0):
                pam_count += 1
    log_end = time_calc(i, timestamp, times)
    elapsed = (log_end[1].day-1, log_end[1].hour, log_end[1].minute, log_end[1].second)
    parse_out = {'time_gap':time_gap, 'time_lc':time_lc, 'elapsed':elapsed, \
                    'nss_count':nss_count, 'pam_count':pam_count, 'm_lc':m_lc, 'lc':line_count, \
                    'matches':matches, 'log_start':log_start, 'log_end':log_end[0]}

    return parse_out
    



        
#### Supplemental

class Re(object):
    def __init__(self):
        self.m = None
    def match(self,pattern,line):
        self.m = pattern.match(line)
        return self.m

def time_calc(i, timestamp, times):
    if i == 0: #first line
        times += (mktime(strptime(timestamp, "%b %d %H:%M:%S")), )
        return timestamp
    elif i != 0:
        try:
            times, timestamp
            times += (mktime(strptime(timestamp, "%b %d %H:%M:%S")), )
            duration = timedelta(seconds=(times[-1]-times[0]))
            d = datetime(1,1,1) + duration
            return timestamp, d
        except:
            pass

######################### testing / not implemented

def part(fileinput, chunk=512):
    while True:
        result = fileinput.read(chunk)
        if not result:
            break
        yield result

def string_match(sm, lc):
    for i, m in enumerate(sm): 
        #m = m.rstrip("\n")
        lc += 1
        print(lc, m)
    
    
def start():
    pass

def end():
    pass


def adinfo_support(): # still testing - not invoked
    if "adinfo_support" in str(args.log_file):
         print (args.log_file)
        #do some special stuff for adinfo_support (aesthetic env details)
    pass






if __name__ == "__main__":
    main(sys.argv[1:], log)


## DEBUG ##
print ("\n\n########### debugging\n") 
print ("args passed: %s" % (sys.argv))
print ("\n-s: %s" % args.start )
print ("-e: %s" % args.end )
print (args)
###########
