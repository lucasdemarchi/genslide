#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sysconfig

class Slide:
    def __init__(self, is_chorus):
        self.lines = []
        self._should_finish = False

    def should_finish(self):
        if (self._should_finish or
           (sysconfig.option_parser.max_rows and
            len(self.lines) >= sysconfig.option_parser.max_rows)):
            return True
        return False

    def should_finish_set(self, value):
        self._should_finish = value

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

