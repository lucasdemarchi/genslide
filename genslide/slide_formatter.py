#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sysconfig
import textwrap

class Slide:
    def __init__(self, is_chorus):
        self.lines = []
        self._is_chorus = is_chorus
        self._should_finish = False

    def is_chorus_set(self, is_chorus):
        self._is_chorus = is_chorus
    def is_chorus(self):
        return self._is_chorus
    def should_finish(self):
        if (self._should_finish or
           (sysconfig.option_parser.max_rows and
            len(self.lines) >= sysconfig.option_parser.max_rows)):
            return True
        return False
    def should_finish_set(self, value):
        self._should_finish = value

class SlideFormatter:
    header=sysconfig.template + '.header'
    footer=sysconfig.template + '.footer'

    def __init__(self, builddir, toupper):
        self.builddir = builddir
        self.toupper = toupper
        self._twrapper = None
        self._max_cols = sysconfig.option_parser.max_cols
        if self._max_cols:
            self._twrapper = textwrap.TextWrapper(width=sysconfig.option_parser.max_cols,
                                             break_on_hyphens=False)

    def smart_split_line(self, line):
        if ((not self._twrapper) or len(line) <= self._max_cols):
            return [line + '\\\\\n']
        return [l + '\\\\\n' for l in self._twrapper.wrap(line)]

    def format_file(self, file_in, file_out):
        self.__setup_dirs()

        with open(file_in, 'r') as f:
            text = f.readlines()

        text_out = self.format(text)

        with open(file_out, 'w') as f:
            f.writelines(text_out)

    def glue_slides(self, slides):
        text_out = []
        tmpl=sysconfig.template_file_get(self.header)
        with open(tmpl, 'r') as f:
            text_out = f.readlines()

        i = 0
        chorus = -1
        for aslide in slides:
            if aslide.is_chorus():
                chorus = i

            text_out.extend(aslide.lines)
            if (chorus >= 0):
                text_out.extend(slides[chorus].lines)
            i += 1

        tmpl = sysconfig.template_file_get(self.footer)
        with open(tmpl, 'r') as f:
            text_out.extend(f.readlines())
            text_out.append('\n')

        return text_out

    def finish_slide(self, slides, aslide):
        #FIXME: this should be somehow in template
        if len(slides) == 0:
            aslide.lines.insert(0, '\\bfseries{\n')
        aslide.lines.insert(0, '\\begin{center}\n')
        aslide.lines.insert(0, '\\begin{frame}[allowframebreaks]\n')

        #FIXME: this should be somehow in template
        if len(slides) == 0:
            aslide.lines.append('}\n')
        aslide.lines.append('\\end{center}\n')
        aslide.lines.extend(['\\end{frame}', '\n' , '\n'])

        slides.append(aslide)

    def format(self, text_in):
        slides = []

        # force last slide to be generated
        text_in.append('\n')

        aslide = Slide(False)
        for line in text_in:
            if line.strip() == '' and aslide.lines != []:
                # start a new slide
                aslide.should_finish_set(True)
            elif line.strip() == '\\':
                aslide.lines.append('\\vskip 20pt\n')
            elif line.strip() != '':
                line = line.strip()
                if self.toupper:
                    line = line.upper()
                spl = self.smart_split_line(line)
                while len(spl):
                    aslide.lines.append(spl.pop(0))
                    if aslide.should_finish():
                        self.finish_slide(slides, aslide)
                        aslide = Slide(False)

            if aslide.should_finish():
                self.finish_slide(slides, aslide)
                aslide = Slide(False)

        return self.glue_slides(slides)

    def __setup_dirs(self):
        pass

if __name__ == "__main__":
    slide = SlideFormatter('/tmp/', '/tmp/')
    slide.format_file('/tmp/test3', '/tmp/test_out')
