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
import json
import time


class RepoCommitsTool:
    def __init__(self, path="."):
        self.path = path
        self.r = git.Repo(path)

    def commits_in(self, path):
        return self.r.iter_commits(paths=path)

    def commits(self):
        return self.r.iter_commits()

    def dirs(self):
        return json.loads("".join(open(os.path.join(self.path, 'config/mirrors.json')).readlines())).keys()

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

    def check_commits_in_dir(self):
        if not self.is_consistent():
            print("The commits must be over only one project")
            cmd = "git reset --mixed HEAD^"
            subprocess.call(cmd.split(' '))

    def check_sync(self, dest, k):
        origin_commits = list(self.commits_in(k))
        ncom_origin = len(origin_commits)
        dest_commits = list(dest.commits_in(k))
        ncom_dest = len(dest_commits)

        origin_commits.sort(key=lambda x: x.authored_date, reverse=True)
        dest_commits.sort(key=lambda x: x.authored_date, reverse=True)

        if self.active_branch() != dest.active_branch():
            res = (1, None)
        else:
            if ncom_origin == ncom_dest:
                res = (2, None)
            else:
                if ncom_origin < ncom_dest:
                    res = (3, None)
                else:
                    res = (4, [ncom_origin, ncom_dest])
        if res[0] != 1:
            n = min(ncom_dest, ncom_origin)
            origin_commits = origin_commits[ncom_origin - n:]
            dest_commits = dest_commits[ncom_dest - n:]
            i = n - 1
            flag = True
            while i > -1 and flag:
                # if origin_commits[i].committed_date != dest_commits[i].committed_date:
                if origin_commits[i].authored_date != dest_commits[i].authored_date:
                    flag = False
                    res = (5, origin_commits[i], dest_commits[i])
                else:
                    i -= 1
        return res


class SingleGitRepoFlow:
    @staticmethod
    def gsync(config):
        """ Utlidad orientada a automatizar la sincronizacion de multiples repos git locales-privados
            con un repo git central-publico. (tiene que existir al menos un commit en cada repo)
        """
        for k in config.keys():
            origin = RepoCommitsTool()
            dest = RepoCommitsTool(config[k])

            res = origin.check_sync(dest, k)

            def st_same_branch():
                print("Different active_branch in: " + k)

            def st_in_sync():
                print("Already in sync in: " + k)

            def st_origin_outdated():
                print("Origin outdated in: " + k)

            def st_ok():
                diff = res[1][0] - res[1][1]
                commits = list(origin.commits_in(k))[:diff]
                num = 1
                commits.reverse()
                print()
                print("Creating patchs from: " + k)
                for com in commits:
                    subprocess.call(
                        ["git", "format-patch", "-1", com.hexsha, "-o", "new-commits-" + k.replace('/', '-'),
                         "-s", "--start-number",
                         str(num)])
                    num += 1

            def st_different_history():
                print("Different history in: " + k)
                print("First different datetime in origin at", res[1].hexsha)
                print(time.ctime(res[1].authored_date), "/", time.ctime(res[2].authored_date))
                print("Origin:", res[1].message, "vs", "\nDest:", res[2].message)

            cases = {
                1: st_same_branch,
                2: st_in_sync,
                3: st_origin_outdated,
                4: st_ok,
                5: st_different_history
            }

            cases[res[0]]()