#!/usr/bin/env python
import re, argparse, sys, os, itertools 
import time
from time import mktime, strftime, strptime
from datetime import datetime, timedelta
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

    p   = parse_out
    p1  = vs.process_out
    print_goodness( p, p1, input_file, file_size, pretty, vs.pat_store, vs.suserd )







def parse(parse_target,patterns,vs): 
    print("Analysis started...")
    #keys = [ 'sshd', 'blah' ] 
    #kw_pat  = re.compile( '|'.join( ['(%s)' % i for i in keys] ) )
    idx,valid_fd,closed_fd,kw_match= ( [], [], [], [] )
    sshd_lc, sshd_matches = [], []
    afd = {}
    extra_time = [0]
    pr = Process()
    ssh_success = 0
    pam_auth_starts = []
    pam_user_lines  = []
    pam_auth_ends   = []
    pam_loop        = []
    for ( line_count, line ) in enumerate( parse_target, 1 ):
        #line = line.strip("\n")
        #if line.strip():
          #  if "adclient" in line: 
          #      line = line.split("adclient")
          #      meta, data = line[0], line[1]
          #  else:
          #      meta,data = line,line
        chunkyank = line.strip()[0:15]
        #if re.match( vs.time_chk, chunkyank): 
        try: 
            if re.match( vs.time_chk, chunkyank):
                vs.timestamp = chunkyank #alt - split by fields
            if vs.i == 0: 
                time_calc( vs.i, vs.timestamp, vs, line_count, end=0 )
                vs.i += 1
            if len(vs.timestamp.split()) == 3:
                p_ts = line.split()[:3]
                extra_time.append(int(p_ts[2].split(":")[2]))
                if ( extra_time[-1]-extra_time[0] ) >= 5:
                    time_calc( vs.i, vs.timestamp, vs, line_count, end=0 )
                extra_time.remove(extra_time[0])

        except:
            pass
        finally:
            if ( line.find("Accepted new lrpc2 client on <fd:") ) >= 0:
                fd_open         = line.split(" ")[13].lstrip("<fd:").rstrip(">'")
                if fd_open not in set(valid_fd):  valid_fd.append( fd_open )
                afd[fd_open] = "OPEN"
            

            if ( line.find("lrpc client disconnected normally ") ) >= 0:
                fd_close    = line.split(" ")[12].lstrip("<fd:").rstrip(">\n'")
                afd[fd_close] = "CLOSE"
            
            if ( "sshd" in line and "pam_sm_authenticate" in line and "result" not in line ):
                pam_auth_starts.append(line)
                pam_loop.append(line)
            if ( "Authentication for user" in line ):
                pam_user_lines.append(line)
                if line not in pam_loop: pam_loop.append(line)
            if ( "sshd" in line and "pam_sm_open_session" in line and "PAM_SUCCESS" in line ):
                pam_auth_ends.append(line)
                pam_loop.append(line)

            if any(sk in line for sk in vs.sshd_keys):
                if "PAM_SUCCESS" in line or "PAM open session granted" in line:
                    ssh_success = 1
                pr.sshd(line, vs.timestamp, vs, line_count, success=1)
                

            ## Primary matching from patterns contained in patterns tuple ##
            if ( vs.reg.match(patterns, line) ): # User-defined matches (./pat_file)
                m      = vs.reg.m.group(0)
                vs.m_lc.append( line_count )
                vs.matches.append( m ) 

                #for vfd in list(set(valid_fd)): # sloooooow
                #    if "sshd(" in m and ("fd:"+vfd) in m: #if fd still ope
                if "sshd(" in m:
                    sshd_lc.append( str(line_count) )
                    sshd_matches.append( m )
                
                #process(m, vs)
                        
                    
                ## add success to s_users, fail to f_users. Conditional print based on matches in users -> f/s_users
                ## consider just doing context output for now. ie. just printing a user's login loop, rather than pretty output for the time being. Once we get this info, it will be easy enough to parse it further for pretty out.

    #z = 0
    # print lines containing 'sshd' keyword along the same FDs from list of opened FDs in file

    #for vfd in list(set(valid_fd)):
    #    for (lc,smatch) in zip(sshd_lc,sshd_matches):
    #        if ("fd:"+vfd) in smatch and afd[vfd] == "OPEN": # if valid FD and if ACTIVE FD-only works lin-by-line
    #            print(lc,smatch)
    #            pass
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

    
    log_end   = time_calc( vs.i, vs.timestamp, vs, line_count,  end=1 )
    elapsed   = ( log_end[1].day-1, log_end[1].hour, log_end[1].minute, log_end[1].second )
    vs.parse_results( elapsed, line_count, vs.log_start, log_end[0] )
    for s_user in set(vs.s_users):
        vs.s_usersc.append(str(vs.s_users.count(s_user)))
    for f_user in set(vs.f_users):
        vs.f_usersc.append(str(vs.f_users.count(f_user)))
    s_tse,e_tse = [],[]





    #print("\n".join(s for s in pam_loop))
    #for vfd in list(set(valid_fd)):
        #print("\n".join(s for s in pam_loop if "fd:"+vfd in s))
    #    pass
    #yank timestamp -> convert to epoch -> store value -> timedelta two values -> booya
        #for (s,e) in zip(pr.sloopstart,pr.sloopend):
        #    if ("fd:"+vfd) in s and ("fd:"+vfd) in e:
    #print(s_tse)
    #print(e_tse)

    #self.slooptime = time_calc( vs.i, ts, vs, line_count, oneoff=1 )    
    #print(self.slooptime)
    #sat = self.slooptime
    #self.sat_e = (sat[1].minute/60 + sat[1].second)
    #if self.sat_e  >= 10:
    #    self.auth_gap = True
    #    vs.a_gap.append(self.at_e)
    


    return vs.parse_out
    

        
#### Supplemental

class Process:
    
    def __init__(self):
        self.slooptime  = None
        self.sat_e      = None
        self.i          = 0
        self.auth_time  = False
        self.s_userc    = 0
        self.ssh_userl  = []
        self.sloopstart = []
        self.sloopend   = []
        self.sloop     = defaultdict(list)

    def sshd(self, line, ts, vs, line_count, success=1):
        #self.auth_time = time_calc( vs.i, ts, vs, line_count, end=1 )
        if success == 1:
            if "sshd(" in line and "Authentication for user" in line:
                #self.sloopu = line.split("'")[1] #is user our responsibility
                self.sloopu = line.split("'")[1]
                self.sloopstart.append(line)
                self.sloop[self.sloopu].append(line)
#todo: test against another log - test against sso

            if "service=sshd" in line and "PAM open session granted" in line:
                s_user = line.split("user=")[1].split("(")[0]
                vs.s_users.append(s_user)
                self.sloopend.append(line)
                if self.sloop[s_user]:
                    #print("pre_append",self.sloop[s_user])
                    self.sloop[s_user].append(line)
                    #print("post_append",self.sloop[s_user])
                    print("start",self.sloop[s_user][0].strip()[0:15])
                    print(self.sloop[s_user][0])
                    print("end",self.sloop[s_user][-1].strip()[0:15])
                    print(self.sloop[s_user][-1])
                    # do time stuff with completed loop
                    #s_ts = self.sloop[s_user][0].strip()[0:15]
                    #e_ts = e.strip()[0:15]
                    #s_tse += time_calc( vs.i, s_ts, vs, line_count, oneoff=1 )
                    #e_tse += time_calc( vs.i, e_ts, vs, line_count, oneoff=1 )
                    del self.sloop[s_user] #remove user loop so that next one can enter
                   # print("post_del",self.sloop[s_user])
                else:
                    #unknown logic - broken login loop
                    pass


            if "service=sshd" in line and "PAM authentication denied" in line:
                f_user = (line.split("user")[1].split(")")[0].lstrip("=") + ")")
                vs.f_users.append(f_user)
            if "Getting unix name of" in line:
                self.ssh_userl.append(line)




            
        vs.process_results()


            #print("user: time: method: count:")
            


       

def process(m, vs):
    if ( 'data' in m ): vs.nss_count += 1
    if ( 'red'  in m ): vs.pam_count += 1

    if ( m.find("sshd(") ) >= 0:
        sshd_fd = m.split(" ")[6].lstrip("<fd:")

    if ( m.find("pam_sm_authenticate") ) >= 0:
        auth_fd    = m.split(" ")[6][4:] # returns auth thread fd

    if ( m.find("Authentication for user ") ) >= 0: # improve or exapand NEED ACTION
        user       = m.split(" ")[-1].strip("'") # returns user name in this context...
    else:
        user = None ## temp til better logic for users

   # elif m.find("Accepted gssapi-with-mic for ") >= 0:
   #     pass

    if   ( 'ssh' in m ): 
        if user not in vs.ssh_users: vs.ssh_users.append( user )
    elif ( 'dzdo' in m ): 
        if user not in vs.dz_users: vs.dz_users.append( user )

        




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
        self.log_start      = None
        self.timestamp      = None
        self.suserd         = defaultdict(list)
        

        (self.times, self.time_gap, 
         self.time_lc, self.matches, 
         self.m_lc,self.ssh_users, 
         self.dz_users, self.s_users, 
         self.f_users,self.at_times,
         self.s_usersc,self.f_usersc,
         self.a_gap,self.otimes)              = [[] for li in range(14)]

        self.sshd_keys  = ['pam_sm_authenticate','PAMGetUnixName','AUDIT_TRAIL','PAM_AUTHTOK',
                           'Authentication for user']
        self.sshd_dkeys = ['pam_sm_authenticate','PAMUserIsOurResponsibility','PAMGetUnixName','PAM_AUTHTOK',
                          'PAMVerifyPassword','PAMIsMfaEnabled','PAMIsMfaRequired','UTF8STRING','AUDIT_TRAIL',
                          'pam_sm_acct_mgmt','DAIIsUserAllowedAccessByAudit2','PAMIsUserAllowedAccess2',
                          'PAMDoesLegacyConflictExist','Result: account=','GID array count:',
                          'pam_sm_setcred','Set credentials for user','Open session: Set environment variable',
                          'PAMCreateHomeDirectory','getpwnam_centrifydc_r','DAIReplacePasswdWithNoLoginShellByAudit',
                          'pam_sm_open_session']

    def parse_results( self,elapsed,line_count,log_start,log_end ):
        self.parse_out      = { 'time_gap':self.time_gap, 'time_lc':self.time_lc, 'elapsed':elapsed, \
                    'nss_count':self.nss_count, 'pam_count':self.pam_count, 'm_lc':self.m_lc, 'lc':line_count, \
                    'matches':self.matches, 'log_start':log_start, 'log_end':log_end, 'ssh_user':self.ssh_users, \
                    'dz_user':self.dz_users }

    def process_results( self ):
        self.process_out    = { 's_users':self.s_users,'s_usersc':self.s_usersc,'f_users':self.f_users, \
                    'f_usersc':self.f_usersc,'a_gap':self.a_gap }

## DO SOMETHING WITH THIS OR GET RID OF IT
## http://stackoverflow.com/questions/597476/how-to-concisely-cascade-through-multiple-regex-statements-in-python/597493
class Re(object): 
    def __init__(self):
        self.m = None

    def match( self, pattern, line ):
        self.m = pattern.match(line)
        return self.m

    def search( self, pattern, line ):
        self.m = pattern.search(line)
        return self.m

def time_calc( i, timestamp, vs, line_count, end=0, oneoff=0 ):
    if ( oneoff == 0 ):
        if ( end == 0 ):
            vs.times   += ( mktime(convert_time(timestamp)[1]), )  
            last_time   = vs.times[-1]
            gap         = ( last_time - vs.x )
            if ( i == 0 ): #first line

                #times                   += ( mktime( strptime( timestamp, "%b %d %H:%M:%S" ) ), )
                vs.times                     += ( mktime(convert_time(timestamp)[1]), )  
                vs.log_start               = timestamp #yank timestamp as "Log start"
            else:
                if ( vs.x == last_time ):
                    #print("equals %s" % (timestamp))
                    pass
                elif ( vs.x < last_time and gap > 5 and gap < 9000 ): #safe-guard; convert_time uses positive stamps 
                    vs.time_gap.append( int(gap) )
                    vs.time_lc.append( line_count )
                vs.x = last_time

        elif ( end == 1 ):

            if ( i != 0 ):
                try:
                    vs.times, timestamp

                    #times               += ( mktime( strptime( timestamp, "%b %d %H:%M:%S" ) ), )
                    vs.times                   += ( mktime(convert_time(timestamp)[1]), )  
                    duration            = timedelta( seconds=( vs.times[-1]-vs.times[0] ) )
                    d                   = datetime( 1,1,1 ) + duration

                    return ( timestamp, d )
                except:
                    pass
            else:
                print("EPIC FAILURE IN TIME_CALC")
    elif ( oneoff == 1 ):
        vs.otimes                   += ( mktime(convert_time(timestamp)[1]), )  
        if len(vs.otimes) > 2: del vs.otimes[0]
        #print(vs.otimes)
        duration            = timedelta( seconds=( vs.otimes[-1]-vs.otimes[0] ) )
        #print(duration)
        d                   = datetime( 1,1,1 ) + duration

        return ( timestamp, d )
            



months = dict(jan=1,feb=2,mar=3,apr=4,may=5,jun=6,jul=7,aug=8,sep=9,oct=10,nov=11,dec=12)

def convert_time(string, year=None):
    if year is None: year = time.gmtime()[0]
    mon,d,t = string.split(" ")
    h,m,s   = t.split(":")
    mon     = months[mon.lower()]
    tt      = [year, mon,d,h,m,s,0,0,0]
    tt      = tuple([int(v) for v in tt])
    ts      = int(time.mktime(tt))
    tt      = time.gmtime(ts)
    return (ts, tt, string)



def sizeof_fmt( num, suffix='B' ):

    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if ( abs(num) < 1024.0 ):
            return "%3.1f%s%s" % ( num, unit, suffix )
        num /= 1024.0

    return ( "%.1f%s%s" % (num, 'Yi', suffix) )



def print_goodness( p, p1, input_file, file_size, pretty, pat_store, suserd ):

    # Look into replacing format operators with new versions. see:
    # https://docs.python.org/2/library/string.html#format-string-syntax
    v = args.verbose    
    #print(p1['a_gap'])

    print ("\n-> Performing analysis of log: '{0}'({1})".format( input_file, file_size ))
    print ("\nLog start: %s" % (p['log_start']))
    print ("Log end:   %s" % (p['log_end']))
    print ("Elapsed:   %d days %d hr %d min %d sec\n" %(p['elapsed']))
    print ("Lines: %d\n" % (p['lc'])) 

    print ("\n%s\nDebug information:\n%s\n" % ( pretty, pretty ))
    if p['ssh_user']: print ("Authentication attempts made for the following users via sshd:\n%s\n" % (p['ssh_user']))
    if p1['s_users']: 
        print ("Authentication successful for the following users via sshd:\n")
        for u,c in zip(set(p1['s_users']),p1['s_usersc']):
            print ("user: {:50} count: {}".format(u, c))
    if p1['f_users']: 
        print ("Authentication failed for the following users via sshd:\n")
        for u,c in zip(set(p1['f_users']),p1['f_usersc']):
            print ("user: {:50} count: {}".format(u, c))
    if p['dz_user']:  print ("\nAuthentication attempts made for the following users via dzdo:\n%s\n" % (p['dz_user']))
    if p['time_gap'] and ( v == "1" ):
        print ("\nIrregular time gaps:") 
        for gap, l in zip(p['time_gap'], p['time_lc']):
            print ("%4s seconds on line: %s" % (gap, l))
    else:
        i = 0
        print ("\nIrregular time gaps (Only first 10 are displayed. Use -v for all):")
        for gap, l in zip(p['time_gap'], p['time_lc']):
            if i == 10: break
            print ("%4s seconds on line: %s" % (gap, l))
            i += 1
        
    print ("\nNSS calls: '%s' in the file: %s" % ( p['nss_count'], log ))
    print ("PAM calls: '%s' in the file: %s\n" % ( p['pam_count'], log ))
    print ("\n%s\nPattern detection:\n%s\n" % ( pretty, pretty ))
    print ("Matching against patterns in ./pat_file: \n {%s}\n" % ( "}, {".join(pat_store,) ))
    print ("Matched lines truncated: To display full matches, please use the '-v' option. \
            \n(Note: This may result in substantial output. Consider outputting results to a file via '-o')\n")

    if ( v == "1" ):
        for ( l, m ) in zip( p['m_lc'], p['matches'] ):
            print ("%-*s %s" % (2, l, m))
    else:
        i = 0
        for ( l, m ) in zip( p['m_lc'], p['matches'] ):
            if i == 10:
                break
            if len(m) > 90:
                print ("%-*s %.90s..." % (5, l, m))
            else:
                print ("%-*s %s" % (5, l, m))
            i += 1
    


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
