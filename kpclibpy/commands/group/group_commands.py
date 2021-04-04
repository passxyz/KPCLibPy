#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import typing
from prettytable import PrettyTable
from termcolor import cprint
from nubia import command, argument, context

def print_group(group, detail=False):
    ctx = context.get_context()

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
            s_table.add_row([entry.Strings.ReadSafe(ctx.keepass.TITLE)])

    s_table.align = "l"
    s_table.border = False
    s_table.header = False
    print("Current group is {}.\n".format(group))
    print(s_table)

@command
@argument("path", description="a specified path", positional=False)
@argument("detail", description="print detail information or not")
def ls(path="", detail=False):
    "Lists entries or groups in pwd or in a specified path"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        if path:
            current_group = ctx.keepass.find_group_by_path(path)
            if current_group:
                print_group(current_group, detail)
            else:
                entry = ctx.keepass.find_entry_by_path(path)
                if entry:
                    print("{}".format(entry.get_Name()))
                else:
                    print("cannot access {}: No such file or directory".format(path))
        else:
            print_group(ctx.keepass.current_group, detail)


@command
def pwd():
    "Print the current working directory"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        print(ctx.keepass.db.CurrentPath)


@command
@argument("path", description="enter a path", positional=True)
def cd(path: str):
    """
    Change directory (group), '/' - root, '..' - parent
    """
    ctx = context.get_context()
    if ctx.keepass.is_open():
        if path == '/':
            ctx.keepass.current_group = ctx.keepass.root_group
        else:
            group = ctx.keepass.find_group_by_path(path)
            if group:
                ctx.keepass.current_group = group
            else:
                cprint("Cannnot find {}".format(path), "yellow")


@command
@argument("group_name", description="enter a group name", positional=True)
def mkdir(group_name: str):
    "Create a new directory (group)"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        new_group = ctx.keepass.current_group.FindCreateGroup(group_name, False)
        if new_group:
            cprint("{} already exist.".format(new_group))
        else:
            new_group = ctx.keepass.current_group.FindCreateGroup(group_name, True)
            cprint("Created group {}".format(new_group))

@command
@argument("group_name", description="enter a group name", positional=True)
def rmdir(group_name: str):
    "Delete a directory (group)"
    ctx = context.get_context()
    if ctx.keepass.is_open():
        group = ctx.keepass.current_group.FindCreateGroup(group_name, False)
        if group:
            ctx.keepass.db.DeleteGroup(group)
            cprint("Removed {}.".format(group))
        else:
            cprint("rmdir: failed to remove {}: No such group.".format(group))
