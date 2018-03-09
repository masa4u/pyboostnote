# -*- coding: utf-8 -*-
import os
import cson
from enum import Enum
from tabulate import tabulate


class NoteType(Enum):
    MARKDOWN_NOTE = ('MarkdownNote', ('contents'),
                     lambda x: 'len=%d' % len(x.content))
    SNIPPET_NOTE = ('SnippetNote', ('snippets'),
                    lambda x: 'files=%d' % len(x.snippets))

    def __init__(self, note_type, fields, summary):
        self.note_type = note_type
        self.fields = fields
        self.summary = summary

    def __repr__(self):
        return self.name


class Note(object):
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self):
        self._data = {'createdAt': '',
                      'updatedAt': '',
                      'type': NoteType.MARKDOWN_NOTE.name,
                      'folder': '',
                      'title': '',
                      'content': '',
                      'description': '',
                      'tags': [],
                      'isStarred': False,
                      'isTrashed': False}

    @classmethod
    def create_note(self, folder, title, full_path):
        from boostnote.migration.util import creation_date, update_date
        note = Note()

        note.folder = folder
        note.title = title
        note.createdAt = creation_date(full_path, self.date_format)
        note.updatedAt = update_date(full_path, self.date_format)

        with open(full_path, 'r', encoding='utf-8') as fp:
            content = fp.read()
            note.content = content

        return note

    def load(self, fin):
        self._data = cson.load(fin)
        return self

    def loads(self, s):
        self._data = cson.loads(s)
        return self

    def dump_file(self, filename):
        if os.path.exists(filename):
            print('already generated file (%s) => (%s) (%s)' % (filename, self.folder, self.title))
            return
        with open(filename, 'w+') as fp:
            cson.dump(self._data, fp)

    def get_created_at(self):
        return self._data['createdAt']

    def set_created_at(self, _date):
        self._data['createdAt'] = _date

    createdAt = property(fget=get_created_at, fset=set_created_at)

    def get_updated_at(self):
        return self._data['updatedAt']

    def set_updated_at(self, _date):
        self._data['updatedAt'] = _date

    updatedAt = property(fget=get_updated_at, fset=set_updated_at)

    def get_type(self) -> NoteType:
        return getattr(NoteType, self._data['type'])

    type = property(fget=get_type)

    def get_folder(self):
        return self._data['folder']

    def set_folder(self, folder):
        self._data['folder'] = folder

    folder = property(fget=get_folder, fset=set_folder)

    def get_title(self):
        return self._data['title']

    def set_title(self, title):
        self._data['title'] = title

    title = property(fget=get_title, fset=set_title)

    def get_description(self):
        return self._data['description']

    description = property(fget=get_description)

    def get_content(self):
        return self._data['content']

    def set_content(self, c):
        self._data['content'] = c

    content = property(fget=get_content, fset=set_content)

    def get_snippets(self):
        return self._data['snippets']

    snippets = property(fget=get_snippets)

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
        note_info = self.type.summary(self)
        return '<%s: %13s folder=%s title=%s, %s>' % (
            self.__class__.__name__, self.type, self.folder, self.title, note_info)

    def __repr__(self):
        rlt = []
        rlt.append(self.__str__())
        rlt.extend(tabulate(self._data.items(), headers=('key', 'value'), tablefmt='orgtbl').split('\n'))
        return '\n'.join(rlt)


if __name__ == '__main__':
    folder = r'C:\Users\Owner\Boostnote\notes\63a94ae29718dd240436.cson'
