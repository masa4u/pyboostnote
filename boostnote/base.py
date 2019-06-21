# -*- coding: utf-8 -*-
from typing import List, Union

from boostnote.storage import Storage
from boostnote.note import NoteType


class Boostnote(object):
    def __init__(self, paths: Union[List[str], str]):
        if isinstance(paths, str):
            paths = [paths]
        self._storages = {}
        name = 'Default'
        for idx, path in enumerate(paths):
            self.storages['%s%d' % (name, idx)] = Storage(path)

    def get_storages(self) -> dict:
        return self._storages

    storages: List[Storage] = property(fget=get_storages)

    def walk_note(self):
        for storage in self.storages.values():
            for key, folder in storage.folders.items():
                for note in folder.notes:
                    if note.type == NoteType.SNIPPET_NOTE:
                        continue
                    yield storage, folder, note

    def save_notes(self):
        for storage, folder, note in self.walk_note():
            if note.is_updated is True:
                note.dump_file(note.filename)

    def find_note(self, func):
        for storage, folder, note in self.walk_note():
            if func(note) is True:
                yield storage, folder, note

    def __str__(self):
        return '<%s Storages=%d>' % (self.__class__.__name__, len(self.storages))
