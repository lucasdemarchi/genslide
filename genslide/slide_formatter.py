#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sysconfig

class Slide:
    def __init__(self, is_chorus):
        self.lines = []
        self._is_chorus = is_chorus

    def is_chorus_set(self, is_chorus):
        self._is_chorus = is_chorus
    def is_chorus(self):
        return self._is_chorus

class SlideFormatter:
    header=sysconfig.template + '.header'
    footer=sysconfig.template + '.footer'

    def __init__(self, outdir, builddir, toupper):
        self.outdir = outdir
        self.builddir = builddir
        self.toupper = toupper

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


    def format(self, text_in):
        slides = []

        # force last slide to be generated
        text_in.append('\n')

        aslide = Slide(False)
        for line in text_in:
            if line.strip() == '' and aslide.lines != []:
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

                # start a new slide
                aslide = Slide(False)
            elif line.strip() != '':
                line = line.strip() + ' \\\\\n'
                if self.toupper:
                    line = line.upper()
                aslide.lines.append(line)

        return self.glue_slides(slides)

    def __setup_dirs(self):
        pass

if __name__ == "__main__":
    slide = SlideFormatter('/tmp/', '/tmp/')
    slide.format_file('/tmp/test3', '/tmp/test_out')
