[![Build Status](https://travis-ci.org/masa4u/pyboostnote.svg?branch=master)](https://travis-ci.org/masa4u/pyboostnote)
[![Coverage Status](https://coveralls.io/repos/github/masa4u/pyboostnote/badge.svg?branch=master)](https://coveralls.io/github/masa4u/pyboostnote?branch=master)

# pyboostnote

boostnote.io python data handler(importer / exporter)

## support impoters
 * moniwiki
 * gollum

## export to normal markdown

Using export_to_md.py, you can export BOOSTNOTE markdown to normalized markdown.

It remove ':storage' and ':note' link and add front-meta(PANDOC) headings.

It support below attachment link types,
 * LinkRelativePath
 * CopyToMarkdownPath
 * CopyToMarkdownSubPath

```python
from boostnote.base import Boostnote
from boostnote.exporter.markdown import export_boostnote
from boostnote.exporter.exporting_rules import AttachPathType

source_path = 'c:/temp/boostnote'
target_path = 'c:/temp/boostnote_export'

boostnote = Boostnote([source_path])
storage = boostnote.storages['Default0']

export_boostnote(storage, target_path, AttachPathType.CopyToMarkdownPath)
```

## Future Updates

### importer

* adding unittest and migration examples

### exporter
 * 
