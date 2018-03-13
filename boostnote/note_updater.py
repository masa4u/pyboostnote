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
                    storage._path, folder.name, note.title, note.filename))
                    print('=> %s ... %d matchs found' % (from_rep.replace('\n', '\\n'), len(matchs)))
                    for idx, match in enumerate(matchs):
                        print('%02d : %s' % (idx, match))

    def do_update(self):
        for storage, folder, note in self.boostnote.walk_note():
            for from_rep, to_rep, regex in self._note_replace:
                contents = note.content
                contents = re.sub(from_rep, to_rep, contents)
                note.content = contents
            exit()


if __name__ == '__main__':
    path = [r'C:\Users\masa\Boostnote']
    bnote = Boostnote(path)
    updater = NoteUpdater(bnote, True)

    # Headings
    updater.add_replace('([#]+ )(.*?)([ ]+[#]+)\n', '\n\\1 \\2\n')
    updater.add_replace('(= )(.*?)([ ]+=)\n', '# \\2\n')
    updater.add_replace('([=]{2} )(.*?)([ ]+[=]{2})\n', '## \\2\n')
    updater.add_replace('([=]{3} )(.*?)([ ]+[=]{3})\n', '### \\2\n')
    updater.add_replace('([=]{4} )(.*?)([ ]+[=]{4})\n', '#### \\2\n')
    # special func
    updater.add_replace('\[\[TableOfContents\]\]', '[[TOC]]')
    # Emphasis
    updater.add_replace("([']{3})(.*?)([']{3})", "**\\2**")
    # Link
    updater.add_replace(
        '(\[)(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+) ([a-zA-Z0-9.\+\/]+)(\])',
        '')

    updater.check()
