# Author José Albert Cruz Almaguer <jalbertcruz@gmail.com>
# Copyright 2018 by José Albert Cruz Almaguer.
#
# This program is licensed to you under the terms of version 3 of the
# GNU Affero General Public License. This program is distributed WITHOUT
# ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING THOSE OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. Please refer to the
# AGPL (http:www.gnu.org/licenses/agpl-3.0.txt) for more details.

import re
import sys

secrets = "".join(open("secrets.json").readlines())
secrets = eval(secrets)
current_file_content = "".join(open(sys.argv[1]).readlines())

for k in secrets.keys():
    current_file_content = re.sub("({})(\s*)=(.*)".format(k)
                                  , "{}=\"**SECRET**\"".format(k),
                                  current_file_content)

print(current_file_content, end='')
