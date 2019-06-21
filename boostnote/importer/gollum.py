# -*- coding: utf-8 -*-

from boostnote.importer.files import FilesImpoter


class MarkdownGollum(FilesImpoter):
    def import_file(self, sub, filename):
        print('path=\"%s\", filename=%s' % (sub, filename))
