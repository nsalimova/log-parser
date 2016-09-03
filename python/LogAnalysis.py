#!/usr/bin/env python
import re, argparse, sys, string, datetime #re for regex, argparse for options, sys for argv
#import operator, fileinput  

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




####################################
#------- Globals declaraion -------#
####################################
expr_comp = re.compile(r"(.*data.*)", re.M)
expr_pam = re.compile(r"(.*red.*)", re.M)
log = args.log_file 

# Patterns for primary parsing logic
# All "relevant logs" should match a pattern in this array
expr_strings = ['.*data.*', 
                '.*red.*',
               # '.*CAPIValidate.*adagent.*',
                '.*example.*']




####################################
#----- Primary logic / parser -----#
####################################
def main(argv, input_file):
    ## -o ##
    if args.out is not None:
        outtofile(args.out)
    ########
    
    if args.log_file: #primary - "overview output"
        with open(input_file) as parse_target: #maybe move this line to main()? then things below stay here? 
            parse(parse_target, expr_strings)

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
    timestamp = []
    global nss_count, pam_count
    nss_count, pam_count = (0, 0)
        #for p in part(f):  # parse by chunk - temporarily disabled in favor of line-by-line for now
    for line_count, line in enumerate(parse_target, 1):
        for regex in patterns: 
            finditer = (re.findall(regex, line, re.M))

        ## Iterate lines matching patterns provided in expr_strings[] ##
            for match in finditer: 

        ## Fringe-case pattern matching - Currently demo for NSS/PAM count logic ##
                call_count(match, line_count) 
    print("NSS calls: '%s' in the file: %s" % (nss_count, log))
    print("PAM calls: '%s' in the file: %s" % (pam_count, log))


        
####################################
#----- Supplemental functions -----#
####################################


## Output to file designated with -o/--out ##
def outtofile(output_file):
    sys.stdout = open(output_file, "w")


## Count function for NSS/PAM calls ##
def call_count(m, line_count):
    global nss_count, pam_count
    if re.match(expr_comp, m): 
        nss_count += 1
#        print(line_count, m)
    if re.match(expr_pam, m):
        pam_count += 1
#        print(line_count, m)






######################### in development


def time_calc(m, time):
    time.append(m[2].split(":"))
    #print(int(time[-1][-1])-int(time[0][2]))
    #print(time[0][0]) 
    #print(time)
    #time = ''.join(time)
    #time = ''.join(m[2])
    #print(time)

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
