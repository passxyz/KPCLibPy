#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import sys
from prettytable import PrettyTable
sys.path.append("../src")

from commands.keepass import KeePass, IStatusLogger, get_homepath, lsdb

class ShowWarningsLogger(IStatusLogger):
    __namespace__ = "KPCLibPy"
    
    def StartLogging(self, strOperation, bWriteOperationToLog):
        print('StartLogging {} {}'.format(strOperation, bWriteOperationToLog))
        return
    def EndLogging(self):
        print('EndLogging')
        return
    def SetProgress(self, uPercent):
        #print('In progress {}'.format(uPercent))
        return True
    def SetText(self, strNewText, lsType):
        print('SetText {} {}'.format(strNewText, lsType))
        return True
    def ContinueWork(self):
        return True

def print_group(group, detail=False):
    if detail:
        s_table = PrettyTable(["Time", "Type", "Name"])
        for gp in group.Groups:
            s_table.add_row([gp.LastModificationTime.ToString(), "Group", gp.get_Name()])
        for entry in group.Entries:
            s_table.add_row([entry.LastModificationTime.ToString(), "Entry", entry.Strings.ReadSafe("Title")])
    else:
        s_table = PrettyTable(["Name"])
        for gp in group.Groups:
            s_table.add_row([gp.get_Name()+"/"])
        for entry in group.Entries:
            s_table.add_row([entry.Strings.ReadSafe("Title")])

    s_table.align = "l"
    s_table.border = False
    s_table.header = False
    print("Current group is {}.\n".format(group))
    print(s_table)

if __name__ == '__main__':
    _keepass = KeePass()
    logger = ShowWarningsLogger()
    db_path = get_homepath() + '/' + "utdb.kdbx"
    _keepass.open(db_path, "12345", logger)
    print_group(_keepass.root_group)
