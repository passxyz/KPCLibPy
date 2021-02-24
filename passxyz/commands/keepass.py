from pathlib import *
from os import listdir
from os.path import isfile, join
import kpclibpy

from KeePassLib import PwDatabase, PwGroup 
from KeePassLib.Serialization import IOConnectionInfo
from KeePassLib.Keys import CompositeKey, KcpPassword
from KeePassLib.Interfaces import IStatusLogger


def get_homepath():
    return str(Path.home())+'/.kpclibdb'

def lsdb():
    home_path = get_homepath()
    onlyfiles = [f for f in listdir(home_path) if isfile(join(home_path, f))]
    return onlyfiles


class KeePass:
    _keepass = None
    _db = None
    def __new__(cls, *args, **kwargs):
        if not cls._keepass:
            cls._keepass = super(KeePass, cls
                ).__new__(cls, *args, **kwargs)
        return cls._keepass
    
    def is_open(self):
        if not self._db:
            return False
        else:
            return True

    def close(self):
        if self._db.IsOpen:
            self._db.Close()
            self._db = None

    def open(self, db_path, password, logger):
        ioc = IOConnectionInfo.FromPath(db_path)
        cmpKey = CompositeKey()
        cmpKey.AddUserKey(KcpPassword(password))

        self._db = PwDatabase()
        #swLogger = StatusLogger()
        self._db.Open(ioc, cmpKey, logger)

