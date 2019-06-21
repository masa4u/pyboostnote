# -*- coding: utf-8 -*-
import re
import requests
from urllib.parse import urljoin, quote

special = ''.join(['\\' + x for x in '+-*/=_ .,;:!?#&$%@|^(){}[]~<>\'"\\'])


def moniwiki_page_link(wiki_title: str, wiki_text: str):
    target_page = wiki_text
    link_pattern = '\[([[^\w가-힣\/\. ]+)\]'

    # remove code
    inner_code = '([ ]*)[\{]{3}(#![a-z]+ ([a-z ]+)|)\n([\w\s가-힣' + special + ']*)[\n\}]{3}\n'
    target_page = re.sub(inner_code, '', target_page)

    # toc
    target_page = re.sub('[\[]{2}([\w가-힣]+)[\]]{2}', '', target_page)

    matchs = re.findall(link_pattern, target_page)
    if len(matchs) > 0:
        for idx, link_name in enumerate(matchs):
            full_link = link_name
            if link_name[:2] == './':
                full_link = wiki_title + link_name[1:]
            yield idx, link_name, full_link


def moniwiki_url(title) -> str:
    def upper_str(match):
        return '_' + match.group(3).lower()

    quote_title = quote(title, safe='')
    pattern = '(([\%])([A-F0-9]{2}))'
    quote_title = re.sub(pattern, upper_str, quote_title)

    return quote_title


def moniwiki_pds_url(wiki_root: str, title: str) -> str:
    title_encode = moniwiki_url(title)
    pds_root = urljoin(wiki_root, 'pds/%s' % title_encode)

    return pds_root


def url_exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def moniwiki_page_attach(wiki_root: str, wiki_title: str, wiki_text: str):
    pds_base = moniwiki_pds_url(wiki_root, wiki_title)

    patterns = [('(\[\[[cC][lL][iI][pP]\()([a-zA-Z0-9]+)(\)\]\])', lambda x: x[1] + '.png'),
                ('(attachment\:)([a-zA-Z0-9_+\-\.\[\]\@가-힣]+.[a-z0-0]+)', lambda x: x[1])]
    for pattern, rep in patterns:
        matchs = re.findall(pattern, wiki_text)
        for idx, match in enumerate(matchs):
            full_url = urljoin(pds_base + '/', quote(rep(match)))
            if url_exists(full_url):
                yield idx, ''.join(match), rep(match), full_url
            else:
                print('not found: %s' % full_url)


if __name__ == '__main__':
    wiki_text = '''
    [[Clip(menu)]]
[[Clip(search)]]

'IVSDAX_DW', 'IVSRU_DW', 'IVSHSI_DW', 'IVSXIN9I_DW', 'IVSAS51_DW');
   (2016개 있어야 한다)
attachment:그림2.jpg
fdsa 
    '''
    matchs = moniwiki_page_attach('http://172.21.39.15/moniwiki/', 'Daily업무/OptPremium', wiki_text)
    for idx, match, full_url in matchs:
        print(idx, match, full_url)
