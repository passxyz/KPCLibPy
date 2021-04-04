#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import pytest

@pytest.mark.order(1)
def test_version(pxshell):
    version = pxshell.run_interactive_line('version')
    assert version == "1.1.0"


@pytest.mark.order(2)
def test_cat(keepass_db, pxshell):
    pxshell.run_interactive_line('cat "Sample Entry"')


@pytest.mark.order(3)
def test_show1(pxshell):
    pxshell.run_interactive_line('show')


@pytest.mark.order(4)
def test_show2(keepass_db, pxshell):
    pxshell.run_interactive_line('show')

