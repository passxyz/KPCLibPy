#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import typing
from prettytable import PrettyTable
from termcolor import cprint, colored
from nubia import command, argument, context
from kpclibpy.commands.keepass import IStatusLogger, get_homepath, lsdb
#from KeePassLib import PwGroup, PwEntry, Collections


class KPCLibPyLogger(IStatusLogger):
    __namespace__ = "KPCLibPyLogger"
    
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

"""
@command("export")
def export_db():
    "Export entries to a new database"
    return None

@command("import")
def import_db():
    "Import another database to the current one"
    return None
"""


def print_entries(entries):
    e_table = PrettyTable(["No", "Entry Name"])
    num = 0
    indexes = {}
    for entry in entries:
        num = num + 1
        e_table.add_row([num, entry])
        indexes[num] = entry
    e_table.align = "l"
    e_table.border = False
    e_table.header = False
    print(e_table)
    return indexes

@command
@argument("keywords", description="Search keyword in entries", positional=True)
def find(keywords: str):
    "Find entries"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        entries = ctx.keepass.find(keywords)
        while True:
            indexes = print_entries(entries)
            x = input('Enter the entry number (or q to quite):')
            try:
                if x == 'q':
                    break
                else:
                    ctx.keepass.print_entry(entries[indexes[int(x)]])
                    input('Please any key to continue')
            except ValueError:
                print("Wrong entry number, please choose a correct one or enter 'q' to quit")
    else:
        cprint("Please connect to a database first.", "red")


def _move_group(src, dst_group):
    """
    Move src to a group
    src       - source path of an entry or a group
    dst_group - a PwGroup instance
    """
    ctx = context.get_context()
    if ctx.keepass.is_open():
        if src:
            src_group = ctx.keepass.find_group_by_path(src)
            if src_group:
                ctx.keepass.move_group(src_group, dst_group)
            else:
                src_entry = ctx.keepass.find_entry_by_path(src)
                if src_entry:
                    ctx.keepass.move_entry(src_entry, dst_group)
                else:
                    print("mv: cannot access {}: No such file or directory".format(src))
        else:
            print("mv: src is empty.")

@command
@argument("src", description="source entry/group", positional=True)
@argument("dst", description="destination group", positional=True)
def mv(src: str, dst: str):
    "Move an entry or group to a new location"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        if dst:
            dst_group = ctx.keepass.find_group_by_path(dst)
            if dst_group:
                _move_group(src, dst_group)
            else:
                print("mv: cannot access group {}: No such file or directory".format(dst))
        else:
            print("mv: dst is empty.")


def rename_entry(src, dst):
    ctx = context.get_context()
    try:
        if(ctx.keepass.entries[src]):
            ctx.keepass.entries[src].set_Name(dst)
            return ctx.keepass.entries[dst]
        else:
            return None
    except KeyError:
        return None

def rename_group(src, dst):
    ctx = context.get_context()
    try:
        if(ctx.keepass.groups[src]):
            ctx.keepass.groups[src].set_Name(dst)
            return ctx.keepass.groups[dst]
        else:
            return None
    except KeyError:
        return None

@command
@argument("src", description="source entry/group", positional=True)
@argument("dst", description="destination entry/group", positional=True)
def rename(src: str, dst: str):
    "Rename a group or entry"
    if rename_entry(src, dst):
        cprint("Renamed entry {} to {}".format(src, dst))
    elif rename_group(src, dst):
        cprint("Renamed group {} to {}".format(src, dst))
    else:
        cprint("rename: cannot stat {}: No such entry or group".format(src))


@command
def version():
    "Display version number"
    en_table = PrettyTable(["Components", "Version"])
    en_table.align = "l"

    ctx = context.get_context()
    en_table.add_row([colored("KPCLibPy", "yellow"), ctx.version])
    en_table.add_row([colored("KPCLib", "yellow"), "{}".format(ctx.keepass.version)])

    if ctx.keepass.is_open():
        en_table.add_row([colored("CurrentGroup", "yellow"), "{}".format(ctx.keepass.current_group)])
    
    print(en_table)
    return ctx.version


@command
def save():
    """
    Save te database to disk
    """
    ctx = context.get_context()
    db = ctx.keepass.db

    if ctx.keepass.is_open():
        logger = KPCLibPyLogger()
        db.Save(logger)


@command("show")
@argument("items", type=str, description="Database configuration, version etc.",
    choices=["config", "version", "databases", "help"], positional=True)
def show(items):
    """
    This command shows the information of the current databases.
    """
    ctx = context.get_context()
    db = ctx.keepass.db

    help_table = PrettyTable(["Sub-command", "Description"])
    help_table.align = "l"
    help_table.add_row(["databases", "list of databases"])
    help_table.add_row(["config", "database configuration"])
    help_table.add_row(["version", "App version"])

    if items == "config":
        if ctx.keepass.is_open():
            db_table = PrettyTable(["Property", "Value"])
            db_table.align = "l"

            db_table.add_row([colored("Database name", "magenta"), db.Name])
            db_table.add_row([colored("DefaultUserName", "magenta"), db.DefaultUserName])
            db_table.add_row([colored("Modified", "magenta"), db.Modified])
            db_table.add_row([colored("Hide password", "magenta"), ctx.keepass.is_hidden])
            db_table.add_row([colored("RecycleBinEnabled", "magenta"), db.RecycleBinEnabled])
            db_table.add_row([colored("HistoryMaxItems", "magenta"), db.HistoryMaxItems])
            db_table.add_row([colored("HistoryMaxSize", "magenta"), db.HistoryMaxSize])
            db_table.add_row([colored("Description", "magenta"), db.Description])
            db_table.add_row([colored("MaintenanceHistoryDays", "magenta"), db.MaintenanceHistoryDays])
            db_table.add_row([colored("Filename", "magenta"), ctx.keepass.file_name])
            if ctx.keepass.db_type == "PassXYZ":
                db_table.add_row([colored("Decoded Filename", "magenta"), ctx.keepass.user_name])
            cprint("Database configureation", "yellow")
            print(db_table)
        else:
            cprint("Database is closed", "red")
    elif items == "version":
        version()
    elif items == "databases":
        print("The current path: ", get_homepath())
        db_table = PrettyTable(["No.", "Name"])
        db_table.align = "l"
        num = 1
        for file in lsdb():
            db_table.add_row([num, file])
            num = num + 1
        print(db_table)
    elif items == "help":
        print(help_table)
    else:
        print(help_table)


@command
@argument("dbfile", description="Pick a data file", choices=lsdb())
@argument("password", description="Please provide your password")
def open(dbfile: str, password = ""):
    """
    This command is used to connect a database.
    """
    if not password:
        import getpass
        password = getpass.getpass('Password:')

    ctx = context.get_context()
    db = ctx.keepass.db

    if ctx.keepass.is_open():
        cprint("Database name: {}\nDescription: {}\nMaintenanceHistoryDays:{}"
            .format(db.Name, db.Description, db.MaintenanceHistoryDays))
    else:
        #logger = KPCLibPyLogger()
        #db_path = get_homepath() + '/' + dbfile
        #ctx.keepass.open(db_path, password, logger)
        ctx.keepass.connect(dbfile, password)
    
    ctx.keepass.file_name = dbfile


@command
@argument("dbfile", description="Pick a data file")
@argument("password", description="Please provide your password")
@argument("type", description="kdbx or xyz")
def newdb(dbfile: str, password = "", type = ".kdbx"):
    """
    This command is used to create a new database.
    """

    ctx = context.get_context()
    db = ctx.keepass.db

    if ctx.keepass.is_open():
        cprint("Please close the current database {} before you can create a new database."
            .format(db.Name))
    else:
        newfile = dbfile + type
        for file in lsdb():
            if newfile == file:
                print("Data file {} already exist.".format(newfile))
                return
        if not password:
            import getpass
            password = getpass.getpass('Password:')
        db_path = get_homepath() + '/' + newfile
        ctx.keepass.new(db_path, password)
        ctx.keepass.db.Name = dbfile
        ctx.keepass.db.DefaultUserName = dbfile
        ctx.keepass.db.Description = db_path


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
        self.keepass = ctx.keepass
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

    @command
    def toggle(self):
        """
        Toggle show or hide password
        """
        if self.keepass:
            if self.keepass.is_hidden:
                self.keepass.is_hidden = False
            else:
                self.keepass.is_hidden = True
