#!/usr/bin/env python
import re, argparse, sys #re for regex, argparse for options, sys for argv
#import operator  #may not need. holding as a reference though

def usage():
    print("USAGE RESULT PLACEHOLDER")

# options designation (replaced getopt). 'log_file' is required positional
parser = argparse.ArgumentParser(description='Log parser - INTERNAL ONLY')
parser.add_argument("log_file",type=argparse.FileType('r'),default=sys.stdin,help='Log file for parsing')
parser.add_argument('-s','--start',help='Line to begin parsing',required=False)
args = parser.parse_args()


# -s (need to address --start=x if warranted)
if args.start:
    print("start specified!!\n")



def main(argv):
    while args.log_file: #while value for log_file is passed
        line = args.log_file.readline() #readline and assign to 'line' variable
        expr = '.*data.*'
        expr_comp = re.compile('(.*data.*)')
        
        for m in re.finditer(expr, line.rstrip("\n"), re.S):
            print (m.group())
       #     return {m.group()}


        if not line: break #break for EOF

## broke - keeping as reference though
       # for i in line:
       #     m = expr_comp.match(line)
       #     if m:
       #         print (m.group())


def parse(line2):
    fmt = ('^date?')
    m = re.search(fmt, line2)


if __name__ == "__main__":
    main(sys.argv[1:])


## DEBUG ##
print ("\n\n\nStart line: %s" % args.start )
print (args)
###########
