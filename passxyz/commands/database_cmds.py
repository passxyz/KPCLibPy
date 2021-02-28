#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import typing
from pathlib import *
from prettytable import PrettyTable
from termcolor import cprint, colored
from nubia import command, argument, context
from commands.keepass import IStatusLogger, get_homepath, lsdb
#from KeePassLib import PwGroup, PwEntry, Collections


class ShowWarningsLogger(IStatusLogger):
    __namespace__ = "KPCLibPyTest1"
    
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


@command
def edit():
    "Edit an etnry or group"
    return None

@command("export")
def export_db():
    "Export entries to a new database"
    return None

@command("import")
def import_db():
    "Import another database to the current one"
    return None

@command
def mv():
    "Move an entry or group to a new location"
    return None


@command
def rename():
    "Rename a group or entry"
    return None


@command
def version():
    "Display version number"
    ctx = context.get_context()
    cprint("Version {}".format(ctx.version))


@command
def save():
    """
    Save te database to disk
    """
    ctx = context.get_context()
    db = ctx.keepass.db

    if ctx.keepass.is_open():
        logger = ShowWarningsLogger()
        db.Save(logger)


@command("show")
@argument("items", type=str, description="Database configuration, version etc.",
    choices=["configuration", "version", "database"])
def show(items="database"):
    """
    This command shows the information of the current databases.
    """
    ctx = context.get_context()
    db = ctx.keepass.db

    if items == "database":
        if ctx.keepass.is_open():
            db_table = PrettyTable(["Property", "Value"])
            db_table.align = "l"

            db_table.add_row([colored("Database name", "magenta"), db.Name])
            db_table.add_row([colored("DefaultUserName", "magenta"), db.DefaultUserName])
            db_table.add_row([colored("Modified", "magenta"), db.Modified])
            db_table.add_row([colored("RecycleBinEnabled", "magenta"), db.RecycleBinEnabled])
            db_table.add_row([colored("HistoryMaxItems", "magenta"), db.HistoryMaxItems])
            db_table.add_row([colored("HistoryMaxSize", "magenta"), db.HistoryMaxSize])
            db_table.add_row([colored("Description", "magenta"), db.Description])
            db_table.add_row([colored("MaintenanceHistoryDays", "magenta"), db.MaintenanceHistoryDays])
            cprint("Database configureation", "yellow")
            print(db_table)
        else:
            cprint("Database is closed", "red")
    elif items == "version":
        cprint("Version {}".format(ctx.version))
    elif items == "configuration":
        cprint("Configuration")
    else:
        cprint("Undefined item")


@command
@argument("dbfile", description="Pick a data file", choices=lsdb())
@argument("password", description="Please provide your password")
def open(dbfile: str, password: str):
    """
    This command is used to connect a database.
    """

    ctx = context.get_context()
    db = ctx.keepass.db

    if ctx.keepass.is_open():
        cprint("Database name: {}\nDescription: {}\nMaintenanceHistoryDays:{}"
            .format(db.Name, db.Description, db.MaintenanceHistoryDays))
    else:
        logger = ShowWarningsLogger()
        db_path = get_homepath() + '/' + dbfile
        ctx.keepass.open(db_path, password, logger)


@command
def close():
    """
    Close the database
    """
    ctx = context.get_context()
    ctx.keepass.close()
    cprint("Database is closed")

@command
def clear():
    '''
    Clears console.
    '''
    print("\033c")

# instead of replacing _ we rely on camelcase to - super-command


@command
class Configure:
    "KeePass Database configuration"

    def __init__(self) -> None:
        ctx = context.get_context()
        self._pwdb = ctx.keepass.db
        if not self._pwdb:
            cprint("Please connect to a database first.", "red")

    @property
    def pwdb(self):
        return self._pwdb

    """This is the super command help"""

    @command("name")
    @argument("db_name", positional=False)
    def db_name(self, db_name=""):
        """
        show or change the database name
        """
        if self.pwdb:
            if db_name:
                self.pwdb.Name = db_name
                self.pwdb.Modified = True
                cprint("Updated database name to {}".format(self.pwdb.Name))
            else:
                cprint("Database name: {}".format(self.pwdb.Name))

    @command
    @argument("username", positional=False)
    def default_user_name(self, username=""):
        """
        show or change the default username
        """
        if self.pwdb:
            if username:
                self.pwdb.DefaultUserName = username
                self.pwdb.Modified = True
                cprint("Updated default username to {}".format(self.pwdb.DefaultUserName))
            else:
                cprint("Database name: {}".format(self.pwdb.DefaultUserName))
