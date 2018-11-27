#!/usr/bin/env python

import sys
import re
import json
from urllib.parse import urlparse
from urllib.request import urlopen

def pull_url_to_api_url(url):
    u = urlparse(url)
    
    if not re.match('github.com', u.netloc):
        raise Exception('not a github url')
    comps = u.path.split('/')
    comps = comps[1:]
    if len(comps) < 4 or comps[2] != 'pull':
        raise Exception('not a github pr url')
    
    user = comps[0]
    project = comps[1]
    pr_id = comps[3]
    return 'https://api.github.com/repos/' + user + '/' + project + '/pulls/' + pr_id + '/comments'

def hunk_to_pat(hunk):
    keep = []
    st = None 
    for l in hunk.split('\n'):
        if l == ' ':
            keep.append('')
        elif l[0] == ' ':
            keep.append(l[1:])
        elif len(l) > 0 and l[0] == '+':
            keep.append(l[1:])
        elif len(l) > 1 and l[0:2] == '@@':
            m = re.search('@@ -(\d+),', l)
            st = int(m.group(1)) if m else None 
    return keep, st 

def hunk_to_line(hunk, filename):
    pat, start = hunk_to_pat(hunk)
    line_count = 0
    match_len = 0
    try:
        with open(filename, 'r') as f:
            for line in f:
                line_count += 1
                if line_count < start - 3:
                    continue
                if match_len == len(pat) - 1:
                    return line_count
                if line.rstrip() == pat[match_len]:
                    match_len += 1
                else:
                    match_len = 0
    except:
        pass
    return None

pull_url = sys.argv[1]
comments = json.load(urlopen(pull_url_to_api_url(pull_url)))
for c in comments:
    line = hunk_to_line(c['diff_hunk'], c['path'])
    line = line if line else 0
    print('%s:%d: %s'%(c['path'], line, c['body']))

