#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import typing
from pathlib import *
from termcolor import cprint
from nubia import command, argument, context
from commands.keepass import KeePass, IStatusLogger, get_homepath, lsdb
from KeePassLib import PwGroup, PwEntry, Collections


@command
@argument("path", description="a specified path", positional=False)
def ls(path=""):
    "Lists entries or groups in pwd or in a specified path"
    ctx = context.get_context()
    if ctx.keepass.is_open:
        print(ctx.keepass.entries)
    #    for g in ctx.keepass.current_group.Groups
    #        print("{}".format(g))
        for entry in ctx.keepass.entries
            print("{}".format(entry))


@command
def pwd():
    "Print the current working directory"
    return None


@command
def cd():
    "Change directory (group)"
    return None


@command
def mkdir():
    "Create a new directory (group)"
    return None


@command
def rmdir():
    "Delete a directory (group)"
    return None
