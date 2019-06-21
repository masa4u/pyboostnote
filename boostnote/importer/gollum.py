# -*- coding: utf-8 -*-

from boostnote.importer.files import FilesImpoter


class MarkdownGollum(FilesImpoter):
    def import_file(self, sub, filename):
        print('path=\"%s\", filename=%s' % (sub, filename))

if __name__ == '__main__':
    md_storage = MarkdownGollum(r'C:\fng\wiki')
    print(md_storage)
    md_storage.do_import(r'c:/fng/temp')
