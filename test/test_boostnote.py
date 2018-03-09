# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from boostnote import Boostnote
    path = r'C:\Users\Owner\Boostnote'
    note = Boostnote(path)
    # print(note)
    print(note.__repr__())

    for storage, note in note.walk_note():
        print('\t'.join([storage.name, note.title]))
        print(note.__repr__())
