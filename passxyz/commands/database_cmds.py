#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import asyncio
import socket
import typing
from pathlib import *
from termcolor import cprint
from nubia import command, argument, context
from commands.keepass import KeePass, IStatusLogger, get_homepath, lsdb

__keepass__ = KeePass()

class ShowWarningsLogger(IStatusLogger):
    __namespace__ = "KPCLibPyTest1"
    
    def StartLogging(self, strOperation, bWriteOperationToLog):
        print('StartLogging {} {}'.format(strOperation, bWriteOperationToLog))
        return
    def EndLogging(self):
        print('EndLogging')
        return
    def SetProgress(self, uPercent):
        print('In progress {}'.format(uPercent))
        return True
    def SetText(self, strNewText, lsType):
        print('SetText {} {}'.format(strNewText, lsType))
        return True
    def ContinueWork(self):
        return True

@command(aliases=["lookup"])
@argument("hosts", description="Hostnames to resolve", aliases=["i"])
@argument("bad_name", name="nice", description="testing")
def lookup_hosts(hosts: typing.List[str], bad_name: int):
    """
    This will lookup the hostnames and print the corresponding IP addresses
    """
    ctx = context.get_context()
    cprint("Input: {}".format(hosts), "yellow")
    cprint("Verbose? {}".format(ctx.verbose), "yellow")
    for host in hosts:
        cprint("{} is {}".format(host, socket.gethostbyname(host)))

    # optional, by default it's 0
    return 0


@command("show")
def show():
    """
    This command will list the current available databases.
    """
    #cprint(lsdb(), "green")
    db = __keepass__._db

    if __keepass__.is_open():
        cprint("Database name: {}\nDescription: {}\nMaintenanceHistoryDays:{}".format(db.Name, db.Description, db.MaintenanceHistoryDays))
    else:
        cprint("Database is closed", "red")


@command
@argument("number", type=int)
async def triple(number):
    "Calculates the triple of the input value"
    cprint("Input is {}".format(number))
    cprint("Type of input is {}".format(type(number)))
    cprint("{} * 3 = {}".format(number, number * 3))
    await asyncio.sleep(2)


@command
@argument("dbfile", description="Pick a data file", choices=lsdb())
@argument("password", description="Please provide your password")
def open(dbfile: str, password: str):
    """
    This command is used to connect a database.
    """

    logger = ShowWarningsLogger()
    db_path = get_homepath() + '/' + dbfile
    __keepass__.open(db_path, password, logger)

@command
def close():
    """
    Close the database
    """
    __keepass__.close()
    cprint("Database is closed")


# instead of replacing _ we rely on camelcase to - super-command


@command
class SuperCommand:
    "This is a super command"

    def __init__(self, shared: int = 0) -> None:
        self._shared = shared

    @property
    def shared(self) -> int:
        return self._shared

    """This is the super command help"""

    @command
    @argument("firstname", positional=True)
    def print_name(self, firstname: str):
        """
        print a name
        """
        cprint("My name is: {}".format(firstname))

    @command(aliases=["do"])
    def do_stuff(self, stuff: int):
        """
        doing stuff
        """
        cprint("stuff={}, shared={}".format(stuff, self.shared))
