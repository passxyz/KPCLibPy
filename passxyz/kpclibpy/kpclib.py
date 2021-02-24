import os
import clr
import sys

def interop_dll_path(dll_name):
    # Unfrozen path
    dll_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib', dll_name)
    if os.path.exists(dll_path):
        return dll_path

    # Frozen path, dll in the same dir as the executable
    dll_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), dll_name)
    if os.path.exists(dll_path):
        return dll_path

    try:
        # Frozen path packed as onefile
        dll_path = os.path.join(sys._MEIPASS, dll_name)
        if os.path.exists(dll_path):
            return dll_path
    except Exception:
        pass

    raise Exception('Cannot find %s' % dll_name)

clr.AddReference(interop_dll_path('KPCLib.dll'))
clr.AddReference(interop_dll_path('SkiaSharp.dll'))

if __name__ == '__main__':
	from KeePassLib import PwDatabase, PwGroup
	print(PwDatabase)
	print(PwGroup)
