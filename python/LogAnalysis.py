#!/usr/bin/env python
import re, argparse, sys #re for regex, argparse for options, sys for argv
#import operator, fileinput  

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

## Globals declaraion ##
nss_count = 0
expr = '.*data.*'
expr_comp = re.compile(r"(.*data.*)", re.MULTILINE)
expr_pam = re.compile(r"(.*red.*)", re.MULTILINE)
expr_nl = re.compile(r"\W+")
expr_strings = ['.*data.*', 
                '.*red.*',
                '.*NSSGet.*']
expr_counts = ['.*data.*']
log = args.log_file
canlog = args.log_file.name
prov_log = 2#open(args.log_file, 'r')
logtxt = 2#prov_log.read()
has_run = False
pam = 1
nss = 2
#line = args.log_file.readline()
########################


## Primary logic / parser ##
def main(argv):
    if args.start:          ## need to add clause for case where -s and -e are both specified
        call_count(pam)
    elif args.end:
        call_count(nss)
 
    with open(canlog) as f:
       # line = args.log_file.readline() 
#        global has_run 
#        nss_count = re.match(expr_comp, line)
#
#        if not has_run:
#            if nss_count:
#                with open(args.log_file.name) as f:
#                    num_lines = len(f.readline())
#                    print (num_lines)
#            has_run = True
                #break
        
        for l in f:
            for pat_list in expr_strings:
                finditer = (re.findall(pat_list, l, re.S))

                for i, m in enumerate(finditer):
                    m = m.rstrip("\n")
                    if re.match(expr_comp, m):
                        m1 = []
                        m1 += m
                        print(m)
         #               print(''.join(m1))
                    if re.match(expr_pam, m):
                        print(m)
 
       # if not line: break #break for EOF


        

def parse(argv): #testing - not called
    with open(canlog) as f:
        for line in f:
            for match in expr_comp.findall(f.readline()):
                print(match)        #only matching starting at data3, why?
#    l = args.log_file.readline()                        ### use regular readline: consider argparse alt 
#    m = []
#    for l in prov_log:
#        core_r = (re.findall(expr, l, re.S))
#        m += core_r
#        print(m)
#    prov_log.close()


def test():
    with open(args.log_file.name) as f:
        #for i in range(4):
        #    f.next()
        for l in f:
            for match in expr_comp.findall(f.readline()):
                print(match)        #only matching starting at data3, why?
            #print(l)

def start():
    pass

def end():
    pass


## Count function for NSS/PAM calls ##
def call_count(count):
    with open(canlog) as f:
        expr_pam2 = re.compile(r"(.*)", re.M)
        expr_nss = re.compile(r"(.*data.*)", re.M)
        l = log.readline() 
        pam_count = expr_pam2.match(l)       #not evaluating; why? ##because we are only seeing the first line!
        nss_count = expr_nss.match(l)
        print(pam_count)
        print(nss_count)
    if count == 1:
        if pam_count:  ## -s pam
            with open(canlog) as f:
                num_lines = len(f.readline())
                print ("PAM calls: %s \n" % num_lines)
    elif count == 2:   ## -e nss
        if nss_count:
            with open(canlog) as f:
                num_lines = len(f.readline())
                print ("NSS calls: %s \n" % num_lines)
    else:
        print("NADA!")
 #   print("nss: %s \n" % nss_count)
 #   print("pam: %s \n" % pam_count)
    
def adinfo_support():
        #if "adinfo_support" in str(args.log_file):
            # print (args.log_file)
            #do some special stuff for adinfo_support (environmental prettiness)
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
    #call_count(pam)
    #parse(sys.argv[1:])
    #test()


## DEBUG ##
print ("\n\n\nStart line: %s" % args.start )
print (args)
print (sys.argv)
###########
