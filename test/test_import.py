# -*- coding: utf-8 -*-
import os
import cson
from tabulate import tabulate

path = r'C:\Users\Owner\Boostnote\notes'
file_name = '63a94ae29718dd240436.cson'
# file_name = '29744262a47e574f877e.cson'

with open(os.path.join(path, file_name), 'rb') as fp:
    data = cson.load(fp)
    print(tabulate(data.items()))