#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

from nubia import context
from nubia import exceptions
from nubia import eventbus
from commands.keepass import KeePass

_keepass = KeePass()

class NubiaPassXYZContext(context.Context):
    def __init__(self, *args, **kwargs):
        self.keepass = _keepass
        self.version = "1.0.5"
        super().__init__()

    def on_connected(self, *args, **kwargs):
        pass

    def on_cli(self, cmd, args):
        # dispatch the on connected message
        self.verbose = args.verbose
        self.registry.dispatch_message(eventbus.Message.CONNECTED)

    def on_interactive(self, args):
        self.verbose = args.verbose
        ret = self._registry.find_command("connect").run_cli(args)
        if ret:
            raise exceptions.CommandError("Failed starting interactive mode")
        # dispatch the on connected message
        self.registry.dispatch_message(eventbus.Message.CONNECTED)
