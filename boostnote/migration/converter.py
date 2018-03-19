# -*- coding: utf-8 -*-


class MigrationConverter(object):
    verbose = False
    def __init__(self, _migration_base):
        self.base = _migration_base

    def converter(self, note):
        raise NotImplementedError()

if __name__ == '__main__':
    pass