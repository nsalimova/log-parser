#!/usr/bin/env python
import re, argparse, sys, fileinput #re for regex, argparse for options, sys for argv
#import operator  #may not need. holding as a reference though


# options designation (replaced getopt). 'log_file' is required positional
parser = argparse.ArgumentParser(description='Log parser - For internal testing purposes only (for now)')

parser.add_argument("log_file",
                        metavar="<log_file>",
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='Log file for parsing')
parser.add_argument('-s',
                        '--start',
                        metavar="NUM",
                        help='Line to begin parsing (integer) - NOT IMPLEMENTED',
                        required=False)
parser.add_argument('-e',
                        '--end',
                        metavar="NUM",
                        help='Line to stop parsing; if not EOF (integer)',
                        required=False)
parser.add_argument('-t',
                        '--keys',
                        help='Keywords to exclude. _____ delimiter - NOT IMPLEMENTED',
                        required=False)

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
expr = '.*data.*'
expr_comp = re.compile('(.*data.*)')
expr_red_comp = re.compile('(.*red.*)')
expr_strings = ['.*data.*', 
                '.*red.*',
                '.*NSSGet.*']
expr_counts = ['.*data.*']
has_run = False
def main(argv):
#    for line in fileinput.input(files=args.log_file if len(args.log_file) > 0 else ('-', )):
    while args.log_file: 
        line = args.log_file.readline()
        pat1 = re.match(expr_comp, line)
        global has_run
        if not has_run:
            if pat1:
                with open(args.log_file.name) as f:
                    num_lines = len(f.readline())
                    print (num_lines)
            has_run = True
                #break
        for pat_list in expr_strings:
            #finditer = (re.findall(pat_list, str(line.rstrip("\n")), re.S))
            finditer = (re.findall(pat_list, line, re.S))
            for i, m in enumerate(finditer):
                m = m.rstrip("\n")
                if re.match(expr_comp, m):
        #            print(m)
                    pass
                if re.match(expr_red_comp, m):
                    print(m)
                    pass
        #call_count()
        


#pat1 = re.search('.*data.*', line) #another option 
        
        #if "adinfo_support" in str(args.log_file):
            # print (args.log_file)
            #do some special stuff for adinfo_support (environmental prettiness)

##        for regex in expr_strings:
##            for m in re.finditer(regex, str(line.rstrip("\n")), re.S):
##                print (m.group())




        if not line: break #break for EOF


def start():
    pass

def end():
    pass

def call_count():
    line = args.log_file.readline()
    pat1 = re.match(expr_comp, line)
    called = 0
    while True:
        if pat1:
            called += 1
            with open(args.log_file.name) as f:
                num_lines = len(f.readline())
                print (num_lines)
            break
        else: 
            called = 0
            break
        
  #  for field, values in .items():
  #  print(field, values)
    
def adinfo_support():
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
    #call_count()


## DEBUG ##
print ("\n\n\nStart line: %s" % args.start )
print (args)
###########
