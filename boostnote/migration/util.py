# -*- coding: utf-8 -*-
import os
import platform
import re

from datetime import datetime


def time_convert(dt: datetime, format: str):
    return datetime.utcfromtimestamp(dt).strftime(format)


def creation_date(path_to_file: str, format: str):
    if platform.system() == 'Windows':
        t = os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            t = stat.st_birthtime
        except AttributeError:
            t = stat.st_mtime

    return time_convert(t, format)


def update_date(path_to_file: str, format: str):
    return time_convert(os.path.getmtime(path_to_file), format)


def is_hangul(text):
    hanguul_re = re.compile(r'[ㄱ-ㅣ가-힣]')
    return hanguul_re.search(text) is not None
