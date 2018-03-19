# -*- coding: utf-8 -*-

from boostnote.migration.files import MigrationFiles


class MarkdownGollum(MigrationFiles):
    def import_file(self, sub, filename):
        print('path=\"%s\", filename=%s' % (sub, filename))

if __name__ == '__main__':
    md_storage = MarkdownGollum(r'C:\fng\wiki')
    print(md_storage)
    md_storage.do_import(r'c:/fng/temp')
