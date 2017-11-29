#!/usr/bin/python3

# TODO: use url = 'https://%s:%s@mail.google.com/mail/feed/atom' % (email, password)
# see conky !aw

import imaplib
import email
import sys
import configparser
import os.path
from email.parser import HeaderParser
from email.header import decode_header
from hashlib import sha512
import subprocess


CONFIGFILE = os.path.expanduser('~') + '/.config/scripts/mailcheck.ini'
notified_file = '/home/spotlight/.config/mailcheck/notified'
parser = HeaderParser()

def check_notified(hash):
    directory = os.path.split(notified_file)[0]
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(notified_file):
        with open(notified_file, 'x'):
            pass

    with open(notified_file, 'r+') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == hash:
                return True
        return False


def write_hash(hash):
    with open(notified_file, 'a+') as f:
        f.write(hash+"\n")

def checknew(imap, messages):
    for i in messages:
        result, data = imap.fetch(str(i), '(BODY.PEEK[HEADER])')
        for response in data:
            if isinstance(response, tuple):
                header_data = response[1]
                try: # email only works on strings, not bytes
                    header_data = header_data.decode('utf-8')
                except:
                    pass
                header = parser.parsestr(header_data)
                subject = decode_header(header['Subject'])[0][0]
                sender = decode_header(header['From'])
                msg_id = decode_header(header['Message-Id'])[0][0]
                msg_id = msg_id.encode('utf-8')
                msg_id_hash = sha512(msg_id).hexdigest()
                try:
                    sender_email = sender[0][0].split('<')[1].split('>')[0]
                except:
                    sender_email = sender[0][0] # what'ev
                if not check_notified(msg_id_hash):
                    subprocess.call(["notify-send", sender_email, subject])
                    write_hash(msg_id_hash)
                else:
                    return



def getnewmails(host, user, pw):
    imaplib.socket.setdefaulttimeout(2)
    imap = imaplib.IMAP4_SSL(host)
    imap.login(user, pw)
    imap.select('inbox')
    result, data = imap.search(None, "NOT SEEN")
    data = data[0].decode('ascii')
    try:
        messages = data.split(" ")
    except:
        print("error while decoding/parsing messages")
        imap.close()
        imap.logout()

    if len(messages) == 1 and messages[0]=='':
        return 0
    else:
        checknew(imap, messages)
        return len(messages)


if __name__ == '__main__':
    width = 1920
    try:
        output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4 | cut -d "x" -f1',shell=True, stdout=subprocess.PIPE).communicate()[0]
        width = int(output)
    except:
        pass

    config = configparser.ConfigParser()
    config.read(CONFIGFILE)
    output_type = config.get('General', 'output', fallback='conky')

    output = ''
    for section in config.sections():
        if section in ['General']:
            continue
        server = config.get(section, 'server', fallback='')
        login = config.get(section, 'login', fallback='')
        password = config.get(section, 'password', fallback='')
        new_mails = 0
        try:
            new_mails = getnewmails(server, login, password)
        except Exception as e:
            new_mails = -1


        if output_type == 'conky':
            conky_pos = config.get(section, 'conky_pos' + str(width), fallback='')
            if not server or not login or not password or not conky_pos:
                continue
            output += '${goto '+conky_pos+'}' + str(new_mails)
        elif output_type == 'polybar':
            prefix = config.get(section, 'prefix', fallback=section)
            output += '%s %d    ' % (prefix, new_mails)
        else:
            assert False, 'Output "%s" not supported!' % output_type
    print(output)
