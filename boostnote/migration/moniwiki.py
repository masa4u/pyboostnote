# -*- coding: utf-8 -*-
import re
import requests

from bs4 import BeautifulSoup


class WikiBase(object):
    def __init__(self, wiki_url):
        self._source = {}

    def get_source(self):
        return self._source

    source = property(fget=get_source)


class Moniwiki(WikiBase):
    def __init__(self, wiki_url):
        super().__init__(wiki_url)

        full_url = wiki_url + 'wiki.php?%s'

        r = requests.get(full_url % 'TitleIndex')
        soup = BeautifulSoup(r.text, "html.parser")

        skip_pages = ['FrontPage', 'FindPage', 'TitleIndex', 'RecentChanges', 'UserPreferences']
        for item in soup.find_all('li'):
            title_name = item.find('a').get('href').replace('/wiki.php?', '')
            if '&' in title_name or title_name in skip_pages:
                continue

            wiki_data = requests.get(full_url % title_name + '&action=raw')
            self.source[title_name] = wiki_data.text
            # print(wiki_data.text)
            self.init_wiki(self.source[title_name])

    def init_wiki(self, wiki_page: str):
        link_pattern = '\[([\w ]+)\]'
        matchs = re.findall(link_pattern, wiki_page)
        if len(matchs) > 0:
            for idx, link_name in enumerate(matchs):
                print('%02d : %s ==> broken link' % (idx, link_name))


if __name__ == '__main__':
    wiki = Moniwiki('http://wiki.cguru.org/')
