# -*- coding: utf-8 -*-
import os
import json
import fnmatch

from boostnote.note import Note
from boostnote.folder import Folder


class Storage(object):
    json_file = 'boostnote.json'

    def __init__(self, path):
        # init variables
        self._folders = {}

        if os.path.exists(path):
            self._path = path
        else:
            raise FileNotFoundError(path)

        self._setting_file = os.path.join(path, self.json_file)

        if os.path.exists(self.setting_file):
            with open(self.setting_file, 'rb') as fp:
                self._data = json.load(fp)

        for d in self._data['folders']:
            s = Folder(**d)
            self.folders[s.key] = s

        for root, dirnames, filenames in os.walk(self._path):
            for filename in fnmatch.filter(filenames, '*.cson'):
                cson_file = os.path.join(root, filename)
                with open(cson_file, 'r', encoding='utf-8') as fp:
                    note = Note().load(fp)
                    self.folders[note.folder].notes.append(note)

    def get_setting_file(self) -> str:
        return self._setting_file

    setting_file = property(fget=get_setting_file)

    def get_folders(self) -> dict:
        return self._folders

    folders = property(fget=get_folders)

    def __str__(self):
        return '<%s: %s, Storages=%d>' % (self.__class__.__name__, self.setting_file, len(self.folders))

    def __repr__(self):
        rlt = []
        rlt.append(self.__str__())
        prefix_func = lambda x: '+-' if x[0] == '<' else '  '
        for key, value in self.folders.items():
            rlt.extend(list(map(lambda x: prefix_func(x.__str__()) + x, value.__repr__().split('\n'))))
        return '\n'.join(rlt)

    def walk_note(self):
        for folders in self.folders.values():
            for note in folders.notes:
                yield folders, note
