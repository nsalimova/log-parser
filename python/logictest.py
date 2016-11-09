#!/usr/bin/env python
import re,mmap,os

log = '../logs/adinfo_support-slowlogin.txt'
keys = ['.*AUDIT_TRAIL.*PAM auth.*user.*service=sshd.*', '.*AUDIT_TRAIL.*PAM open.*service=sshd.*']

if __name__ == '__main__':
    req_keys = re.compile( '|'.join( ['(%s)' % k for k in keys] ) )
    temp = re.compile(b'.*AUDIT_TRAIL.*')
    with open(log, 'r+') as f:
        data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        for line in iter(data.readline, ""):
            if len(line) < 1: break
            if re.search(temp, line):
                print(line)




       # for lc,l in enumerate(input_file, 1):
       #     l = l.strip()

       #     if re.match(req_keys, l):
       #         #print(lc, l)
       #         pass
    
    
