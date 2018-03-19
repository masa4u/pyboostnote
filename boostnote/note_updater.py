# -*- coding: utf-8 -*-
from boostnote import Boostnote
import re


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
                    print('\n<storage=%s folder=%s note=%s(%s)>' % (
                        storage._path, folder.name, note.title, note.uuid))
                    print('=> %s ... %d matchs found' % (from_rep.replace('\n', '\\n'), len(matchs)))
                    for idx, match in enumerate(matchs):
                        print('%02d : %s' % (idx, match))

    def do_update(self):
        for storage, folder, note in self.boostnote.walk_note():
            content = note.content
            # print(content)

            for from_rep, to_rep in self._note_replace:
                if note.title == 'GitSVN':
                    print('%s => ' % from_rep)
                content = re.sub(from_rep, to_rep, content)
                if content != note.content:
                    print('%s note changed(%s)=>(%s)' % (note.title, from_rep, to_rep))
            note.content = content
            if self.verbose is True:
                old = content.split('\n')
                for old_line, new_line in zip(old, content.split('\n')):
                    if (old_line != new_line):
                        print('  ' + old_line)
                        print('=>' + new_line)

    def do_rename_file(self, name_pattern='{path}\\notes\{folder_name}_{title}.cson'):

        for storage, folder, note in self.boostnote.walk_note():
            named_dict = {}
            named_dict.update({'folder_key': folder.key,
                               'folder_name': folder.name,
                               'path': storage._path
                               })
            named_dict.update(note._data)
            print(note.filename)
            note.filename = name_pattern.format(**named_dict)
            print(note.filename)

    def find_inner_link(self):
        link_pattern = '\[([\w ]+)\]\(\:note\:([\w]+)\)'
        for storage, folder, note in self.boostnote.walk_note():
            matchs = re.findall(link_pattern, note.content)
            if len(matchs) > 0:
                for idx, (link_name, cson) in enumerate(matchs):
                    if cson in storage.notes:
                        print('%02d : %s ==> %s' % (idx, cson, storage.notes[cson]))
                    else:
                        print('%02d : %s ==> broken link' % (idx, cson))



if __name__ == '__main__':
    from boostnote.settings import config
    print(config.path)
    bnote = Boostnote([r'C:\TEMP\moniwiki'])
    updater = NoteUpdater(bnote, True)

    # Headings
    updater.add_replace('([#]+ )(.*?)([ ]+[#]+)\n', '\\1\\2\n')
    updater.add_replace('(= )(.*?)([ ]+=)\n', '# \\2\n')
    updater.add_replace('([=]{2} )(.*?)([ ]+[=]{2})\n', '## \\2\n')
    updater.add_replace('([=]{3} )(.*?)([ ]+[=]{3})\n', '### \\2\n')
    updater.add_replace('([=]{4} )(.*?)([ ]+[=]{4})\n', '#### \\2\n')
    # special func
    updater.add_replace('\[\[TableOfContents\]\]', '[TOC]')
    # Emphasis
    updater.add_replace("([']{3})(.*?)([']{3})", "**\\2**")
    updater.add_replace("([']{2})(.*?)([']{2})", "*\\2*")
    # code
    special = ''.join(['\\' + x for x in '+-*/= .,;:!?#&$%@|^(){}[]~<>\''])
    inner_code = '[ ]*[\{]{3}([#!a-z ]*)\n([\w\s가-힣' + special + ']*)[\}]{3}'
    updater.add_replace(inner_code, '```\\1```\n')
    # Link
    updater.add_replace(
        '(\[)(http[s]?://[\w\-./%#가-힣]+) ([a-zA-Z0-9.가-힣 \+\/]+)(\])',
        '[\\3](\\2)')

    # updater.do_rename_file()
    # updater.find_inner_link()
    updater.do_update()
    # updater.check()
    bnote.save_notes()
