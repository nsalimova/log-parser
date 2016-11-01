#!/usr/bin/env python
import os, re
from tempfile import gettempdir
from itertools import islice, cycle
from collections import namedtuple
import heapq
pat_store = ()
#with open('adinfo_support.txt', 'r+') as f, open('pat_file', 'r') as pat_list:
with open('pat_file', 'r') as pat_list:
    for line in pat_list:
        if "#" in line: l = line[:line.index("#")].strip()
        else:           l = line.strip()
        if not l.startswith("#") and len(l) != 0: pat_store += (l,)
    patterns  = re.compile( ('|'.join( ['(%s)' % i for i in pat_store] )), re.MULTILINE )
    pattern = re.compile(r'(.*DEBUG.*sshd.*Authentication for user \'.*|.*DEBUG.*dzdo.*Authentication for user \'.*|.*DEBUG <main> daemon.ipcserver Accepted new lrpc2 client on.*|.*DEBUG <main> daemon.ipcserver lrpc client disconnected.*)', re.DOTALL | re.IGNORECASE | re.MULTILINE)


Keyed = namedtuple("Keyed", ["key", "obj"])

def merge(key=None, *iterables):
    # based on code posted by Scott David Daniels in c.l.p.
    # http://groups.google.com/group/comp.lang.python/msg/484f01f1ea3c832d

    if key is None:
        #keyed_iterables = iterables
        for element in heapq.merge(*iterables):
            if re.match(patterns, element):
                pass
            yield element
    else:
        keyed_iterables = [(Keyed(key(obj), obj) for obj in iterable)
                            for iterable in iterables]
        for element in heapq.merge(*keyed_iterables):
            yield element.obj


def batch_sort(input, output, key=None, buffer_size=32000, tempdirs=None):
    if tempdirs is None:
        tempdirs = []
    if not tempdirs:
        tempdirs.append(gettempdir())

    chunks = []
    try:
        with open(input,'rb',64*1024) as input_file: 
            input_iterator = iter(input_file)
            for tempdir in cycle(tempdirs):
                current_chunk = list(islice(input_iterator,buffer_size))
                if not current_chunk:
                    break
                current_chunk.sort(key=key)
                output_chunk = open(os.path.join(tempdir,'%06i'%len(chunks)),'w+b',64*1024)
                chunks.append(output_chunk)
                output_chunk.writelines(current_chunk)
                output_chunk.flush()
                output_chunk.seek(0)
        with open(output,'wb',64*1024) as output_file:
            output_file.writelines(merge(key, *chunks))
    finally:
        for chunk in chunks:
            try:
                chunk.close()
                os.remove(chunk.name)
            except Exception:
                pass


if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option(
        '-b','--buffer',
        dest='buffer_size',
        type='int',default=500000,
        help='''Size of the line buffer. The file to sort is
            divided into chunks of that many lines. Default : 32,000 lines.'''
    )
    parser.add_option(
        '-k','--key',
        dest='key',
        help='''Python expression used to compute the key for each
            line, "lambda line:" is prepended.\n
            Example : -k "line[5:10]". By default, the whole line is the key.'''
    )
    parser.add_option(
        '-t','--tempdir',
        dest='tempdirs',
        action='append',
        default=[],
        help='''Temporary directory to use. You might get performance
            improvements if the temporary directory is not on the same physical
            disk than the input and output directories. You can even try
            providing multiples directories on differents physical disks.
            Use multiple -t options to do that.'''
    )
    parser.add_option(
        '-p','--psyco',
        dest='psyco',
        action='store_true',
        default=False,
        help='''Use Psyco.'''
    )
    options,args = parser.parse_args()

    if options.key:
        options.key = eval('lambda line : (%s)'%options.key)

    if options.psyco:
        import psyco
        psyco.full()

    batch_sort(args[0],args[1],options.key,options.buffer_size,options.tempdirs)
