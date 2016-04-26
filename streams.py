#!/usr/bin/python2

import urllib as ul
import json
import argparse
from unicodedata import normalize


parser = argparse.ArgumentParser(description='Retrieves live CS:GO Streams')
parser.add_argument('--verbose', '-v', help='Use verbose output', action='store_true')
parser.add_argument('--conky', '-c', help='Formats the output conky-friendly', action='store_true')
parser.add_argument('--delimiter', '-d', help='Prints the output separated by the given argument', metavar='CHAR', default='|')
parser.add_argument('--limit', '-l', help='Limits the output to $n streams', metavar='INT', default='0')
parser.add_argument('--minimal', '-m', help='Minimal viewer count', metavar='INT', default='50')
parser.add_argument('--title', '-t', help='Print the title of the streams aswell', action='store_true')
args = parser.parse_args()


def sanitizeConky(title, name):
    strings = [title, name]
    for i in range(0,len(strings)):
        strings[i] = strings[i].replace("$", "$$")
        strings[i] = strings[i].replace("#", "\#")
    return strings[0], strings[1]

def colorConky(name,viewer):
    str="${color "
    if name in ['tarik_tv','summit1g', 'g5taz', 'meclipse']:
        str += "ff9900"
    else:
        if viewer > 10000:
            str += "cc3300"
        else:
            return "${color0}"
    str += "}"

    return str


if args.verbose:
    print "[**] Open URL"
response = ul.urlopen('https://api.twitch.tv/kraken/streams?game=Counter-Strike%3A%20Global%20Offensive')
if args.verbose:
    print "[**] Read HTMl"
html = response.read().decode('utf-8')
html = normalize('NFKD', html).encode('ascii', 'ignore')

if args.verbose:
    print "[**] Parse Streams"
j = json.loads(html)
streams = j['streams']
i = 0
if args.verbose:
    print "[**] Limit: "+args.limit
    print "[**] Minimal Viewercount: "+args.minimal
if args.conky:
    print "${font}"
sep = args.delimiter
for stream in streams:
    if int(args.limit) != 0:
        i+=1
        if i > int(args.limit):
            break
    channel = stream['channel']
    viewers = stream['viewers']
    if viewers < int(args.minimal):
        continue
    title = channel['status'].encode('utf-8')
    name = channel['name'].encode('utf-8')
    if args.conky:
        title, name = sanitizeConky(title, name)
        print colorConky(name,viewers)+"${font}"+name[:20] + "${font Liberation Sans:bold:size=10}${goto 130}${color3}" +str(viewers) +"${color0}${font}${goto 200}"+title[:30]
        continue
    if args.verbose:
        print name+": "+title[:50]+" ["+str(viewers)+"]"
    else:
        print name+sep+str(viewers)
