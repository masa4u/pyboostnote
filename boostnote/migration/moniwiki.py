# -*- coding: utf-8 -*-
import os
import re
import requests
from urllib.parse import urlparse, unquote, quote, urlsplit
from urllib import request

from uuid import uuid4
from boostnote.migration.wiki import MigrationWiki
from boostnote.migration.converter import MigrationConverter
from boostnote.migration.moniwiki_util import moniwiki_page_link, moniwiki_page_attach
from bs4 import BeautifulSoup


def download_file(url, dest=None, filename=None):
    u = request.urlopen(url)

    if not filename:
        filename = 'downloaded.file'
    if dest:
        filename = os.path.join(dest, filename)

    with open(filename, 'wb') as fp:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func('Content-Length')
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print('Downloading: {0} Bytes: {1}'.format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            fp.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()
    return filename


def skip_page(title_name):
    skip_pages = ['FrontPage', 'FindPage', 'TitleIndex', 'RecentChanges', 'UserPreferences']
    if '&' in title_name or '?' in title_name or title_name in skip_pages:
        return True
    return False


def report_changes(o: str, n: str):
    print('-old-')
    print(o)
    print('-new-')
    print(n)


def split_processor(_code: str):
    rlt = []
    block_start = '[\s]*[\{]{3}'
    block_end = '[\}]{3}'
    new_line = []
    in_block = False
    for row in _code.split('\n'):
        if in_block is False and re.match(block_start, row):
            rlt.append(['inline', '\n'.join(new_line)])
            new_line = [row]
            in_block = True
        elif in_block and re.match(block_end, row):
            new_line.append(row)
            rlt.append(['block', '\n'.join(new_line)])
            new_line = []
            in_block = False
        else:
            new_line.append(row)
    rlt.append(['inline', '\n'.join(new_line)])
    return rlt


class MoniwikiConverter(MigrationConverter):
    special = ''.join(['\\' + x for x in '+-*/=_ .,;:!?#&$%@|^(){}[]~<>\'"\\'])
    note_replace = [
        # Headings
        ('h1', '(= )(.*?)([ ]+=)\n', '# \\2\n'),
        ('h2', '([=]{2} )(.*?)([ ]+[=]{2})\n', '## \\2\n'),
        ('h3', '([=]{3} )(.*?)([ ]+[=]{3})\n', '### \\2\n'),
        ('h4', '([=]{4} )(.*?)([ ]+[=]{4})\n', '#### \\2\n'),
        ('h5', '([=]{4} )(.*?)([ ]+[=]{4})\n', '##### \\2\n'),

        # special func
        ('toc', '\[\[TableOfContents\]\]', '[TOC]'),

        # Emphasis
        ('e1', "([']{3})(.*?)([']{3})", '**\\2**'),
        ('e2', "([']{2})(.*?)([']{2})", '*\\2*'),

        # code
        ('code-block', '([ ]*)[\{]{3}(#![a-z]+ ([a-z ]+)|)\n([\w\s가-힣' + special + ']*)[\}]{3}\n',
         '\\1```\\3\n\\4\n```\n'),

        # Link
        ('link', '(\[)(http[s]?://[\w\-./%#가-힣]+) ([a-zA-Z0-9.가-힣 \+\/]+)(\])', '[\\3](\\2)'),

        # Table
        # ('table', '\[|]{2}(?:([^\r\n}]*)\|\|)+\r?', '|')
    ]

    @classmethod
    def convert_contents(cls, contents: str, method=[]) -> str:
        old_contents = contents
        for key, from_rep, to_rep in cls.note_replace:
            if method == []:
                old_contents = re.sub(from_rep, to_rep, old_contents, re.UNICODE)
            elif key in method:
                if cls.verbose:
                    matchs = re.findall(from_rep, old_contents)
                    if len(matchs) > 0:
                        for match in matchs:
                            print(match)
                old_contents = re.sub(from_rep, to_rep, old_contents, re.UNICODE)

        return old_contents


def empty_or_notfound(wiki_text: str):
    return wiki_text == '' or wiki_text[0] == '<'


def get_wiki_text_from_url(url: str) -> str:
    wiki_data = requests.get(url)
    wiki_text = wiki_data.text.encode(wiki_data.encoding).decode('utf-8')

    return wiki_text


class Moniwiki(MigrationWiki):
    converter = MoniwikiConverter

    def __init__(self, wiki_root_url):
        super().__init__(wiki_root_url)

        parse_object = urlparse(wiki_root_url)
        root_url = '%s://%s' % (parse_object.scheme, parse_object.netloc)
        self.wiki_path = wiki_root_url.replace(root_url, '')
        full_url = root_url + self.wiki_path + 'wiki.php/%s'

        r = requests.get(full_url % 'TitleIndex')
        soup = BeautifulSoup(r.text, 'html.parser')

        no = 0
        for item in soup.find_all('li'):
            wiki_title = self.get_wiki_title(item)
            if skip_page(wiki_title):
                continue
            wiki_root_url = full_url % quote(wiki_title) + '?action=raw'
            wiki_text = get_wiki_text_from_url(wiki_root_url)
            if empty_or_notfound(wiki_text):
                print('wiki_url is empty(%s)' % wiki_root_url)
                continue

            self.append_source(wiki_title, {
                'wiki_title': wiki_title,
                'wiki_url': wiki_root_url,
                'contents': wiki_text,
                'uuid': str(uuid4()),
                'links': {},
                'images': {},
            })
            no = no + 1

        self.init_source()
        for key, value in self.sources.items():
            self.init_wiki(value)
        print('%d files loaded' % no)

    def get_folder_from_arg(self, arg: dict) -> str:
        spilt_title = arg['wiki_title'].split('/')
        if len(spilt_title) > 1:
            self.folders.append(spilt_title[0])
            return spilt_title[0]
        if 'Default' not in self.folders:
            self.folders.append('Default')
        return 'Default'

    def get_title_from_arg(self, arg: dict) -> str:
        return arg['wiki_title'].replace('/', '_')

    def get_create_at_from_arg(self, arg: dict) -> str:
        from boostnote.migration.util import creation_date, update_date
        return creation_date(r'c:\temp', self.date_format)

    def get_update_at_from_arg(self, arg: dict) -> str:
        from boostnote.migration.util import creation_date, update_date
        return creation_date(r'c:\temp', self.date_format)

    def get_filename_from_arg(self, arg: dict) -> str:
        return arg['uuid']

    def get_wiki_title(self, item) -> str:
        title_name = item.find('a').get('href').replace(self.wiki_path + 'wiki.php', '')
        if title_name[0] == '?' or title_name[0] == '/':
            title_name = title_name[1:]
        return unquote(title_name)

    def get_tags_from_arg(self, arg: dict) -> list:
        tags = []
        s = arg['wiki_title'].split('/')
        if len(s) > 0:
            tags.append(s[0])

        return tags

    def init_source(self):
        for key, args in self.sources.items():
            self.init_wiki(args)

    def init_wiki(self, args: dict):

        wiki_title = args['wiki_title']
        wiki_page = args['contents']

        source = self.sources[wiki_title]

        # init moniwiki link pages
        for idx, link_name, full_link in moniwiki_page_link(wiki_title, wiki_page):

            if full_link in self.sources:
                source['links'][link_name] = self.sources[full_link]['uuid']
                # print('%d %s => %s(%s)' % (idx, wiki_title, link_name, self.sources[full_link]['uuid']))

        # init moniwiki attach
        for idx, match_str, image_name, full_url in moniwiki_page_attach(self.wiki_root_url, wiki_title, wiki_page):
            source['images'][match_str] = {'name': image_name, 'full_url': full_url}

    def migrate(self, args: dict) -> str:
        contents = self.converter.convert_contents(args['contents'])
        source = self.sources[args['wiki_title']]
        for rep, link in source['links'].items():
            contents = contents.replace('[%s]' % rep, '[%s](:note:%s)' % (rep, link))

        download = True
        image_path = os.path.join(self.target_folder, 'images')
        for rep, link in source['images'].items():
            if download and self.wiki_root_url in link['full_url']:
                filename = link['name']
                orgname = '.'.join(filename.split('.')[:-1])
                ext = filename.split('.')[-1]
                idx = 0
                while os.path.exists(os.path.join(image_path, filename)):
                    filename = '%s_%d.%s' % (orgname, idx, ext)
                    idx = idx + 1
                download_file(link['full_url'], image_path, filename)
                contents = contents.replace(rep, '![%s](\\:storages\\%s)' % (link['name'], filename))
            else:
                contents = contents.replace(rep, '![%s](%s)' % (link['name'], link['full_url']))
        return contents


if __name__ == '__main__':
    wiki = Moniwiki('http://172.21.39.15/moniwiki/')
    wiki.do_import(r'c:\temp\moniwiki')
    exit()

    conveter = MoniwikiConverter


    def get_code(url):
        res = requests.get(url)
        return res.text.encode(res.encoding).decode('utf-8')


    code = '\n'.join(
        get_code('http://172.21.39.15/moniwiki/wiki.php/PriceItFrontArena/Linking/ATLComDLL?action=raw').split('\n')[
        :160])

    split_processor(code)
    exit()

    # o = wiki.sources['CodingStandard/c']['contents'][-1000:-500]
    n = conveter.convert_contents(code, ['code-block'])
    # report_changes(o, n)
    print(n)
