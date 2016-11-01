#!/usr/bin/env python
import re

log = '../logs/adinfo-support-523-rhel7.txt'
keys = ['.*AUDIT_TRAIL.*PAM auth.*user.*service=sshd.*', '.*AUDIT_TRAIL.*PAM open.*service=sshd.*']

if __name__ == '__main__':
    req_keys = re.compile( '|'.join( ['(%s)' % k for k in keys] ) )
    print(req_keys)
    with open(r'/pewter/Projects/log-parser/logs/adinfo_support-523-rhel7.txt') as input_file:
        for lc,l in enumerate(input_file, 1):
            l = l.strip()

            if ( l.find("PAM authentication") ) >= 0 or and "PAM" in l:
                user = l.split(" ")[10]#.split("|")[2].lstrip("user=").rstrip("(")
                print(user)

            if re.match(req_keys, l):
                #print(lc, l)
                pass
