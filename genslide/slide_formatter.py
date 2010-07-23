#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sysconfig

class SlideFormatter:
    header=sysconfig.template + '.header'
    footer=sysconfig.template + '.footer'

    def __init__(self, outdir, builddir):
        self.outdir = outdir
        self.builddir = builddir

    def format_file(self, file_in, file_out):
        self.__setup_dirs()

        with open(file_in, 'r') as f:
            text = f.readlines()

        text_out = self.format(text)

        with open(file_out, 'w') as f:
            f.writelines(text_out)

    def format(self, text_in):
        #FIXME
        tmpl=sysconfig.template_file_get(self.header)
        with open(tmpl, 'r') as f:
            text_out = f.readlines()

        # force last slide to be generated
        text_in.append('\n')
        aslide = []
        for line in text_in:
            if line.strip() == '' and aslide != []:
                aslide.insert(0, '\\begin{frame}\n')
                text_out.extend(aslide)
                text_out.extend(['\end{frame}', '\n\n'])
                aslide = []
            elif line.strip() != '':
                line = line.strip() + ' \\\\\n'
                aslide.append(line)

        tmpl = sysconfig.template_file_get(self.footer)
        with open(tmpl, 'r') as f:
            text_out.extend(f.readlines())
            text_out.append('\n')

        return text_out

    def __setup_dirs(self):
        pass

if __name__ == "__main__":
    slide = SlideFormatter('/tmp/', '/tmp/')
    slide.format_file('/tmp/test3', '/tmp/test_out')
