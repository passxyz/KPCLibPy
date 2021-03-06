#!/usr/bin/env python3

# Copyright (c) Roger Ye.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#

from pathlib import *
from os import listdir
from os.path import isfile, join
from prettytable import PrettyTable
from termcolor import cprint, colored
import kpclibpy

from KeePassLib import PwDatabase, PwGroup, PwEntry, Collections
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
    """
    Python interface of KeePassLib
    """
    _keepass = None

    def __new__(cls, *args, **kwargs):
        if not cls._keepass:
            cls._keepass = super(KeePass, cls
                ).__new__(cls, *args, **kwargs)
        return cls._keepass
    
    def __init__(self):
        self._db = None
        self._current_group = None
        self._db_type = "KeePass"
        self.is_hidden = True

    @property
    def db(self):
        """
        ReadOnly property to represent a KeePass database instance (PwDatabase)
        """
        return self._db

    @property
    def db_type(self):
        """
        Getter of database type
        The database type can be KeePass or PassXYZ
        """
        return self._db_type

    @db_type.setter
    def db_type(self, db_t):
        """
        Setter of database type
        """
        if db_t == "KeePass" or db_t == "PassXYZ":
            self._db_type = db_t
        else:
            print("Unsupported database type")

    @property
    def  root_group(self):
        """
        Root group of the current database
        """
        return self._db.RootGroup

    @property
    def current_group(self):
        """
        Getter of the current working directory (group)
        """
        return self._current_group

    @current_group.setter
    def current_group(self, group):
        """
        Setter of the current working directory (group)
        """
        self._current_group = group

    @property
    def groups(self):
        """
        A dictionary of groups in current working directory (group)
        Key   - group name
        Value - PwGroup
        """
        if self.current_group:
            groups = {}
            for gp in self.current_group.Groups:
                groups[gp.get_Name()] = gp
            return groups
        else:
            return None

    @property
    def entries(self):
        """
        A dictionary of entries in current working directory (group)
        Key   - entry title
        Value -  PwEntry
        """
        if self.current_group:
            entries = {}
            for entry in self.current_group.Entries:
                entries[entry.Strings.ReadSafe("Title")] = entry
            return entries
        else:
            return None

    def get_value(self, entry, key):
        if(entry.Strings.GetSafe(key).IsProtected):
            if self.is_hidden:
                return "*******"
        return entry.Strings.ReadSafe(key)

    def print_entry(self,  entry):
        en_table = PrettyTable(["Key", "Value"])
        en_table.align = "l"

        for x in entry.Strings:
            en_table.add_row([colored(x.Key, "yellow"), self.get_value(entry, x.Key)])
            #cprint("{}:".format(x.Key), "yellow")
            #cprint("\t{}\n".format(self.get_value(entry, x.Key)))
        print(en_table)

    def is_open(self):
        if self.db:
            if self.db.IsOpen:
                return True
            else:
                return False
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
                self._current_group = self._db.RootGroup
        except InvalidCompositeKeyException:
            self.close()
            print("The composite key is invalid!")
            return
