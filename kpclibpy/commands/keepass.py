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
import kpclibpy.kpclib

from KeePassLib import PwGroup, PwEntry, SearchParameters
from KeePassLib.Collections import PwObjectList
from KeePassLib.Interfaces import IStatusLogger
from KeePassLib.Keys import CompositeKey, KcpPassword, InvalidCompositeKeyException
from KeePassLib.Security import ProtectedString
from KeePassLib.Serialization import IOConnectionInfo
from PassXYZLib import PxDatabase, PxLibInfo


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
        self.TITLE = "Title"
        self.USERNAME = "UserName"
        self.PASSWORD = "Password"
        self.URL = "URL"
        self.NOTES = "Notes"

    @property
    def version(self):
        """
        ReadOnly property to represent the version of PassXYZLib
        """
        return PxLibInfo.Version

    @property
    def db(self):
        """
        ReadOnly property to represent a KeePass database instance (PxDatabase)
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
        if self._db:
            return self._db.CurrentGroup
        else:
            return self._current_group

    @current_group.setter
    def current_group(self, group):
        """
        Setter of the current working directory (group)
        """
        if self._db:
            self._db.CurrentGroup = group
        else:
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
                entries[entry.Strings.ReadSafe(self.TITLE)] = entry
            return entries
        else:
            return None

    def find(self, keywords):
        sp = SearchParameters()
        sp.SearchString = keywords
        ol = PwObjectList[PwEntry]()
        self.root_group.SearchEntries(sp, ol)
        entries = {}
        for entry in ol:
            entries[entry.Name] = entry
        return entries

    def get_entries(self, name):
        """
        Get a dictionary of entries in the sub-group of current group
        name   - sub-group name
        """
        try:
            if self.groups[name]:
                entries = {}
                for entry in self.groups[name].Entries:
                    entries[entry.Strings.ReadSafe(self.TITLE)] = entry
                return entries
            else:
                return None
        except KeyError:
            return None

    def _add_entry(self, title = "New Entry", username = "", pw = "", url = "", notes = ""):
        entry = PwEntry()
        entry.Name = title
        if username:
            entry.Strings.Set(self.USERNAME, ProtectedString(False, username))
        else:
            entry.Strings.Set(self.USERNAME, ProtectedString(False, self.db.DefaultUserName))
        
        if pw:
            entry.Strings.Set(self.PASSWORD, ProtectedString(True, pw))
        else:
            entry.Strings.Set(self.PASSWORD, ProtectedString(True, self.db.DefaultUserName))

        if url:
            entry.Strings.Set(self.URL, ProtectedString(False, url))

        if notes:
            entry.Strings.Set(self.NOTES, ProtectedString(False, notes))

        self.current_group.AddEntry(entry, True)

    def add_entry(self, title = "New Entry", username = "", pw = "", url = "", notes = ""):
        """
        Added a new entry in the current group
        name   - sub-group name
        """
        try:
            if(self.entries[title]):
                cprint("Entry exist.", "red")
            else:
                self._add_entry(title, username, pw, url, notes)
        except KeyError:
            self._add_entry(title, username, pw, url, notes)

    def update_entry(self, entry, key, value):
        """
        Update an entry
        entry  - Entry to be updated
        key   - a key name
        value - a value
        """
        entry.Strings.Set(key, ProtectedString(False, value))


    def get_groups(self, name):
        """
        Get a dictionary of groups in the sub-group of current group
        name   - sub-group name
        """
        try:
            if self.groups[name]:
                groups = {}
                for gp in self.groups[name].Groups:
                    groups[gp.get_Name()] = gp
                return groups
            else:
                return None
        except KeyError:
            return None
        
    def find_group_by_path(self, path):
        return self.db.FindByPath[PwGroup](path)

    def find_entry_by_path(self, path):
        return self.db.FindByPath[PwEntry](path)

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

        self._db = PxDatabase()

        try:
            if not self._db.IsOpen:
                self._db.Open(ioc, cmpKey, logger)
                #self.current_group = self._db.RootGroup
        except InvalidCompositeKeyException:
            self.close()
            self._db = None
            cprint("open: The composite key is invalid!", "red")
            return

    def new(self, db_path, password):
        ioc = IOConnectionInfo.FromPath(db_path)
        cmpKey = CompositeKey()
        cmpKey.AddUserKey(KcpPassword(password))

        self._db = PxDatabase()

        if not self._db.IsOpen:
            self._db.New(ioc, cmpKey)
            self.current_group = self._db.RootGroup
        else:
            cprint("new: Database already exist.", "red")

    def move_group(self, src_group, dst_group):
        if self._db.IsOpen:
            if self._db.MoveGroup(src_group, dst_group):
                print("Moved {} to {}".format(src_group.get_Name(), dst_group.get_Name()))
            else:
                print("Cannot move {} to {}".format(src_group.get_Name(), dst_group.get_Name()))

    def move_entry(self, src_entry, dst_group):
        if self._db.IsOpen:
            if self._db.MoveEntry(src_entry, dst_group):
                print("Moved {} to {}".format(src_entry.get_Name(), dst_group.get_Name()))
            else:
                print("Cannot move {} to {}".format(src_entry.get_Name(), dst_group.get_Name()))