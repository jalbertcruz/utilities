import subprocess
from subprocess import CalledProcessError

import os
import sys

os.chdir("../../goEA/src/mainEA/")

res = []
file = open('err.txt', 'w')
for i in range(1000):
    try:
        subprocess.check_output(["mainEA.exe", "parce"], universal_newlines=True, stderr=file)
    except CalledProcessError as e:
        sys.exit(1)
