#!/usr/bin/env python
import re, argparse, sys #re for regex, argparse for options, sys for argv
#import operator  #may not need. holding as a reference though


# options designation (replaced getopt). 'log_file' is required positional
parser = argparse.ArgumentParser(description='Log parser - For internal testing purposes only (for now)')
parser.add_argument("log_file",metavar="<log_file>",type=argparse.FileType('r'),default=sys.stdin,help='Log file for parsing')
parser.add_argument('-s','--start',metavar="NUM",help='Line to begin parsing (integer) - NOT IMPLEMENTED',required=False)
#parser.add_argument('-e','--end',metavar="NUM",help='Line to stop parsing; if not EOF (integer)',required=False)
#parser.add_argument('-t','--keys',help='Keywords to exclude. _____ delimiter - NOT IMPLEMENTED',required=False)
args = parser.parse_args()

''' not implemented

start_line = 1
#end_line =

if args.start: print("Begin parsing at line: %s " % args.start)
else: print("Begin parsing at line: 1")
if args.end: print("End parsing at line: %s " % args.end)
else: print("End parsing at EOF")
'''
nss_count = 0
def main(argv):
    while args.log_file: #while value for log_file is passed
        line = args.log_file.readline() #readline and assign to 'line' variable
        expr = '.*data.*'
        expr_comp = re.compile('(.*data.*)')
        expr_strings = ['.*data.*', 
                        '.*red.*',
                        '.*NSSGet.*']
        expr_counts = ['.*data.*']
        
        #regex = expr_strings[0 += 1]
        #if "adinfo_support" in str(args.log_file):
            # print (args.log_file)
            #do some special stuff for adinfo_support (environmental prettiness)
        for regex in expr_strings:
            for m in re.finditer(regex, str(line.rstrip("\n")), re.S):
                print (m.group())
           # print (m)
                #if expr_strings[0]:
                 #   global nss_count
                #    nss_count += 1
               # print ("NSS Calls: %s " % nss_count)
       #     return {m.group()}


        if not line: break #break for EOF


def start():
    pass

def end():
    pass

def call_count():
    pass

def adinfo_support():
    pass


if __name__ == "__main__":
    main(sys.argv[1:])


## DEBUG ##
print ("\n\n\nStart line: %s" % args.start )
print (args)
###########
