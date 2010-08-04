#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

import sysconfig
from slide import Slide
from verse import Verse

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
            text_out.append(u'\n')

        return text_out

    def format(self, text_in):
        verses = []

        # force last slide to be generated
        text_in.append(u'\n')

        verse = Verse(_chorus=False, _title=True)
        for line in text_in:
            assert isinstance(line, unicode), 'Wrong type. Input file'\
                                              'must be unicode'
            if line.strip() == '' and not verse.empty():
                # start a new verse
                verse.finish()
                verses.append(verse)
                verse = Verse(_chorus=False)
            elif line.strip() == '\\':
                verse.append_line('')
            elif line.strip() == '\\c':
                verse.chorus_set(True)
            elif line.strip() != '':
                verse.append_line(line)

        return self.glue(verses)

    def __setup_dirs(self):
        pass

if __name__ == "__main__":
    pass
