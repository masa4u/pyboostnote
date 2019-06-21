# -*- coding: utf-8 -*-
import os
import json
from boostnote.note import Note


class BaseImpoter(object):
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    converter = None

    def __init__(self):
        self._folders = []
        self._sources = {}
        self.target_folder = None

    def get_sources(self):
        return self._sources

    sources = property(fget=get_sources)

    def init_source(self):
        pass

    def get_folders(self):
        return self._folders

    folders = property(fget=get_folders)

    def walk_source(self):
        raise NotImplementedError

    def storage_import(self, sub, filename):
        raise NotImplementedError()

    def create_note(self, args: dict) -> Note:
        note = Note()

        note.folder = self.get_folder_from_arg(args)
        note.title = self.get_title_from_arg(args)
        note.createdAt = self.get_create_at_from_arg(args)
        note.updatedAt = self.get_update_at_from_arg(args)
        note.tags = self.get_tags_from_arg(args)

        note.content = self.migrate(args)

        return note

    def get_folder_from_arg(self, arg: dict) -> str:
        raise NotImplementedError()

    def get_title_from_arg(self, arg: dict) -> str:
        raise NotImplementedError()

    def get_create_at_from_arg(self, arg: dict) -> str:
        raise NotImplementedError()

    def get_update_at_from_arg(self, arg: dict) -> str:
        raise NotImplementedError()

    def get_filename_from_arg(self, arg: dict) -> str:
        raise NotImplementedError()
    def get_tags_from_arg(self, arg: dict) -> list:
        raise NotImplementedError()

    def migrate(self, args: dict) -> str:
        # print(args)
        return args['contents']

    def check_source_value(self, value):
        if 'contents' not in value:
            raise ValueError('contents not found')
        if 'uuid' not in value:
            raise ValueError('uuid not found')

    def append_source(self, key, value):
        self.check_source_value(value)
        self.sources[key] = value

    def do_import(self, target_folder):
        self.target_folder = target_folder

        note_path = os.path.join(target_folder, 'notes')
        if not os.path.exists(note_path):
            os.mkdir(note_path)

        for key, args in self.sources.items():
            note = self.create_note(args)
            if self.converter:
                note.content = self.converter.convert_contents(note.content)

            target_file = os.path.join(note_path, self.get_filename_from_arg(args) + '.cson')
            note.dump_file(target_file)

        with open(os.path.join(target_folder, 'boostnote.json'), 'w') as fp:
            def folder_sync(folder):
                return {'name': folder, 'key': folder, 'color': '#6AA5E9'}

            boostnote = {
                'folders': list(map(lambda x: folder_sync(x), self.folders)),
                'version': '1.0'
            }
            json.dump(boostnote, fp)

    def __str__(self):
        return '<%s: %d>' % (self.__class__.__name__, len(self.sources))
