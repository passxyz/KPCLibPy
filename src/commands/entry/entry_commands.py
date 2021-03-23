#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import typing
#from pathlib import *
from termcolor import cprint
from nubia import command, argument, context
#from commands.keepass import KeePass, IStatusLogger, get_homepath, lsdb


@command
@argument("entry", description="enter an entry", positional=True)
def cat(entry: str):
    "Show an entry"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        try:
            if ctx.keepass.entries[entry]:
                ctx.keepass.print_entry(ctx.keepass.entries[entry])
        except KeyError:
            cprint("Cannnot find {}".format(entry), "red")


@command
def find():
    "Find entries"
    return None


@command
def new():
    "Create a new entry"
    return None


@command
@argument("entry_name", description="enter a entry name", positional=True)
def rm(entry_name: str):
    "Remove an entry"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        try:
            entry = ctx.keepass.entries[entry_name]
            if entry:
                ctx.keepass.db.DeleteEntry(entry)
                cprint("Removed {}.".format(entry_name))
            else:
                cprint("rm: cannot remove {}: No such entry".format(entry_name), "red")
        except KeyError:
            cprint("rm: cannot remove {}: No such entry".format(entry_name), "red")
