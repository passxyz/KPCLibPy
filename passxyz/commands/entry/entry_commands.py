#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

from nubia import command, argument, context


@command
def cat():
    "Show an entry"
    return None

@command
def find():
    "Find entries"
    return None

@command
def new():
    "Create a new entry"
    return None

@command
def rm():
    "Remove an entry"
    return None
