#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

import sysconfig
from slide import Slide
from verse import Verse

class SlideFormatter:
    def __init__(self):
        self._header = sysconfig.header_template
        self._footer = sysconfig.footer_template

    def glue(self, verses):
        text_out = []
        tmpl = sysconfig.template_file_get(self._header)
        with codecs.open(tmpl, encoding='utf-8', mode='r') as f:
            text_out = f.readlines()

        for v in verses:
            text_out.extend(v.texify())

        tmpl = sysconfig.template_file_get(self._footer)
        with open(tmpl, 'r') as f:
            text_out.extend(f.readlines())
            text_out.append(u'\n')

        return text_out

    def format(self, text_in):
        verses = []

        # force last slide to be generated
        text_in.append(u'\n')

        verse = Verse(False)
        for line in text_in:
            assert isinstance(line, unicode), 'Wrong type. Input file'\
                                              'must be unicode'
            if line.strip() == '' and not verse.empty():
                # start a new verse
                verse.finish()
                verses.append(verse)
                verse = Verse(False)
            elif line.strip() == '\\':
                verse.lines.append('')
            elif line.strip() != '':
                verse.append_line(line)

        return self.glue(verses)

    def __setup_dirs(self):
        pass

if __name__ == "__main__":
    pass
