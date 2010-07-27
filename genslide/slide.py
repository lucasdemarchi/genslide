#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sysconfig
import textwrap

class Slide:
    def __init__(self, is_chorus):
        self.lines = []
        self._should_finish = False
        self._max_rows = sysconfig.option_parser.max_rows
        self._max_cols = sysconfig.option_parser.max_cols
        self._twrapper = None
        if self._max_cols:
            self._twrapper = textwrap.TextWrapper(width=self._max_cols,
                                                  break_on_hyphens=False)

    def should_finish(self):
        return self._should_finish

    def finish(self):
        self._should_finish = True

    def smart_split_line(self, line):
        if ((not self._twrapper) or len(line) <= self._max_cols):
            return [line]
        return self._twrapper.wrap(line)

    def append(self, line):
        spl = self.smart_split_line(line)
        while len(spl) and not self._should_finish:
            self.lines.append(spl.pop(0))
            if self._max_rows and len(self.lines) >= self._max_rows:
                self._should_finish = True

        if len(spl):
            return ' '.join(spl)

        return None

    def texify(self):
        ret = self.lines

        for i in xrange(0, len(ret)):
            if (ret[i] == ''):
                ret[i] = '\\vskip 20pt\n'
            else:
                ret[i] += '\\\\\n'

        #FIXME: this should be somehow in template
        #if len(slides) == 0:
        #    aslide.lines.insert(0, u'\\bfseries{\n')
        ret.insert(0, u'\\begin{center}\n')
        ret.insert(0, u'\\begin{frame}[allowframebreaks]\n')

        #FIXME: this should be somehow in template
        #if len(slides) == 0:
        #    aslide.lines.append(u'}\n')
        ret.append(u'\\end{center}\n')
        ret.extend([u'\\end{frame}', u'\n' , u'\n'])

        return ret

