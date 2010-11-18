#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs

from . import sysconfig
from .slide import Slide
from .verse import Verse

class SlideFormatter:
    def glue(self, verses):
        text_out = []
        tmpl = sysconfig.template_file_get(sysconfig.template_header)
        with codecs.open(tmpl, encoding='utf-8', mode='r') as f:
            text_out = f.readlines()

        chorus = None
        for v in verses:
            text_out.extend(v.texify())
            if v.chorus():
                chorus = v
            elif chorus:
                text_out.extend(chorus.texify())

        tmpl = sysconfig.template_file_get(sysconfig.template_footer)
        with open(tmpl, 'r') as f:
            text_out.extend(f.readlines())
            text_out.append('\n')

        return text_out

    def format(self, text_in):
        verses = []

        # force last slide to be generated
        text_in.append('\n')

        verse = Verse(_chorus=False, _title=True)
        for line in text_in:
            assert isinstance(line, str), 'Wrong type. Input file'\
                                              'must be unicode'
            line = line.strip()
            if line == '':
                if verse.empty():
                    continue
                # start a new verse
                verse.finish()
                verses.append(verse)
                verse = Verse(_chorus=False)
            elif line == '\\c':
                verse.chorus_set(True)
            elif line == '\\':
                verse.append_line('')
            elif line[0] == '|':
                verse.append_line_inblock(line)
            elif verse.inblock:
                verse.close_inblock(line)
            else:
                verse.append_line(line)

        return self.glue(verses)

    def __setup_dirs(self):
        pass

if __name__ == "__main__":
    pass
