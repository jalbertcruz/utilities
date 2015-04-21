#!/usr/bin/env python

# File for hook: post-commit

#
# Author José Albert Cruz Almaguer <jalbertcruz@gmail.com>
# Copyright 2015 by José Albert Cruz Almaguer.
#
# This program is licensed to you under the terms of version 3 of the
# GNU Affero General Public License. This program is distributed WITHOUT
# ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING THOSE OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. Please refer to the
# AGPL (http:www.gnu.org/licenses/agpl-3.0.txt) for more details.

import subprocess
import os
import pyperclip

origin = "."
commitsFolder = "commitsTemp"

os.chdir(origin)

commitsCount = "git rev-list --count HEAD"
commitsCount = int(subprocess.check_output(commitsCount.split(' ')))
commitsGeneration = "git format-patch -{0!s} -o {1} -s".format(commitsCount, commitsFolder)

"git format-patch -1 <commit hex number> -o aa -s" # Hace un patch a partir del commit con dicho numero
"git format-patch -1 -o aa -s" # Hace un patch a partir del commit con dicho numero

subprocess.call(commitsGeneration.split(' '))

destination = "c:/Users/jalbert/Downloads/temp/repoCentral"

os.chdir(destination)

applyAllPatches = "git am {0}/*".format(commitsFolder)
# subprocess.call(applyAllPatches.split(' '))# Works in bash, not in cmd (solo sirve para Linux)
pyperclip.copy(applyAllPatches)

# Uso:
# 1. Lo anterior para la primera vez
# 2. A partir de este momento seguir el siguiente flujo:
#    * En el repo secundario (en su master está la versión ya incluida en el repo principal):
#        - trabajo en una nueva rama:
#               $> git checkout -b development
#                - hago los commits que sean necesarios:
#                       $> git add .
#                       $> git commit -m "commit n"
#        - creo los patchs a pasar al repo principal:
#               $> git format-patch master..development -o new-commits -s
#        - actualizo el master
#            $> git checkout master
#            $> git merge development
#        - elimino la rama
#            $> git branch -d development
#
#    * En el repo principal (actualizo):
#       $> git am new-commits/*

# Para configurar los datos personales:
# $> git config --global user.name "John Doe"
# $> git config --global user.email johndoe@example.com

# git reset --hard HEAD^