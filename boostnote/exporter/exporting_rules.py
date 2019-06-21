# -*- coding: utf-8 -*-

from enum import Enum
from dataclasses import dataclass


class AttachPathType(Enum):
    LinkRelativePath = 0
    CopyToMarkdownPath = 1
    CopyToMarkdownSubPath = 2
    LinkRelativePathBaseRoot = 3


@dataclass
class ExportingRules(object):
    tagging_name: str = 'tags'
    folder_to_tags: bool = False
    attachment_method: AttachPathType = AttachPathType.LinkRelativePath


DefaultMarkDownRules = ExportingRules()
NotableRule = ExportingRules('tags', True, AttachPathType.LinkRelativePathBaseRoot)

if __name__ == '__main__':
    print(DefaultMarkDownRules)
    print(NotableRule)
