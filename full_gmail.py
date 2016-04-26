#!/usr/bin/env python

import sys
from urllib.request import FancyURLopener
import xml.etree.ElementTree as ET
import argparse


parser = argparse.ArgumentParser(description = 'Read Gmail Account messages per RSS')
parser.add_argument('username', metavar='Username', action='store', help='GMail username (@gmail.com can be omitted)')
parser.add_argument('password', metavar='Password',action='store', help='GMail password or the device password')
parser.add_argument('--conky', dest='conky', action='store_true', help='conky-friendly output')


args = parser.parse_args()

email = args.username
password = args.password
ns = '{http://purl.org/atom/ns#}'
url = 'https://%s:%s@mail.google.com/mail/feed/atom' % (email, password)


opener = FancyURLopener()
page = opener.open(url)

contents = page.read().decode('utf-8')
#auth_handler = urllib.request.HTTPBasicAuthHandler()
#auth_handler.add_password(realm='https://mail.google.com/',
#                          uri='https://mail.google.com/',
#                          user=email,
#                          password=password)
#opener = urllib.request.build_opener(auth_handler)
#urllib.request.install_opener(opener)

ifrom = contents.index('<fullcount>') + 11
ito   = contents.index('</fullcount>')

fullcount = contents[ifrom:ito]

root = ET.fromstring(contents)

if int(fullcount) == 1:
    msg = '1 new message in ' + '${color #ff6600}' + email + '${color}\n'
else:
    msg = fullcount + ' new messages in ' + '${color #ff6600}' + email + '${color}\n'

print(msg)


for entry in root.findall(ns + 'entry'):
    title = entry.findtext(ns + 'title')[:50]
    author = entry.find(ns + 'author')
    author_name = author.findtext(ns + 'name')[:20]
    author_email = author.findtext(ns + 'email')[:25]
    if args.conky:
        line = title
        line += '${goto 350}'
        line += author_name
        line += '${goto 500}'
        line += author_email
    else:
        line = '\'' + title + '\' from ' + author_name + ' (' + author_email + ')'
    print(line)

