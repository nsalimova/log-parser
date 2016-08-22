#!/usr/bin/env python
import re, argparse, sys, string #re for regex, argparse for options, sys for argv
#import operator, fileinput  

####################################
### Argument/other configuration ###
####################################
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


####################################
######## Globals declaraion ########
####################################
expr_comp = re.compile(r"(.*data.*)", re.M)
expr_pam = re.compile(r"(.*red.*)", re.M)
log = args.log_file ## TextIOWrapper - primary file fed in as passed file
colog = args.log_file.name  ## colloquial name for passed file (attribute of args.log_file)

# Patterns for primary parsing logic
# All "relevant logs" should match a pattern in this array
expr_strings = ['.*data.*', 
                '.*red.*',
                '.*example.*']
####################################




####################################
###### Primary logic / parser ######
####################################
def main(argv):
    global m_count
    global m2_count
    m_count = 0
    m2_count = 0
    pam = 1 ## returns on -s invocation
    nss = 2 ## returns on -e invocation

 
    with open(colog) as f: # opening our log file and assigning it the value 'f' in memory
        for l in f: # for line in provided file
            for pat_list in expr_strings: 
                finditer = (re.findall(pat_list, l, re.S))
                for i, m in enumerate(finditer): 
                    m = m.rstrip("\n") 
                    if re.match(expr_comp, m): 
                        m_count += 1
#                        print(m)
                    if re.match(expr_pam, m):
                        m2_count += 1
#                        print(m)
        print("There are '%s' instances of 'data' in the file: %s" % (m_count, colog))
        print("There are '%s' instances of 'red' in the file: %s" % (m2_count, colog))

        ## invoke call_count() for NSS/PAM calls depending on arguments passed (-s/-e are placeholders)
        if args.start and args.end: ## -s and -e
            call_count(nss)
            call_count(pam)
        elif args.start: # -s
                call_count(pam)
        elif args.end:   # -e
                call_count(nss)
 
####################################


        
####################################
###### Supplemental functions ######
####################################



def start():
    pass

def end():
    pass


## Count function for NSS/PAM calls ##
def call_count(count):
    if count == 1: 
        print ("PAM calls: %s (value derived from pattern: %s" % (m_count, expr_comp))
    elif count == 2:   ## -e nss
        print ("NSS calls: %s (value derived from pattern: %s" % (m2_count, expr_pam)) 
    else:
        print("NADA!")

# alt call_count - preserving until QA just to be safe
    #with open(colog) as f: # open file and assign to 'f'
        #expr_pam2 = re.compile(r"(.*)", re.M)
        
        #expr_nss = re.compile(r"(.*data.*)", re.M) 
        #l = log.readline() # bane of existence. This needs to go into a for loop at some point. Reads line of file.
        #pam_count = expr_pam2.match(l) 
        #nss_count = expr_comp.match(l) 
       # print(pam_count) #debug
       # print(nss_count) #""
     #   pass
    
def adinfo_support(): # still testing - not invoked
    if "adinfo_support" in str(args.log_file):
         print (args.log_file)
        #do some special stuff for adinfo_support (environmental prettiness)
    pass


def test(): # misc testing - not currently invoked
    with open(args.log_file.name) as f:
        #for i in range(4):
        #    f.next()
        for l in f:
            for match in expr_comp.findall(f.readline()):
                print(match)        #only matching starting at data3, why?
            #print(l)


def parse(argv): #testing alternate primary logic for main() - not currently in use or called anywhere
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
                       # m1 = [] # testing - blank array
                       # m1 += m # testing - add to array
                       # m1 = ''.join(m1)
                       # m1 = len(m1)
                        #print(''.join(m1))





if __name__ == "__main__":
    main(sys.argv[1:])
    #call_count(pam)
    #parse(sys.argv[1:])
    #test()


## DEBUG ##
print (sys.argv)
print ("\n\n\nStart line: %s" % args.start )
print ("End line:   %s" % args.end )
print (args)
###########
