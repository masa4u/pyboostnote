# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from boostnote import Boostnote
    path =[r'e:\fng\boostnote']

    bnote = Boostnote(path)
    for storage, folder, note in bnote.walk_note():
        print('\t'.join([folder.name, note.title]))
        print(note.__repr__())
        exit()
