#!/usr/bin/python3

# mostly copied from https://gist.github.com/bshillingford/6259986edca707ca58dd
import requests
import lxml.html as html
import re
import urllib
import os, sys, subprocess, os.path
import atexit
import tempfile
import argparse
import configparser
import fnmatch
import shutil


query = None #"http://arxiv.org/abs/1511.08228"
kindle_email = None #'ADDRESS_HERE@kindle.com'
gmail_acc = None #'ADDRESS_HERE@gmail.com'
gmail_pw = None #getpass.getpass()

clean_at_exit = False


# paper settings (decrease width/height to increase font)
landscape = True
width = "6in"
height = "4in"
margin = "0.2in"
# settings for latex geometry package:
if landscape:
    geom_settings = dict(paperwidth=width, paperheight=height, margin=margin)
else:
    geom_settings = dict(paperwidth=height, paperheight=width, margin=margin)


def delete_tmp(dir):
    if clean_at_exit:
        print("Clean temporary directory (" + dir + ")")
        shutil.rmtree(dir)

def parseArxivId(query):
    # parse arxiv id with magic
    arxiv_id = re.match(r'(https?://.*?/)?(?P<id>\d{4}\.\d{4,5}(v\d{1,2})?)', query).group('id')
    arxiv_abs = 'https://arxiv.org/abs/' + arxiv_id
    arxiv_pdf = 'https://arxiv.org/pdf/' + arxiv_id
    arxiv_pgtitle = html.fromstring(requests.get(arxiv_abs).text.encode('utf8')).xpath('/html/head/title/text()')[0]
    arxiv_title = re.sub(r'\s+', ' ', re.sub(r'^\[[^]]+\]\s*', '', arxiv_pgtitle), re.DOTALL)
    arxiv_title_scrubbed = re.sub('[^-_A-Za-z0-9]+', '_', arxiv_title, re.DOTALL)

    return (arxiv_id, arxiv_title, arxiv_title_scrubbed)


def progresshook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def retrieveSources(arxiv_id):
    tmp_dir = tempfile.mkdtemp(prefix='arxiv2kindle_')
    atexit.register(delete_tmp, dir=tmp_dir)

    url = 'http://arxiv.org/e-print/' + arxiv_id
    print("Downloading arxiv e-print")
    urllib.request.urlretrieve(url, os.path.join(tmp_dir, 'src.tar.gz'), progresshook)
    print(tmp_dir)

    try: 
        subprocess.check_call(['tar', 'xf', 'src.tar.gz'], cwd = tmp_dir)
    except subprocess.CalledProcessError as e:
        print("tar returned " + str(e.returncode))
        shutil.rmtree(tmp_dir)
        sys.exit(1)
    except Exception as e:
        print("error occured:")
        print(e)
        shutil.rmtree(tmp_dir)
        sys.exit(1)
    return tmp_dir


def compileEPrint(tmp_dir):
    src = None
    doc_texfile = None
    docline = 0
    os.chdir(tmp_dir)
    for file in os.listdir(tmp_dir):
        if fnmatch.fnmatch(file, '*.tex'):
            print('try: ' + file)
            with open(file, 'r') as f:
                src = f.readlines()
            linecount = 0
            docs = [count for count, line in enumerate(src[0:30]) if 'documentclass' in line]
            print(docs)
            if docs:
                doc_texfile = file
                docline = docs[0]
                break


    print('correct texfile: ' + doc_texfile)
    # # filter comments/newlines for easier debugging:
    # src = [line for line in src if line[0] != '%' and len(line.strip()) > 0]

    # strip font size, column stuff, and paper size stuff in documentclass line:
    print(docline)
    src[docline] = re.sub(r'\b\d+pt\b', '', src[docline])
    src[docline] = re.sub(r'\b\w+column\b', '', src[docline])
    src[docline] = re.sub(r'\b\w+paper\b', '', src[docline])
    src[docline] = re.sub(r'(?<=\[),', '', src[docline]) # remove extraneous starting commas
    src[docline] = re.sub(r',(?=[\],])', '', src[docline]) # remove extraneous middle/ending commas


    # find begin{document}:
    print(src[0:5])
    begindocs = [i for i, line in enumerate(src) if line.strip().startswith(r'\begin{document}')]
    print(begindocs)
    assert(len(begindocs) == 1)
    src.insert(begindocs[0], '\\usepackage['+','.join(k+'='+v for k,v in geom_settings.items())+']{geometry}\n')
    src.insert(begindocs[0], '\\usepackage{times}\n')
    src.insert(begindocs[0], '\\pagestyle{empty}\n')
    if landscape:
        src.insert(begindocs[0], '\\usepackage{pdflscape}\n')

    # shrink figures to be at most the size of the page:
    for i in range(len(src)):
        line = src[i]
        m = re.search(r'\\includegraphics\[width=([.\d]+)\\(line|text)width\]', line)
        if m:
            mul = m.group(1)
            src[i] = re.sub(r'\\includegraphics\[width=([.\d]+)\\(line|text)width\]',
                       r'\\includegraphics[width={mul}\\textwidth,height={mul}\\textheight,keepaspectratio]'.format(mul=mul),
                       line)
    os.rename(doc_texfile, doc_texfile+'.bak')
    with open(doc_texfile, 'w') as f:
        f.writelines(src)


    for x in range(3): # 3 wishes
        print("Compiling latex file #"+str(x)+"/2")
        run = subprocess.call(['pdflatex', '-interaction' , 'batchmode', doc_texfile], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    pdffilename = os.path.splitext(doc_texfile)[0] + '.pdf'
    return os.path.join(tmp_dir, pdffilename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Send compiled Arxiv papers to kindle device')
    parser.add_argument('query', metavar='Query', action='store', help='Arxiv query, URL or Arxiv-ID')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.secrets'))
    kindle_email = config['arxiv-kindle']['kindle_email']
    gmail_acc = config['arxiv-kindle']['gmail_acc']
    gmail_pw = config['arxiv-kindle']['gmail_pw']
    pdf_dir = config['arxiv-kindle']['pdf_dir']

    parsed = parseArxivId(args.query)
    tmp_dir = retrieveSources(parsed[0])
    pdffile = compileEPrint(tmp_dir)

    print("copied to " + os.path.join(pdf_dir, parsed[0] + '_' + parsed[2] + '.pdf'))
    shutil.copyfile(pdffile, os.path.join(pdf_dir, parsed[0] + '_' + parsed[2] + '.pdf'))
    shutil.rmtree(tmp_dir)


    # print("output pdf: " + pdffile)
# sendAttachedEmail(pdffilename, kindle, acc, pass)

