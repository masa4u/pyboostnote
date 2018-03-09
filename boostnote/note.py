# -*- coding: utf-8 -*-
import cson
from enum import Enum
from tabulate import tabulate


class NoteType(Enum):
    MARKDOWN_NOTE = 1
    SNIPPET_NOTE = 2


class Note(object):
    def __init__(self):
        self._data = {}

    def load(self, fin):
        self._data = cson.load(fin)
        return self

    def loads(self, s):
        self._data = cson.loads(s)
        return self

    def get_create_at(self):
        return self._data['createdAt']

    createdAt = property(fget=get_create_at)

    def get_updated_at(self):
        return self._data['updatedAt']

    updatedAt = property(fget=get_updated_at)

    def get_type(self):
        return self._data['type']

    type = property(fget=get_type)

    def get_folder(self):
        return self._data['folder']

    folder = property(fget=get_folder)

    def get_title(self):
        return self._data['title']

    title = property(fget=get_title)

    def get_description(self):
        return self._data['description']

    description = property(fget=get_description)

    def get_tags(self) -> list:
        return self._data['tags']

    tags = property(fget=get_tags)

    def get_is_starred(self) -> bool:
        return self._data['isStarred']

    isStarred = property(fget=get_is_starred)

    def get_is_trashed(self) -> bool:
        return self._data['isTrashed']

    isTrashed = property(fget=get_is_trashed)

    def __str__(self):
        return '<CSonNote: %13s title=%s>' % (self.type, self.title)

    def __repr__(self):
        rlt = []
        rlt.append(self.__str__())
        rlt.extend(tabulate(self._data.items(), headers=('key', 'value'), tablefmt='orgtbl').split('\n'))
        return '\n'.join(rlt)


if __name__ == '__main__':
    folder = r'C:\Users\Owner\Boostnote\notes\63a94ae29718dd240436.cson'
