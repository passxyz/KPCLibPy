#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import clr
import sys

from kpclibpy import __path__ as kpclibpy_path

def interop_dll_path(dll_name):
    # Unfrozen path
    dll_path = os.path.join(os.path.dirname(os.path.realpath(kpclibpy_path[0])), 'kpclibpy', 'kpclib', 'lib', dll_name)
    #print("1. ", dll_path)
    if os.path.exists(dll_path):
        return dll_path

    # Frozen path, dll in the same dir as the executable
    dll_path = os.path.join(os.path.dirname(os.path.realpath(kpclibpy_path[0])), 'kpclibpy', '..', 'kpclib', 'lib', dll_name)
    #print("2. ", dll_path)
    if os.path.exists(dll_path):
        return dll_path

    raise Exception('Cannot find %s' % dll_path)

clr.AddReference(interop_dll_path('KPCLib.dll'))
clr.AddReference(interop_dll_path('SkiaSharp.dll'))
clr.AddReference(interop_dll_path('PassXYZLib.dll'))
clr.AddReference(interop_dll_path('PassXYZ.dll'))

if __name__ == '__main__':
	from KeePassLib import PwDatabase, PwGroup
	print(PwDatabase)
	print(PwGroup)
