#!/usr/bin/python3.5

import re
import subprocess

a = subprocess.run(["lsof", "-wni", "tcp:8080"], universal_newlines=True, stdout=subprocess.PIPE)

l = a.stdout.split('\n')

for e in l[1:]:
    rows = re.split(' +', e)
    if len(rows) > 1:
        pid = rows[1]
        subprocess.run(["kill", "-9", pid])
