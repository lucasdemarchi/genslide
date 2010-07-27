#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

import sysconfig
from slide import Slide

class SlideFormatter:
    def __init__(self):
        self._header = sysconfig.header_template
        self._footer = sysconfig.footer_template
        self._toupper = sysconfig.option_parser.toupper

    def glue_slides(self, slides):
        text_out = []
        tmpl = sysconfig.template_file_get(self._header)
        with codecs.open(tmpl, encoding='utf-8', mode='r') as f:
            text_out = f.readlines()

        for s in slides:
            text_out.extend(s.texify())

        tmpl = sysconfig.template_file_get(self._footer)
        with open(tmpl, 'r') as f:
            text_out.extend(f.readlines())
            text_out.append(u'\n')

        return text_out

    def format(self, text_in):
        slides = []

        # force last slide to be generated
        text_in.append(u'\n')

        aslide = Slide(False)
        for line in text_in:
            assert isinstance(line, unicode), 'Wrong type. Input file'\
                                              'must be unicode'
            if line.strip() == '' and aslide.lines != []:
                # start a new slide
                aslide.finish()
            elif line.strip() == '\\':
                aslide.lines.append('')
            elif line.strip() != '':
                line = line.strip()
                if self._toupper:
                    line = line.upper()
                while line:
                    line = aslide.append(line)
                    if aslide.should_finish():
                        slides.append(aslide)
                        aslide = Slide(False)

            if aslide.should_finish():
                slides.append(aslide)
                aslide = Slide(False)

        return self.glue_slides(slides)

    def __setup_dirs(self):
        pass

if __name__ == "__main__":
    slide = SlideFormatter('/tmp/', '/tmp/')
    slide.format_file('/tmp/test3', '/tmp/test_out')
