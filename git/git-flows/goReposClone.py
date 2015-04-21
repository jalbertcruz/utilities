import subprocess
import codecs
import re

# subprocess.check_call(["git", "clone", 'https://github.com/jalbertcruz/erlEA'])

import urllib.request

# resp = urllib.request.urlopen('http://go-lang.cat-v.org/pure-go-libs')
#
# data = resp.read()
# text = data.decode('utf-8')
#
# from bs4 import BeautifulSoup
#
# soup = BeautifulSoup(text)
#
#
#
# codecs.open('rps.txt', encoding='utf-8', mode='w').write("\n".join([str(a) for a in soup.find_all('a')]))

lns = codecs.open('rps.txt', encoding='utf-8').readlines()

p = re.compile('href=\"(.+)\"')
# for l in soup.find_all('a'):
for l in lns:
    m = p.search(l)
    if m:
        a = m.group(1)
        if a.startswith('http:'):
            a = 'https:' + a[5:]

        if 'code.google' in a:
            # print('google: ', a)
            pass
        elif 'github.com' in a:
            # subprocess.check_call(["git", "clone", a])
            # print('git:', a)
            pass

            # p = re.compile('(a)b')
            # m = p.match('ab')
            # print(m.group(0))