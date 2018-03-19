# -*- coding: utf-8 -*-
import os
import fnmatch
import json

from enum import Enum

from boostnote.note import Note


class MarkdownStorage(object):
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(path)

        self._path = path

    def walk_target(self):
        for root, _, filenames in os.walk(self._path):
            for filename in fnmatch.filter(filenames, '*.md'):
                full_path = os.path.join(root, filename)
                yield root.replace(self._path, ''), filename, full_path

    def storage_import(self, sub, filename):
        raise NotImplementedError()

    def generate_boostnote(self, dir, filename, fullpath) -> Note:
        title = filename.split('.')[0]
        note = Note.create_note(dir, title, fullpath)

        return note

    def do_import(self, target_folder):
        boostnote = {
            'folders': [],
            'version': '1.0'
        }
        note_path = os.path.join(target_folder, 'notes')
        if not os.path.exists(note_path):
            os.mkdir(note_path)

        folders = []
        for dir, filename, full_path in self.walk_target():
            folder = dir[1:] if len(dir) > 0 and dir[0] == '\\' else dir
            if folder == '':
                folder = 'Default'
            else:
                folder = folder.replace('\\', '_')
            if folder not in folders:
                boostnote['folders'].append({'name': folder, 'key': folder, 'color': '#6AA5E9'})
                folders.append(folder)

            note = self.generate_boostnote(folder, filename, full_path)

            target_file = os.path.join(note_path, note.title + '.cson')
            note.dump_file(target_file)

        with open(os.path.join(target_folder, 'boostnote.json'), 'w') as fp:
            json.dump(boostnote, fp)

    def __str__(self):
        return '<%s: %d>' % (self.__class__.__name__, 0)
