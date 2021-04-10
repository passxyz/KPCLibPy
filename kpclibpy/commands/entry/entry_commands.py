#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import typing
import click
#from pathlib import *
from termcolor import cprint
from nubia import command, argument, context
#from commands.keepass import KeePass, IStatusLogger, get_homepath, lsdb


@command
@argument("path", description="the entry path", positional=True)
def cat(path: str):
    "Show an entry"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        entry = ctx.keepass.find_entry_by_path(path)
        if entry:
            ctx.keepass.print_entry(entry)
        else:
            print("cannot access {}: No such file or directory".format(path))


@command
@argument("path", description="entry path", positional=True)
@argument("key", description="source entry/group")
@argument("value", description="destination entry/group")
@argument("protected", description="print detail information or not")
def edit(path, key="Notes", value="", protected=False):
    "Edit an entry. Need to provide a key and a value to edit a field."
    ctx = context.get_context()
    if ctx.keepass.is_open():
        entry = ctx.keepass.find_entry_by_path(path)
        if entry:
            if value:
                ctx.keepass.update_entry(entry, key, value, protected)
            else:
                value = click.edit(entry.Strings.ReadSafe(key))
                ctx.keepass.update_entry(entry, key, value, protected)
        else:
            print("cannot access {}: No such file or directory".format(path))
    

@command
@argument("title", description="enter a title")
@argument("username", description="enter a username")
@argument("password", description="enter a password")
@argument("url", description="enter a url")
@argument("notes", description="enter a note")
def new(title="New entry", username="", password="", url="", notes=""):
    "Create a new entry"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        ctx.keepass.add_entry(title, username, password, url, notes)


@command
@argument("entry_name", description="enter a entry name", positional=True)
@argument("key", description="source entry/group")
def rm(entry_name: str, key=""):
    "Remove an entry or a field"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        try:
            entry = ctx.keepass.entries[entry_name]
            if entry:
                if key:
                    ctx.keepass.update_entry(entry, key, "")
                    cprint("Removed field {}.".format(key))
                else:
                    ctx.keepass.db.DeleteEntry(entry)
                    cprint("Removed entry {}.".format(entry_name))
            else:
                cprint("rm: cannot remove {}: No such entry".format(entry_name), "red")
        except KeyError:
            cprint("rm: cannot remove {}: No such entry".format(entry_name), "red")
