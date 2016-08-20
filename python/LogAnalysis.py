#!/usr/bin/env python
import re, argparse, sys #re for regex, argparse for options, sys for argv
#import operator  #may not need. holding as a reference though


# options designation (replaced getopt). 'log_file' is required positional
parser = argparse.ArgumentParser(description='Log parser - For internal testing purposes only (for now)')
parser.add_argument("log_file",metavar="<log_file>",type=argparse.FileType('r'),default=sys.stdin,help='Log file for parsing')
parser.add_argument('-s','--start',metavar="#",help='Line to begin parsing (integer) - NOT IMPLEMENTED',required=False)
#parser.add_argument('-e','--end',metavar="#",help='Line to stop parsing; if not EOF (integer)',required=False)
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



def main(argv):
    while args.log_file: #while value for log_file is passed
        line = args.log_file.readline() #readline and assign to 'line' variable
        expr = '.*data.*'
        expr_comp = re.compile('(.*data.*)')
        
        for m in re.finditer(expr, str(line.rstrip("\n")), re.S):
            print (m.group())
       #     return {m.group()}


        if not line: break #break for EOF

## broke - keeping as reference though
       # for i in line:
       #     m = expr_comp.match(line)
       #     if m:
       #         print (m.group())

def start():
    pass

def end():
    pass

def call_count():
    pass


if __name__ == "__main__":
    main(sys.argv[1:])


## DEBUG ##
print ("\n\n\nStart line: %s" % args.start )
print (args)
###########
