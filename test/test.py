import os
import sys
sys.path.append("..")
import kpclibpy

from KeePassLib import PwDatabase, PwGroup 
from KeePassLib.Serialization import IOConnectionInfo
from KeePassLib.Keys import CompositeKey, KcpPassword
from KeePassLib.Interfaces import IStatusLogger

class ShowWarningsLogger(IStatusLogger):
    __namespace__ = "KPCLibPy"
    
    def StartLogging(self, strOperation, bWriteOperationToLog):
        return
    def EndLogging(self):
        return
    def SetProgress(self, uPercent):
        return True
    def SetText(self, strNewText, lsType):
        return True
    def ContinueWork():
        return True

test_db_path = 'utdb.kdbx'
ioc = IOConnectionInfo.FromPath(test_db_path)
TEST_DB_KEY = "12345"
cmpKey = CompositeKey()
cmpKey.AddUserKey(KcpPassword(TEST_DB_KEY))

pwDb = PwDatabase()

swLogger = ShowWarningsLogger()
pwDb.Open(ioc, cmpKey, swLogger)

def printEntry(kp):
    for kp in entry.Strings:
        print('{}={}'.format(kp.Key, kp.Value.ReadString()))

pg = pwDb.RootGroup
i = 0
for entry in pg.Entries:
    print('--- Item {} ---'.format(i))
    printEntry(entry)
    i = i + 1