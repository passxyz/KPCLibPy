from pathlib import *
from os import listdir
from os.path import isfile, join
import kpclibpy

from KeePassLib import PwDatabase, PwGroup 
from KeePassLib.Serialization import IOConnectionInfo
from KeePassLib.Keys import CompositeKey, KcpPassword, InvalidCompositeKeyException
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
    
    @property
    def db(self):
        """
        ReadOnly property to represent a KeePass database instance (PwDatabase)
        """
        if self._db:
            return self._db
        else:
            return None

    def is_open(self):
        if self.db:
            return True
        else:
            return False

    def close(self):
        if self._db:
            if self._db.IsOpen:
                self._db.Close()
                self._db = None
        else:
            print("Database connection is not established yet.")

    def open(self, db_path, password, logger):
        ioc = IOConnectionInfo.FromPath(db_path)
        cmpKey = CompositeKey()
        cmpKey.AddUserKey(KcpPassword(password))

        self._db = PwDatabase()

        try:
            if not self._db.IsOpen:
                self._db.Open(ioc, cmpKey, logger)
        except InvalidCompositeKeyException:
            self.close()
            print("The composite key is invalid!")
            return


