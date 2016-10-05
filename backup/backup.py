#!/usr/bin/python3.5

import subprocess
import os
from pathlib import Path

home_backup = 1 == 1

# concrete_paths = []
#
# prefix = '/home/j/Downloads/aa/'
# destination = '/home/j/Downloads/aa/result/'
#
# paths = ['bower_components/summernote/dist/', 'bower_components/knockout/']

if home_backup:
    concrete_paths = []
    excluded_paths = ['src/dbs/']
    prefix = '/home/j/'
    destination = '/run/media/j/Medias/BFS/10-16/home/'
    init_paths = ['.android/', '.AndroidStudio2.2/', 'appslnx/google/', 'appslnx/jetbrains/', 'code/', '.config/git/',
                  'Desktop/', 'Downloads/', '.m2/', '.lein/', '.ivy2/', '.gradle/', '.mozilla/',
                  '.npm/', '.sbt/', 'src/', '.ssh/', '.vim/', '.zprezto/', '.emacs.d/', '.pub-cache/']
    just_files = ['.zhistory', '.viminfo', '.spacemacs', '.gitconfig', '.bash_history',
                  '.tmux.conf', '.vimrc', '.bashrc']
else:
    concrete_paths = ['Literature/', 'ff/']
    excluded_paths = []
    prefix = '/home/datos/'
    destination = '/run/media/j/Medias/BFS/10-16/d/'
    init_paths = ['docs/', 'docs/P/PLs/Varied/', 'docs/P/PLs/Varied/C#/Basics/', 'docs/SWE/',
                  'docs/AI/', 'docs/OSs/', 'mdocs/', 'mdocs/teaching/', 'mdocs/docencia/Postgrados/', 'installers/']
    concrete_paths = ['ff/']
    just_files = []

if home_backup:
    all_paths = set(init_paths)
else:
    all_paths = []
    for p in init_paths:
        l = p.split('/')[:-1]
        for i in range(len(l)):
            all_paths.append(l[:i + 1])

    all_paths = {'{}/'.format('/'.join(a))
                 for a in all_paths}

os.chdir(prefix)

if home_backup:
    for f in just_files:
        if not Path('{}{}'.format(destination, f)).exists():
            subprocess.run(['cp', f, destination], check=True)

for p in concrete_paths:
    new_tar = '{}{}.tar'.format(destination, p[:-1])
    if not Path(new_tar).exists():
        subprocess.run(['tar', '-cvf', new_tar, p], check=True)

full_paths = {'{}{}'.format(prefix, x)
              for x in all_paths}

for p in all_paths:
    current_target_path = '{}{}'.format(destination, p)
    if not Path(current_target_path).exists():
        os.makedirs(current_target_path)
    new_dir = '{}{}'.format(prefix, p)
    os.chdir(new_dir)
    dirs = [x for x in Path('.').iterdir() if x.is_dir()]
    files = [x for x in Path('.').iterdir() if x.is_file()]
    for e in dirs:
        if ('{}{}/'.format(new_dir, e.name)) not in full_paths:
            new_tar = '{}{}.tar'.format(current_target_path, e.name)
            if not Path(new_tar).exists() \
                    and ('{}{}/'.format(p, e.name)) not in excluded_paths:
                subprocess.run(['tar', '-cvf', new_tar, e.name], check=True)
    for e in files:
        if not Path('{}{}'.format(current_target_path, e.name)).exists():
            subprocess.run(['cp', e.name, current_target_path], check=True)
