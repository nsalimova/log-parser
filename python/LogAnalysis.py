#!/usr/bin/env python
import re, argparse, sys, string #re for regex, argparse for options, sys for argv
#import operator, fileinput  

####################################
#-- Argument/other configuration --#
####################################
parser = argparse.ArgumentParser(description='Log parser - For internal testing purposes only (for now)')

parser.add_argument("log_file",
                        metavar="<log_file>",
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='Log file for parsing')
parser.add_argument('-o',
                        '--out',
                        metavar='<file>',
                        #type=argparse.FileType('w'),
                        #default=sys.stdout,
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




####################################
#------- Globals declaraion -------#
####################################
expr_comp = re.compile(r"(.*data.*)", re.M)
expr_pam = re.compile(r"(.*red.*)", re.M)
log = args.log_file ## TextIOWrapper - primary file fed in as passed file
colog = args.log_file.name  ## colloquial name for passed file (attribute of args.log_file)

# Patterns for primary parsing logic
# All "relevant logs" should match a pattern in this array
expr_strings = ['.*data.*', 
                '.*red.*',
               # '.*CAPIValidate.*adagent.*',
                '.*example.*']




####################################
#----- Primary logic / parser -----#
####################################
def main(argv):
    global m_count, m2_count
    m_count, m2_count, l_count = (0, 0, 0)
    pam = 1 ## returns on -s invocation (just for testing the returns. s/e will be re-implemented later)
    nss = 2 ## returns on -e invocation

    ## -o ##
    if args.out is not None:
        outtofile(args.out)
    ########

    ## Core parsing logic ##
    with open(colog) as f: 
        #for p in part(f):  # parse by chunk - temporarily disabled in favor of line-by-line for now
        for p in f:
            for pat_list in expr_strings: 
                finditer = (re.findall(pat_list, p, re.M))

            ## Print lines matching patterns provided in expr_strings[] ##
                for i, m in enumerate(finditer, 1): 
                    l_count += 1
                    #m = m.rstrip("\n")
                    #print(i, m) 
   

            ## Fringe-case pattern matching - Currently demo for NSS/PAM count logic ##
                    if re.match(expr_comp, m): 
                        m_count += 1
                  #      print(i, m)
                    if re.match(expr_pam, m):
                        m2_count += 1
                        print(l_count, m)
        call_count()
 


        
####################################
#----- Supplemental functions -----#
####################################


## Output to file designated with -o/--out ##
def outtofile(f):
    sys.stdout = open(f, "w")


## Count function for NSS/PAM calls ##
def call_count():
    print("NSS calls: '%s' in the file: %s" % (m_count, colog))
    print("PAM calls: '%s' in the file: %s" % (m2_count, colog))



## Parse by chunk
def part(fileinput, chunk=512):
    while True:
        result = fileinput.read(chunk)
        if not result:
            break
        yield result







######################### in development


def string_match(sm, lc):
    for i, m in enumerate(sm): 
        m = m.rstrip("\n")
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
    main(sys.argv[1:])
    


## DEBUG ##
print (sys.argv)
print ("\n\n\nStart line: %s" % args.start )
print ("End line:   %s" % args.end )
print (args)
###########
