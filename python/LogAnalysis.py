#!/usr/bin/env python
import re, argparse, sys, string, datetime #re for regex, argparse for options, sys for argv
#import operator, fileinput
from time import mktime, strftime, strptime, gmtime

####################################
#-- Argument/other configuration --#
####################################
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




expr_comp = re.compile(r"(.*data.*)", re.M)
expr_pam = re.compile(r"(.*red.*)", re.M)
log = args.log_file 

# Patterns for primary parsing logic
# All "relevant logs" should match a pattern in this tuple
expr_strings = ('.*data.*', 
                '.*red.*',
               # '.*CAPIValidate.*adagent.*',
                '.*example.*')

#pat_list = (l.rstrip(' #') for l in open("pat_file", 'r'))

#patterns = re.compile('|'.join(['(%s)' % i for i in expr_strings]))

####################################
#----- Primary logic / parser -----#
####################################
def main(argv, input_file):
    patterns = []
    ## -o ##
    if args.out is not None:
        outtofile(args.out)
    ########
    
    if args.log_file: #primary - "overview output"
        try:
            with open(input_file, 'r') as parse_target, open('pat_file', 'r') as pat_list: #maybe move this line to main()? then things below stay here? 
                print(pat_list)
                #patterns = re.compile('|'.join(['(%s)' % i for i in pat_list.rstrip(' #')]))
                for l in pat_list:
                    patterns += l.rstrip(' #\n')
                    print(patterns)
                parse(parse_target, patterns)
        except IOError as err:
            print("Operation failed: %s" % (err.strerror))
            sys.exit()

   ## Act on deeper requests ## - Unimplemented - Example
   ## May not be reasonable. We want to avoid opening the file multiple times. 
   ## The trick will be figuring out a clean way of passing args into parse() as an existing function.
   ## Perhaps this is where our "map" comes into play.
   # elif args.keys: 
   #     pass
   # elif "adinfo_support" in str(log): #not clean but checks for string in <log_file> arg name
   #     adinfo_support()
   # elif etc.. etc..
        


## Core parsing logic ##
def parse(parse_target, patterns): 
    nss_count, pam_count = (0, 0)
    times = []
    i = 0
    #for p in part(parse_target):  # parse by chunk - temporarily disabled in favor of line-by-line for now
    for line_count, line in enumerate(parse_target, 1):
        i += 1
        if i == 1: time_calc(i, line, times) #run on first line only

        ## Primary matching from patterns contained in patterns tuple ##
        if re.match(patterns, line):
            #print(line_count, line.rstrip('\n'))        
            pass
        ## Fringe-case pattern matching - Currently demo for NSS/PAM count logic ##
        if re.match(expr_comp, line): 
            nss_count += 1
#            print(line_count, line)
        if re.match(expr_pam, line):
            pam_count += 1
#            print(line_count, line)

#        for regex in patterns: 
#            finditer = (re.findall(regex, line, re.M))
        ## Iterate lines matching patterns provided in expr_strings[] ##
#            for match in finditer: 
#                call_count(match, line_count) 
    time_calc(i, line, times)
    print("NSS calls: '%s' in the file: %s" % (nss_count, log))
    print("PAM calls: '%s' in the file: %s" % (pam_count, log))
    #print(pat_list)
    #pat_list.close()


        
####################################
#----- Supplemental functions -----#
####################################


## Output to file designated with -o/--out ##
def outtofile(output_file):
    sys.stdout = open(output_file, "w")


## Count function for NSS/PAM calls ## -- function out of use. may re-use later. logic moved to parse()
def call_count(m, line_count):
    #global nss_count, pam_count
    if re.match(expr_comp, m): 
        nss_count += 1
#        print(line_count, m)
    if re.match(expr_pam, m):
        pam_count += 1
#        print(line_count, m
    return pam_count, nss_count


def time_calc(i, line, times):
    timestamp = line.strip()[0:15]
    if i == 1: 
        times += (mktime(strptime(timestamp, "%b %d %H:%M:%S")), )
        print("Starting time: %s" % (timestamp))
    else:
        times += (mktime(strptime(timestamp, "%b %d %H:%M:%S")), )
        seconds = int(times[1]-times[0])
        minutes = int(seconds / 60)
        hours = int(minutes / 60)
        #elapsed = str(strftime("%d %H:%M:%S", gmtime(seconds))) #in dev - %d has min of 01 so calc is off
        print("Ending time:   %s" % (timestamp))
        print("Elapsed time:\n  In hours: %s\n  In minutes: %s\n  In seconds: %s " % (hours, minutes, seconds))




######################### in development



## Parse by chunk 
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
    

class demo(object):
    pass
    
def start():
    pass

def end():
    pass


def adinfo_support(): # still testing - not invoked
    if "adinfo_support" in str(args.log_file):
         print (args.log_file)
        #do some special stuff for adinfo_support (environmental prettiness)
    pass


def test(): # misc testing - not currently invoked
    pass
    




if __name__ == "__main__":
    main(sys.argv[1:], log)
    


## DEBUG ##
print (sys.argv)
print ("\n\n\nStart line: %s" % args.start )
print ("End line:   %s" % args.end )
print (args)
###########
