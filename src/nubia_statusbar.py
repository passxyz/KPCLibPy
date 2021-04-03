#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

from pygments.token import Token

from nubia import context
from nubia import statusbar


class NubiaPassXYZStatusBar(statusbar.StatusBar):
    def __init__(self, context):
        self._last_status = None

    def get_rprompt_tokens(self):
        if self._last_status:
            return [(Token.RPrompt, "Error: {}".format(self._last_status))]
        return []

    def set_last_command_status(self, status):
        self._last_status = status

    def get_tokens(self):
        spacer = (Token.Spacer, "  ")
        if context.get_context().keepass.is_hidden:
            is_verbose = (Token.Warn, "Hidden")
        else:
            is_verbose = (Token.Info, "Show")

        return [
            (Token.Info, context.get_context().db_type),
            spacer,
            (Token.Toolbar, "Password"),
            spacer,
            is_verbose,
            spacer,
            (Token.Toolbar, "Status"),
            spacer,
            (Token.Info, context.get_context().current_group),
        ]
