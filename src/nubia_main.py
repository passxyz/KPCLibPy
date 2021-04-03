#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import os

import commands
from nubia import Nubia, Options
from nubia_plugin import NubiaPassXYZPlugin
from commands.keepass import get_homepath


if __name__ == "__main__":
    homepath = get_homepath()
    if not os.path.exists(homepath):
        os.mkdir(homepath)

    plugin = NubiaPassXYZPlugin()
    shell = Nubia(
        name="nubia_passxyz",
        command_pkgs=commands,
        plugin=plugin,
        options=Options(
            persistent_history=False, auto_execute_single_suggestions=False
        ),
    )
    sys.exit(shell.run())
