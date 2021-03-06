#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import os
import pytest

import commands
from nubia import Nubia, Options
from nubia_plugin import NubiaPassXYZPlugin
from commands.keepass import get_homepath

class PxShell(Nubia):
    """
    Unit test class
    >>> import tests.db_test as db_test
    >>> db_test.test_version()

    or
    >>> shell = db_test.PxShell()
    >>> shell.run_interactive_line('version')
    """
    def __init__(self, name="passxyz_test"):
        px_plugin = NubiaPassXYZPlugin()
        super(PxShell, self).__init__(name, plugin=px_plugin, command_pkgs=commands, testing=True)
        self.registry = self._registry

    def run_cli_line(self, raw_line):
        cli_args_list = raw_line.split()
        args = self._pre_run(cli_args_list)
        return self.run_cli(args)

    def run_interactive_line(self, raw_line, cli_args=None):
        cli_args = cli_args or "test_shell connect"
        cli_args_list = cli_args.split()
        args = self._pre_run(cli_args_list)
        io_loop = self._create_interactive_io_loop(args)
        return io_loop.parse_and_evaluate(raw_line)

pxshell = PxShell()

@pytest.mark.order(1)
def test_version():
    global pxshell
    version = pxshell.run_interactive_line('version')
    assert version == "1.0.6"


@pytest.mark.order(2)
def test_open():
    global pxshell
    pxshell.run_interactive_line('open dbfile=utdb.kdbx password="12345"')
    pxshell.run_interactive_line('cat "Sample Entry"')
    pxshell.run_interactive_line('close')


@pytest.mark.order(3)
def test_show1(capsys):
    global pxshell
    pxshell.run_interactive_line('show')
    #out, err = capsys.readouterr()


@pytest.mark.order(4)
def test_show2():
    global pxshell
    pxshell.run_interactive_line('open dbfile=utdb.kdbx password="12345"')
    pxshell.run_interactive_line('show')
    pxshell.run_interactive_line('close')

