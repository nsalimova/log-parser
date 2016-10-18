#!/usr/bin/env python
import re, argparse, sys #re for regex, argparse for options, sys for argv
#import operator, fileinput
from time import mktime, strftime, strptime, gmtime

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
                print("Matching against patterns in ./pat_file: %s\n" % (pat_store,))
                patterns = re.compile('|'.join(['(%s)' % i for i in pat_store]))
                parse(parse_target, patterns)
        except IOError as err:
            print("Operation failed: %s" % (err.strerror))
            sys.exit("Error: Script execution terminated unexpectedly. 	\nPlease verify command integrity and dependent pattern file './pat_file' exists and is readable")



def parse(parse_target, patterns): 
    nss_count, pam_count = (0, 0)
    times = []
    i = 0
    reg = Reg()
    time_chk = re.compile(r'^([A-Za-z]{3} [0-9]{2} [0-9]{2}[:]?[0-9:]+.*)$')
    for line_count, line in enumerate(parse_target, 1):
        timestamp = line.strip()[0:15]
        if i == 0 and reg.match(time_chk, line): # first log entry, pull timestamp
            time_calc(i, timestamp, times)
            i += 1
            
        ## Primary matching from patterns contained in patterns tuple ##
        if reg.match(patterns, line):
            ## Fringe-case pattern matching - Currently demo for NSS/PAM count logic ##
            if 'data' in reg.last_match.group(0):
                nss_count += 1
            if 'red'  in reg.last_match.group(0):
                pam_count += 1
            #print(line_count, reg.last_match.group(0))

    time_calc(i, timestamp, times) # last log entry, pull timestamp
    print("NSS calls: '%s' in the file: %s" % (nss_count, log))
    print("PAM calls: '%s' in the file: %s" % (pam_count, log))
    

        
#### Supplemental

class Reg(object):
    def __init__(self):
        self.last_match = None
    def match(self,pattern,line):
        self.last_match = pattern.match(line)
        return self.last_match
    def search(self,pattern,line):
        self.last_match = pattern.search(line)
        return self.last_match

def time_calc(i, timestamp, times):
    if i == 0: 
        times += (mktime(strptime(timestamp, "%b %d %H:%M:%S")), )
        print("Log start: %s" % (timestamp))
    else:
        times += (mktime(strptime(timestamp, "%b %d %H:%M:%S")), )
        seconds = int(times[1]-times[0])
        minutes = int(seconds / 60)
        hours = int(minutes / 60)
#       elapsed = str(strftime("%d %H:%M:%S", gmtime(seconds))) #%d has min of 01 - <1day = wrong return
        print("Log end:   %s" % (timestamp))
        print("Elapsed time:\n  In hours:   %s\n  In minutes: %s\n  In seconds: %s \n" % (hours, minutes, seconds))



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
print (sys.argv)
print ("\n\n\nStart line: %s" % args.start )
print ("End line:   %s" % args.end )
print (args)
###########
