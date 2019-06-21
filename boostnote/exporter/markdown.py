# -*- coding: utf-8 -*-
import codecs
import os
import re
from shutil import copy2

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import yaml

from boostnote.base import Boostnote, Storage
from boostnote.note import NoteType, Note
from boostnote.exporter.exporting_rules import AttachPathType
from boostnote.settings import logger

YAML_START = '---\n'
YAML_END = '\n---\n'


def default_representer(dumper, data):
    """
    writing pandoc metadata heading

    https://pandoc.org/MANUAL.html#metadata-variables
    """
    meta_key_order = [
        'title', 'author', 'date',
        'subtitle', 'abstract', 'keywords',
        'subject',
        'description', 'category']
    data = sorted(data.items(),
                  key=lambda x: 99 if x[0] not in meta_key_order else meta_key_order.index(x[0]))
    return dumper.represent_dict(data)


Dumper.add_representer(dict, default_representer)



def normalize_filename(org) -> str:
    """
    < (less than)
    > (greater than)
    : (colon)
    " (double quote)
    / (forward slash)
    \\ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)
    """

    map_str = r'<>:"/\|?*'
    chg_str = r'---______'

    return ''.join([chg_str[map_str.find(x)] if x in map_str else x for x in org])


def uuid_to_md_path(storage: Storage, export_to_path, uuid) -> str:
    note_target: Note = storage.notes[uuid]
    folder_path = os.path.join(export_to_path, storage.folders[note_target.folder].name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    md_source_path = os.path.join(folder_path, normalize_filename(note_target.title))
    if not os.path.exists(md_source_path):
        os.mkdir(md_source_path)
    return md_source_path


def split_frontmeta_and_content(content):
    """
    split fonrtmeta(pandoc style) and contents data from original string
    """
    start_len = len(YAML_START)
    note_metadata = dict()
    has_front_meta = content.startswith(YAML_START) and len(content[start_len:].split(YAML_END)) > 0
    if has_front_meta:
        content_string = content[start_len:]
        meta_index = content_string.find(YAML_END)
        meta_string, content = content_string[:meta_index], content_string[meta_index + 1:]
        note_metadata = yaml.load(meta_string, Loader=yaml.SafeLoader)

    return note_metadata, content


def to_normal_md(s: Storage, n: Note, export_to_path,
                 export_attach_method=AttachPathType.LinkRelativePath) -> bool:
    """
    export boost markdown to normal markdown

    1. remove :storage, :note
    2. insert front-meta data
    """

    # preparing variables for converting
    export_folder_path = os.path.join(export_to_path, s.folders[n.folder].name)
    if not os.path.exists(export_folder_path):
        os.mkdir(export_folder_path)
    filename = normalize_filename(n.title)
    md_storage = os.path.join(export_folder_path, filename)

    # split front-meta and content
    note_metadata, content = split_frontmeta_and_content(n.content)

    # remove :storage
    rx_storage = re.compile(r'\(:storage[\\|/]([a-z0-9\-]+)[\\|/]([\w\.]+)\)', re.MULTILINE)

    for match in rx_storage.finditer(content):
        uuid, linkname = match.groups()

        # link methos
        link_source_path = os.path.join(s._path, 'attachments', uuid, linkname)
        if export_attach_method == AttachPathType.LinkRelativePath:
            link_target_path = os.path.join(uuid_to_md_path(s, export_to_path, uuid), linkname)
        elif export_attach_method == AttachPathType.CopyToMarkdownSubPath:
            link_target_path = os.path.join(md_storage, linkname)
        elif export_attach_method == AttachPathType.CopyToMarkdownPath:
            link_target_path = os.path.join(export_folder_path, linkname)
        else:
            raise ValueError('not support variable type')

        if not os.path.exists(link_target_path):
            if not os.path.exists(os.path.dirname(link_target_path)):
                os.mkdir(os.path.dirname(link_target_path))
            if not os.path.exists(link_source_path):
                logger.info(f'missing file {n.title}/{linkname}')
            else:
                copy2(link_source_path, link_target_path)

        # replace \\ type path name to / type, \\ occur error in windows case
        link_target_path = os.path.relpath(link_target_path, export_folder_path)
        link_target_path = link_target_path.replace('\\', '/')
        content = content.replace(match.group(),
                                  f'({link_target_path})'
                                  )

    # remove :note
    rx_note_link = re.compile(r'\(:note:([a-z0-9\-]+)\)')
    for match in rx_note_link.finditer(content):
        uuid = match.groups()[0]
        link_target_path = os.path.join(uuid_to_md_path(s, export_to_path, uuid) + '.md')

        content = content.replace(match.group(),
                                  f'({link_target_path})'
                                  )
    # update front-meta
    keywords = n.tags
    if 'tags' in note_metadata:
        keywords.extend(note_metadata['tags'])
    if keywords != []:
        note_metadata['keywords'] = list(set(keywords))

    with codecs.open(os.path.join(export_folder_path, filename + '.md'), 'w', "utf-8") as fp:
        if note_metadata != {}:
            yaml_string = yaml.dump(note_metadata, Dumper=Dumper, default_flow_style=False, allow_unicode=True)
            fp.write('\n'.join(['---', yaml_string[:-1], '---\n']))
        fp.write(content)

    return True


def export_boostnote(storage: Storage, export_to_path: str, export_attach_method: AttachPathType):
    if not os.path.exists(export_to_path):
        raise Exception(f'{export_to_path} not exists')

    folder_name = {}
    for uuid, folder in storage.folders.items():
        folder_path = os.path.join(export_to_path, folder.name)
        folder_name[uuid] = folder.name
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    for folder, note in storage.walk_note():
        if note.type == NoteType.SNIPPET_NOTE:
            continue
        to_normal_md(storage, note, export_to_path, export_attach_method)



