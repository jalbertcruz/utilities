#!/usr/bin/python3.5

import subprocess
import os
from pathlib import Path

home_backup = 1 == 11

# concrete_paths = []
#
# prefix = '/home/j/Downloads/aa/'
# destination = '/home/j/Downloads/aa/result/'
#
# paths = ['bower_components/summernote/dist/', 'bower_components/knockout/']

home_files = []
if home_backup:
    concrete_paths = []
    excluded_paths = ['src/dbs']

    prefix = '/home/j/'
    destination = '/run/media/j/Medias/BFS/10-16/home/'

    paths = ['.android/', '.AndroidStudio2.2/', 'appslnx/', 'code/', '.config/git/', 'Desktop/', 'Downloads/', '.m2/',
             '.lein/', '.ivy2/', '.gradle/',
             '.mozilla/', '.npm/', '.sbt/', 'src/', '.ssh/', '.vim/', '.zprezto/', '.emacs.d/', '.pub-cache/']

    home_files = ['.zhistory', '.viminfo', '.spacemacs', '.gitconfig', '.bash_history', '.tmux.conf', '.vimrc',
                  '.bashrc']
else:
    concrete_paths = ['Literature', 'ff']
    excluded_paths = []

    prefix = '/home/datos/'
    destination = '/run/media/j/Medias/BFS/10-16/d/'

    paths = ['docs/', 'docs/P/PLs/Varied', 'docs/SWE/', 'docs/AI/', 'docs/OSs/',
             'mdocs/', 'mdocs/teaching/', 'installers/']

    concrete_paths = ['ff']

if home_backup:
    extended_paths = set(paths)
else:
    extended_paths = []
    for p in paths:
        l = p.split('/')[:-1]
        for i in range(len(l)):
            extended_paths.append(l[:i + 1])

    extended_paths = {'/'.join(a) + '/' for a in extended_paths}

os.chdir(prefix)

if home_backup:
    for f in home_files:
        if not Path(destination + f).exists():
            subprocess.run(['cp', f, destination], check=True)

for p in concrete_paths:
    if not Path(destination + p + '.tar').exists():
        subprocess.run(['tar', '-cvf', destination + p + '.tar', p], check=True)

full_paths = {prefix + x[:-1] for x in extended_paths}

for p in extended_paths:
    if not Path(destination + p).exists():
        os.makedirs(destination + p)
    os.chdir(prefix + p)
    dirs = [x for x in Path('.').iterdir() if x.is_dir()]
    files = [x for x in Path('.').iterdir() if x.is_file()]
    for d in dirs:
        if (prefix + p + d.name) not in full_paths:
            if not Path(destination + p + d.name + '.tar').exists() \
                    and (p + d.name) not in excluded_paths:
                subprocess.run(['tar', '-cvf', destination + p + d.name + '.tar', d.name], check=True)
    for f in files:
        if not Path(destination + p + f.name).exists():
            subprocess.run(['cp', f.name, destination + p], check=True)
