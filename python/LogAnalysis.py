import re, getopt, sys #re for regex, getopt for options, sys for argv
import operator  #may not need. holding as a reference though

def usage():
    print("USAGE RESULT")

try:
    opts, args = getopt.getopt(sys.argv[1:], ':hs:e:t:', ['help', 'start=', 'end=', 'keywords='])
except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit(2)

for opt, a in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-s', '--start'):
        start_line = arg
    elif opt in ('-e', '--end'):
        end_line = arg
    elif opt in ('-t', '--keywords'):
        sys.exit(2)
    # need to work out syntax here
    else:
        assert False, "unhandled option"

args = str(sys.argv)
print ("Args passed: %s " % args)
