#!/usr/bin/env python

import sys, os, re, json, requests
from urllib.parse import urlparse

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

def hunk_to_line(hunk):
    first = hunk.splitlines()[0]
    m = re.search(r'@@ -\d+,\d+ \+(\d+),(\d+) @@', first)
    if m:
        return int(int(m.group(1)) + 0.5 * int(m.group(2)))

if __name__ == '__main__':
    token = os.environ["GITHUB_TOKEN"]
    pull_url = sys.argv[1]
    api_url = pull_url_to_api_url(pull_url)
    comments = requests.get(api_url,
            headers={
                'Authorization': f'Bearer {token}',
                'Accept': 'application/vnd.github+json',
            }).json()
    for c in comments:
        if c.get('in_reply_to_id'):
            continue
        line = c.get('original_line') or c.get('original_start_line')
        if not line:
            line = hunk_to_line(c['diff_hunk']) or 0
        body = c['body']
        body = re.sub(r'[\r]+', '', c['body'])
        print('%s:%d: %s'%(c['path'], line, body))
