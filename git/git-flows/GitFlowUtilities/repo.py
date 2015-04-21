#
# Author José Albert Cruz Almaguer <jalbertcruz@gmail.com>
# Copyright 2015 by José Albert Cruz Almaguer.
#
# This program is licensed to you under the terms of version 3 of the
# GNU Affero General Public License. This program is distributed WITHOUT
# ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING THOSE OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. Please refer to the
# AGPL (http:www.gnu.org/licenses/agpl-3.0.txt) for more details.

import git
import os
import subprocess


class RepoCommitsTool:
    def __init__(self, path="."):
        self.r = git.Repo(path)

    def commits_in(self, path):
        # prefix = 'commit '
        # return [l[len(prefix):] for l in self.r.git.log(path).split("\n") if l.startswith(prefix)]
        return self.r.iter_commits(paths=path)

    def commits(self):
        # return self.commits_in(".")
        return self.r.iter_commits()

    @staticmethod
    def dirs():
        return [f for f in os.listdir(".") if os.path.isdir(f) and not f.startswith('.')]

    def is_consistent(self):
        dirs_commits = [set([c.hexsha for c in self.commits_in(a)]) for a in self.dirs()]
        all_commits = [c.hexsha for c in self.commits()]
        for a in all_commits:
            trues = [True for b in dirs_commits if a in b]
            if len(trues) > 1:
                return False
        return True

    def active_branch(self):
        return self.r.active_branch

    def number_of_commits(self):
        return len(list(self.commits()))

    def number_of_commits_in(self, path):
        return len(list(self.commits_in(path)))

    def check_commits_in_dir(self):
        if not self.is_consistent():
            print("The commits must be over only one project")
            cmd = "git reset --mixed HEAD^"
            subprocess.call(cmd.split(' '))


class SingleGitRepoFlow:
    @staticmethod
    def gsync(config):
        """ Utlidad orientada a automatizar la sincronizacion de multiples repos git locales-privados
        con un repo git central-publico.
        Ambos repos se sincronizan a partir del commit 2 (tiene que existir un commit inicial)
        """
        for k in config.keys():
            origin = RepoCommitsTool()
            dest = RepoCommitsTool(config[k])
            ncom_origin = origin.number_of_commits_in(k)
            ncom_dest = dest.number_of_commits_in(k)

            if origin.active_branch() != dest.active_branch():
                print("Diferent active_branch in: " + k)
            else:
                if ncom_origin == ncom_dest:
                    print("Already in sync in: " + k)
                else:
                    if ncom_origin < ncom_dest:
                        print("Origin outdated in: " + k)
                    else:
                        diff = ncom_origin - ncom_dest
                        commits = list(origin.commits_in(k))[:diff]
                        num = 1
                        commits.reverse()
                        print("Creating patchs for: " + k)
                        for com in commits:
                            subprocess.call(
                                ["git", "format-patch", "-1", com.hexsha, "-o", k + "-new-commits", "-s",
                                 "--start-number",
                                 str(num)])
                            num += 1