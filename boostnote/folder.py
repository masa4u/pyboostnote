# -*- coding: utf-8 -*-


class Folder(object):
    def __init__(self, name, key, color):
        self._name = name
        self._key = key
        self._color = color
        self._notes = []

    def get_path(self):
        return self._path

    path = property(fget=get_path)

    def get_name(self):
        return self._name

    name = property(fget=get_name)

    def get_key(self):
        return self._key

    key = property(fget=get_key)

    def get_color(self):
        return self._color

    color = property(fget=get_color)

    def get_notes(self) -> list:
        return self._notes

    notes = property(fget=get_notes)

    def __str__(self):
        return '<Storage: %s, key=%s, note=%d>' % (self.name, self.key, len(self.notes))

    def __repr__(self):
        rlt = []
        rlt.append(self.__str__())
        for note in self.notes:
            rlt.extend(list(map(lambda x: '  ' + x, note.__repr__().split('\n'))))

        return '\n'.join(rlt)
