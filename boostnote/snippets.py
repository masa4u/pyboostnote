# -*- coding: utf-8 -*-

class Snippet(dict):
    def get_name(self):
        return self['name']

    name = property(fget=get_name)

    def get_mode(self):
        return self['mode']

    mode = property(fget=get_mode)

    def get_content(self):
        return self['content']

    content = property(fget=get_content)


class Snippets(list):
    pass
