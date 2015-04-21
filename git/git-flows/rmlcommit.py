import subprocess
import os

cmd = "git reset --hard HEAD^"

subprocess.call(cmd.split(' '))