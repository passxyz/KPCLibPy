import os
import clr
import sys

# Set environment variables
assembly_path = os.environ['HOME']+'/github/passxyz/KPCLib/KPCLib/bin/Debug/netstandard2.0/publish'
sys.path.append(assembly_path)

clr.AddReference("KPCLib")
clr.AddReference("SkiaSharp")

def main():
	from KeePassLib import PwDatabase, PwGroup
	print(PwDatabase)
	print(PwGroup)

if __name__ == '__main__':
    main()