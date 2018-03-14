# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from boostnote.settings import config
    from boostnote import Boostnote

    bnote = Boostnote(config.path)
    for storage, folder, note in bnote.find_note(lambda x: x.title == 'ubuntu'):
        print(note)

    exit()
    for storage, folder, note in bnote.walk_note():
        print('\t'.join([folder.name, note.title]))
        print(note.__repr__())
        exit()
