# Author José Albert Cruz Almaguer <jalbertcruz@gmail.com>
# Copyright 2016 by José Albert Cruz Almaguer.
#
# This program is licensed to you under the terms of version 3 of the
# GNU Affero General Public License. This program is distributed WITHOUT
# ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING THOSE OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. Please refer to the
# AGPL (http:www.gnu.org/licenses/agpl-3.0.txt) for more details.

import sys

lns = ["{} {}".format(sys.argv[2], l)
       for l in open(sys.argv[1]).readlines()]

print('\n'.join(map(lambda l: l.rstrip(), lns)) + '\n' * 2 + open(sys.argv[3]).read(), end='')
