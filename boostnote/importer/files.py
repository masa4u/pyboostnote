# -*- coding: utf-8 -*-
import os
import fnmatch

from uuid import uuid4

from boostnote.importer.base_impoter import BaseImpoter
from boostnote.importer.util import creation_date, update_date
from boostnote.note import Note


class FilesImpoter(BaseImpoter):

    def __init__(self, path):
        BaseImpoter.__init__(self)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self._path = path

        self.init_sources()

    def create_note(self, args):
        note = Note()

        note.folder = self.get_folder_from_arg(args)
        note.title = self.get_title_from_arg(args)
        note.createdAt = self.get_create_at_from_arg(args)
        note.updatedAt = self.get_update_at_from_arg(args)
        note.tags = []

        note.content = self.migrate(args)

        return note

    def init_sources(self):
        for root, dir, filenames in os.walk(self._path):
            for filename in fnmatch.filter(filenames, '*.md'):
                full_path = os.path.join(root, filename)
                with open(full_path, 'r', encoding='utf-8') as fp:
                    contents = fp.read()
                self.sources[filename] = {'filename': filename,
                                          'full_path': full_path,
                                          'uuid': str(uuid4()),
                                          'contents': contents}

    def get_folder_from_arg(self, arg: dict) -> str:
        if 'Default' not in self.folders:
            self.folders.append('Default')
        return 'Default'

    def get_title_from_arg(self, arg: dict) -> str:
        return arg['filename'].split('.')[0].replace('/', '_')

    def get_create_at_from_arg(self, arg: dict) -> str:
        return creation_date(arg['full_path'], self.date_format)

    def get_update_at_from_arg(self, arg: dict) -> str:
        return update_date(arg['full_path'], self.date_format)

    def get_filename_from_arg(self, arg: dict) -> str:
        return arg['uuid']
