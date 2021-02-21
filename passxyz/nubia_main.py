#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import sys

import commands
from nubia import Nubia, Options
from nubia_plugin import NubiaExamplePlugin


if __name__ == "__main__":
    plugin = NubiaExamplePlugin()
    shell = Nubia(
        name="nubia_passxyz",
        command_pkgs=commands,
        plugin=plugin,
        options=Options(
            persistent_history=False, auto_execute_single_suggestions=False
        ),
    )
    sys.exit(shell.run())
