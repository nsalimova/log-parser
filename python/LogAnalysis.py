#!/usr/bin/env python
import re, argparse, sys, string #re for regex, argparse for options, sys for argv
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
expr = '.*data.*' ## not used I don't think? really need to vet all these and cleanup the vars. Just been adding them willy nilly
expr_comp = re.compile(r"(.*data.*)", re.M)
expr_pam = re.compile(r"(.*red.*)", re.M)
expr_nl = re.compile(r"\W+")  ## not used right now - testing
expr_strings = ['.*data.*',   ## this is where all the "primary" regex patterns will be defined
                '.*red.*',
                '.*NSSGet.*']
expr_counts = ['.*data.*']  ## uhhh
log = args.log_file ## TextIOWrapper - primary file fed in as passed file
colog = args.log_file.name  ## colloquial name for passed file (technically an attribute of args.log_file
prov_log = 2#open(args.log_file, 'r') ## testing
logtxt = 2#prov_log.read() ## testing
has_run = False ## used for early call_count() iteration (see commented code under main() 
pam = 1 ## indicator for pam/nss count in main()
nss = 2 ## ""
#line = args.log_file.readline()
########################


## Primary logic / parser ##
def main(argv):
    ## pam/nss count - not actually pulling nss/pam counts. Those are effectively placeholder terms
    if args.start and args.end:
        call_count(nss)
        call_count(pam)
    else:
        if args.start:          ## need to add clause for case where -s and -e are both specified
            call_count(pam) # passes 1 to call_count()
        if args.end:
            call_count(nss) # passes 2 to call_count
 
    with open(colog) as f: # opening our log file and assigning it the value 'f' in memory
        m_count = 0
        m2_count = 0
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
        
        for l in f: # for line in provided file
            for pat_list in expr_strings: # for regex pattern in expr_strings(defined above)
                finditer = (re.findall(pat_list, l, re.S)) # effectively matches the patterns in expr_strings to each line in file, one-by-one

                for i, m in enumerate(finditer): # i = index, m = match. enumerate returns two values (though i just returns 0. Something we need to look at)
                    num_lines = len(f.readline())
                    #print("NUMTEST: %s" % len(m))
                    m = m.rstrip("\n") # strips \n to the right (readline() tags on a \n) 
                    if re.match(expr_comp, m): # if expr_comp matches value returned as m
                        m_count += 1
                        m1 = [] # testing - blank array
                        m1 += m # testing - add to array
                        m1 = ''.join(m1)
                        m1 = len(m1)
                        #print(counter)
                        #print(''.join(m1))
                    if re.match(expr_pam, m):
                        m2_count += 1
                        #print(m)
        print("There are '%s' instances of 'data' in the file: %s" % (m_count, colog))
        print("There are '%s' instances of 'red' in the file: %s" % (m2_count, colog))
 
       # if not line: break #break for EOF


        

def parse(argv): #testing alternate primary logic for main() - not curretnly in use or called anywhere
    with open(colog) as f:
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


def test(): # misc testing - not curretnly in use or called anywhere
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
    with open(colog) as f: # open file and assign to 'f'
        expr_pam2 = re.compile(r"(.*)", re.M) # essentailly assigning that pattern to the var.
        expr_nss = re.compile(r"(.*data.*)", re.M) 
        l = log.readline() # bane of existence. This needs to go into a for loop at some point. Reads line of file.
        pam_count = expr_pam2.match(l)       #not evaluating; why? ##because we are only seeing the first line!
        nss_count = expr_nss.match(l)  # basically assigning a match of expr_nss to l to a variable
       # print(pam_count) #debug
       # print(nss_count) #""
    if count == 1: 
        if pam_count:  ## -s pam
            num_lines = open(colog, 'r').read()
            num_lines = len(num_lines.splitlines())
            print ("PAM calls: %s \n" % num_lines) ## IT WORKS! - now to get it to apply for expr match :)
            print("real count: %s" % p_count)
    elif count == 2:   ## -e nss
        if nss_count:
            num_lines = open(colog, 'r').read()
            num_lines = len(num_lines.splitlines())
            print ("NSS calls: %s \n" % num_lines) ## IT WORKS! - now to get it to apply for expr match :)
    else:
        print("NADA!")
    
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
