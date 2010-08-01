#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sysconfig
import textwrap
import codecs

class Slide:
    def __init__(self):
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

    def _smart_wrap_line(self, line):
        lines = []
        nlines = len(line) / self._max_cols \
                 + ((len(line) % self._max_cols) > 0)

        for i in range(0, nlines):
            idx = len(line) / (nlines - i)
            r = line.find(u' ', idx)
            l = line.rfind(u' ', 0, idx)
            if r == -1:
                break
            elif len(line[:r]) <= self._max_cols:
                idx = r
            elif len(line[:l]) <= self._max_cols:
                idx = l
            else:
                raise Exception("WARNING: unknown line width")

            lines.append(line[:idx])
            line = line[idx + 1:]
        lines.append(line)
        return lines

    def _wrap_line(self, line):
        return self._twrapper.wrap(line)

    def wrap_line(self, line):
        if ((not self._max_cols) or len(line) <= self._max_cols):
            return [line]

        if sysconfig.option_parser.smart_line:
            return self._smart_wrap_line(line)
        else:
            return self._wrap_line(line)

    def append(self, line):
        spl = self.wrap_line(line)
        while len(spl) and not self._should_finish:
            self.lines.append(spl.pop(0))
            if self._max_rows and len(self.lines) >= self._max_rows:
                self._should_finish = True

        if len(spl):
            return ' '.join(spl)

        return None

    def texify(self):
        # Start slide, putting theme just after the frame has started.
        # We don't put a newline after \being{frame}, so user can pass options
        # to the new slide.
        ret = [u'\\begin{frame}']
        with codecs.open(sysconfig.template_file_get('slide.start'),
                         encoding='utf-8', mode='r') as f:
            ret.extend(f.readlines())

        # ensure we don't mix lines with theme
        if ret[-1][-1:] != '\n':
            ret.append(u'\n')

        # All the meat goes here.
        for l in self.lines:
            if (l == ''):
                ret.append(u'\\vskip 20pt\n')
            else:
                ret.append(''.join([l, '\\\\\n']))

        # Finalize slide with the theme and \end{frame}
        with codecs.open(sysconfig.template_file_get('slide.end'),
                         encoding='utf-8', mode='r') as f:
            ret.extend(f.readlines())

        # ensure we don't mix lines with theme
        if ret[-1][-1:] != '\n':
            ret.append(u'\n')
        ret.extend([u'\\end{frame}', u'\n', u'\n'])

        return ret

    def empty(self):
        return not (len(self.lines))

class TitleSlide(Slide):
    def texify(self):
        ret = Slide.texify(self)
        ret.insert(2, u'\\bfseries{\n')
        ret.insert(-4, u'}\n')
        return ret
