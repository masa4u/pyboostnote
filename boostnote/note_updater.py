# -*- coding: utf-8 -*-
import re

from boostnote import Boostnote
from boostnote.note import NoteType
from boostnote.settings import logger


class NoteUpdater(object):
    def __init__(self, boostnote: Boostnote, verbose=False):
        self._boostnote = boostnote
        self._note_replace = []
        self._verbose = verbose

    def get_boostnote(self):
        return self._boostnote

    boostnote = property(fget=get_boostnote)

    def get_verbose(self):
        return self._verbose

    verbose = property(fget=get_verbose)

    def add_replace(self, from_replace, to_replace):
        # regex = re.compile(from_replace, re.UNICODE | re.MULTILINE)
        self._note_replace.append([from_replace, to_replace])

    def check(self):
        for storage, folder, note in self.boostnote.walk_note():
            for from_rep, to_rep in self._note_replace:
                matchs = re.findall(from_rep, note.content)  # , re.DOTALL)
                if self.verbose and len(matchs) > 0:
                    logger.info('\n<storage=%s folder=%s note=%s(%s)>' % (
                        storage._path, folder.name, note.title, note.uuid))
                    logger.info('=> %s ... %d matchs found' % (from_rep.replace('\n', '\\n'), len(matchs)))
                    for idx, match in enumerate(matchs):
                        logger.info('%02d : %s' % (idx, match))

    def do_update(self):
        for storage, folder, note in self.boostnote.walk_note():
            content = note.content

            for from_rep, to_rep in self._note_replace:
                content = re.sub(from_rep, to_rep, content)
                if content != note.content:
                    logger.info('%s note changed(%s)=>(%s)' % (note.title, from_rep, to_rep.strip()))
            note.content = content
            if self.verbose is True:
                old = content.split('\n')
                for old_line, new_line in zip(old, content.split('\n')):
                    if (old_line != new_line):
                        logger.info('  ' + old_line)
                        logger.info('=>' + new_line)

    def do_rename_file(self, name_pattern='{path}\\notes\{folder_name}_{title}.cson'):

        for storage, folder, note in self.boostnote.walk_note():
            named_dict = {}
            named_dict.update({'folder_key': folder.key,
                               'folder_name': folder.name,
                               'path': storage._path
                               })
            named_dict.update(note._data)
            logger.info(f'old={note.filename}')
            note.filename = name_pattern.format(**named_dict)
            logger.info(f'new={note.filename}')

    def find_inner_link(self):
        link_pattern = '\[([\w ]+)[\]|\/]\(\:note\:([\w]+)\)'
        for storage, folder, note in self.boostnote.walk_note():
            if note.type == NoteType.SNIPPET_NOTE:
                continue
            matchs = re.findall(link_pattern, note.content)
            if len(matchs) > 0:
                for idx, (link_name, cson) in enumerate(matchs):
                    if cson in storage.notes:
                        logger.info('%02d : %s ==> %s' % (idx, cson, storage.notes[cson]))
                    else:
                        logger.info('%02d : %s ==> broken link' % (idx, cson))
