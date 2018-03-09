# -*- coding: utf-8 -*-
from boostnote.storage import Storage


class Boostnote(object):
    def __init__(self, paths: list):
        self._storages = {}
        name = 'Default'
        for idx, path in enumerate(paths):
            self.storages['%s%d' % (name, idx)] = Storage(path)

    def get_storages(self) -> dict:
        return self._storages

    storages = property(fget=get_storages)

    def walk_note(self):
        for storage in self.storages.values():
            for key, folder in storage.folders.items():
                for note in folder.notes:
                    yield storage, folder, note

    def __str__(self):
        return '<%s>' % (self.__class__.__name__)

