#!/usr/bin/env python
import re, argparse, sys, os, itertools 
from time import mktime, strftime, strptime
from datetime import datetime, timedelta
import timeit
#import operator, fileinput
from collections import Counter, defaultdict
#from operator import itemgetter
#from itertools import groupby, starmap

#### Argument/other configuration
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
parser.add_argument('-v',
                        '--verbose',
                        metavar="NUM",
                        help='Increase output verbosity',
                        required=False)

args = parser.parse_args()




## MUTABLE/USER-DEFINED REGEX PATTERNS FOUND IN 'pat_file'. STORED IN THE CURRENT WORKING DIRECTORY     ##
## Add patterns that match *from string beginning* any lines to be returned                             ##
## Commented patterns are ignored. Comments acceptable at EOL                                           ##
## eg.
'''
$ cat pat_file
.*data.* # datatest
.*red.* # redtest
# .*testing.* # testing -disabled
'''

log     = args.log_file
pretty  = ( "-" * 50 )

def main(argv, input_file):
    vs = VarStore()
    file_size = sizeof_fmt(os.path.getsize(log)) 
    if args.out is not None:
        sys.stdout = open(args.out, "w")
    
    if args.log_file: #primary - "overview output"

        try:

            with open(input_file, 'r') as parse_target, open('pat_file', 'r') as pat_list: 

                for line in pat_list:
                    if "#" in line: l = line[:line.index("#")].strip()
                    else:           l = line.strip()
                    if not l.startswith("#") and len(l) != 0: vs.pat_store += (l,)
                patterns  = re.compile( '|'.join( ['(%s)' % i for i in vs.pat_store] ) )
                print("Loading user-defined patterns from ./pat_file...")
                parse_out = parse( parse_target, patterns, vs )

        except IOError as err:
            print("Operation failed: %s" % (err.strerror))
            sys.exit( """Error: Script execution terminated unexpectedly. 	
            \nPlease verify command integrity and dependent pattern file './pat_file' exists and is readable""" )

    p = parse_out
    print_goodness( p, input_file, file_size, pretty, vs.pat_store )


def parse(parse_target,patterns,vs): 
    print("Analysis started...")
    keys = [ 'sshd', 'blah' ] 
    #kw_pat  = re.compile( '|'.join( ['(%s)' % i for i in keys] ) )
    idx,opened_fd,closed_fd,kw_match= ( [], [], [], [] )
    sshd_lc, sshd_matches = [], []
    afd = {}

    for ( line_count, line ) in enumerate( parse_target, 1 ):
        if line.strip(): timestamp = line.strip()[0:15] #alt - split by fields
        try:
            vs.reg.match( vs.time_chk, line )
            #print( timestamp.split(" ") ) 
            vs.times   += ( mktime( strptime( timestamp, "%b %d %H:%M:%S" ) ), )
            last_time   = vs.times[-1]
            gap         = ( last_time - vs.x )

            if ( vs.i == 0 ): #first log entry
                log_start = time_calc( vs.i, timestamp, vs.times ) #yank timestamp as "Log start"
            else:
                if   ( vs.x == last_time ):
                    #print("equals %s" % (timestamp))
                    pass
                elif ( vs.x < last_time and gap > 4 ):
                    vs.time_gap.append( int(gap) )
                    vs.time_lc.append( line_count )
                vs.x = last_time
            vs.i += 1

        except:
            timestamp = None

        if ( line.find("Accepted new lrpc2 client on <fd:") ) >= 0:
            fd_open         = line.split(" ")[13].lstrip("<fd:").rstrip(">'")
            opened_fd.append( fd_open )
            afd[fd_open] = "OPEN"

        if ( line.find("lrpc client disconnected normally ") ) >= 0:
            fd_close    = line.split(" ")[12].lstrip("<fd:").rstrip(">\n'")
            afd[fd_close] = "CLOSE"


        ## Primary matching from patterns contained in patterns tuple ##
        if ( vs.reg.match(patterns, line) ): # User-defined matches (./pat_file)
            m      = vs.reg.m.group(0)
            vs.m_lc.append( line_count )
            vs.matches.append( m ) 
            #idxmatch_gen  = [index for ( index, data ) in enumerate( vs.matches ) if m in data]
            #  ^ not reasonable for large files - pull index line-by-line instead
            ofd_list = []

            for i in opened_fd: # same result as set(opened_fd), but in olist - necessary
                if i not in ofd_list:
                    ofd_list.append(i)
            #for keyword in keys:
            #    if keyword in m:
            #        for index in idxmatch_gen: 
            #            idx.append( index )
            #            kw_match.append( vs.matches[index] )

            for ofd in ofd_list:
                if "sshd(" in m and ("fd:"+ofd) in m:
                    sshd_lc.append( str(line_count) )
                    sshd_matches.append( m )
            
            
            if ( 'data' in m ): vs.nss_count += 1
            if ( 'red'  in m ): vs.pam_count += 1

            #if ( m.find("sshd(") ) >= 0:
            #    sshd_fd = m.split(" ")[6].lstrip("<fd:")

            #if ( m.find("pam_sm_authenticate") ) >= 0:
            #    auth_fd    = m.split(" ")[6][4:] # returns auth thread fd

            if ( m.find("Authentication for user ") ) >= 0: # improve or exapand NEED ACTION
                user       = m.split(" ")[-1].strip("'") # returns user name in this context...

           # elif m.find("Accepted gssapi-with-mic for ") >= 0:
           #     pass

                if   ( 'ssh' in m ): 
                    if user not in vs.ssh_users: vs.ssh_users.append( user )
                elif ( 'dzdo' in m ): 
                    if user not in vs.dz_users: vs.dz_users.append( user )
                    
                
            ## add success to s_users, fail to f_users. Conditional print based on matches in users -> f/s_users
            ## consider just doing context output for now. ie. just printing a user's login loop, rather than pretty output for the time being. Once we get this info, it will be easy enough to parse it further for pretty out.

    z = 0
    # print lines containing 'sshd' keyword along the same FDs from list of opened FDs in file

    for ofd in ofd_list:
        for (lc,smatch) in zip(sshd_lc,sshd_matches):
            if ("fd:"+ofd) in smatch and afd[ofd] == "OPEN":
    #            print(lc,smatch)
                pass
            #if fd and ssh and user  and sshd(xxxx) in smatch?:
            #    dictappend.('user':smatch, etc..)
           # if ofd_list[1] and ("fd:"+ofd_list[1]) in smatch:
           #     print(lc,smatch) 
           # if ofd_list[2] and ("fd:"+ofd_list[2]) in smatch:
           #     print(lc,smatch) 
           # if ofd_list[3] and ("fd:"+ofd_list[3]) in smatch:
           #     print(lc,smatch) 
           # if ofd_list[4] and ("fd:"+ofd_list[4]) in smatch:
           #     print(lc,smatch) 
           # if ofd_list[5] and ("fd:"+ofd_list[5]) in smatch:
           #     print(lc,smatch) 


    log_end   = time_calc( vs.i, timestamp, vs.times )
    elapsed   = ( log_end[1].day-1, log_end[1].hour, log_end[1].minute, log_end[1].second )
    vs.parse_results( elapsed, line_count, log_start, log_end[0] )


    return vs.parse_out
    

        
#### Supplemental



def t_dict(d, item):

    return {k:v[:item] for k,v in d.iteritems()} 
    
class VarStore:

    def __init__(self):
        self.pat_store = ()

        self.time_chk       = re.compile(r'^([A-Za-z]{3} [0-9]{2} [0-9]{2}[:]?[0-9:]+.*)$')
        self.reg            = Re()
        self.x              = 0
        self.nss_count      = 0
        self.pam_count      = 0
        self.i              = 0
        

        (self.times, self.time_gap, 
         self.time_lc, self.matches, 
         self.m_lc,self.ssh_users, 
         self.dz_users, self.s_users, 
         self.f_users)                   = [[] for li in range(9)]

    def parse_results( self,elapsed,line_count,log_start,log_end ):
        self.parse_out = { 'time_gap':self.time_gap, 'time_lc':self.time_lc, 'elapsed':elapsed, \
                    'nss_count':self.nss_count, 'pam_count':self.pam_count, 'm_lc':self.m_lc, 'lc':line_count, \
                    'matches':self.matches, 'log_start':log_start, 'log_end':log_end, 'ssh_user':self.ssh_users, \
                    'dz_user':self.dz_users }
class Re(object):

    def __init__(self):
        self.m = None

    def match( self, pattern, line ):
        self.m = pattern.match(line)
        return self.m

    def search( self, pattern, line ):
        self.m = pattern.search(line)
        return self.m

def time_calc( i, timestamp, times ):

    if ( i == 0 ): #first line

        times                   += ( mktime( strptime( timestamp, "%b %d %H:%M:%S" ) ), )

        return timestamp

    elif ( i != 0 ):
        try:
            times, timestamp

            times               += ( mktime( strptime( timestamp, "%b %d %H:%M:%S" ) ), )
            duration            = timedelta( seconds=( times[-1]-times[0] ) )
            d                   = datetime( 1,1,1 ) + duration

            return ( timestamp, d )
        except:
            pass

def sizeof_fmt( num, suffix='B' ):

    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if ( abs(num) < 1024.0 ):
            return "%3.1f%s%s" % ( num, unit, suffix )
        num /= 1024.0

    return ( "%.1f%s%s" % (num, 'Yi', suffix) )

def print_goodness( p, input_file, file_size, pretty, pat_store ):

    # Look into replacing format operators with new versions. see:
    # https://docs.python.org/2/library/string.html#format-string-syntax
    v = args.verbose    

    print ("\n-> Performing analysis of log: '{0}'({1})".format( input_file, file_size ))
    print ("\nLog start: %s" % (p['log_start']))
    print ("Log end:   %s" % (p['log_end']))
    print ("Elapsed:   %d days %d hr %d min %d sec\n" %(p['elapsed']))
    print ("Lines: %d\n" % (p['lc'])) 

    print ("\n%s\nDoebug information:\n%s\n" % ( pretty, pretty ))
    if p['ssh_user']: print ("Authentication attempts made for the following users via sshd:\n%s\n" % (p['ssh_user']))
    if p['dz_user']:  print ("Authentication attempts made for the following users via dzdo:\n%s\n" % (p['dz_user']))
    if p['time_gap'] and (v == "0"): 
        i = 0
        print ("Irregular time gaps (Only first 10 are displayed. Use -v for all):")
        for gap, l in zip(p['time_gap'], p['time_lc']):
            if i == 10: break
            print("%4s seconds on line: %s" % (gap, l))
            i += 1
    elif p['time_gap'] and ( v == "1" ):
        print ("Irregular time gaps:") 
        for gap, l in zip(p['time_gap'], p['time_lc']):
            print("%4s seconds on line: %s" % (gap, l))
        
    print ("\nNSS calls: '%s' in the file: %s" % ( p['nss_count'], log ))
    print ("PAM calls: '%s' in the file: %s\n" % ( p['pam_count'], log ))
    print ("\n%s\nPattern detection:\n%s\n" % ( pretty, pretty ))
    print ("Matching against patterns in ./pat_file: \n {%s}\n" % ( "}, {".join(pat_store,) ))
    print ("Matched lines truncated: To display full matches, please use the '-v' option. \
            \n(Note: This may result in substantial output. Consider outputting results to a file via '-o')\n")

#    if ( v == "1" ):
#        for ( l, m ) in zip( p['m_lc'], p['matches'] ):
#            print("%-*s %s" % (2, l, m))
#    else:
#        i = 0
#        for ( l, m ) in zip( p['m_lc'], p['matches'] ):
#            if i == 10:
#                break
#            if len(m) > 90:
#                print("%-*s %.90s..." % (5, l, m))
#            else:
#                print("%-*s %s" % (5, l, m))
#            i += 1
#    


######################### testing / not implemented

def part(fileinput, chunk=1024*1024):
    while True:
        result = fileinput.read(chunk)
        if not result:
            break
        yield result

def process3(fileinput, pat, chunk):
    f = open(fileinput)
    f.seek(chunk[0])
    d = defaultdict(int)
    search = pat.search
    for line in f.read(chunk[1]).splitlines():
        if "GET /ongoing/When" in line:
            m = search(line)
            if m:
                d[m.group(1)] += 1
    return d

def string_match(sm, lc):
    for i, m in enumerate(sm): 
        #m = m.rstrip("\n")
        lc += 1
        print(lc, m)
    
    
def start():
    pass

def end():
    pass



if __name__ == "__main__":
    main(sys.argv[1:], log)

## DEBUG ##
print ("\n\n########### debugging\n") 
print ("args passed: %s" % (sys.argv))
print ("\n-s: %s" % args.start )
print ("-e: %s" % args.end )
print (args)
###########
