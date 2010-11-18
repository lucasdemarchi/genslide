#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import sysconfig
import textwrap
import codecs

class Slide:
    def __init__(self):
        self.lines = []
        self._should_finish = False
        self._max_rows = sysconfig.option_parser.max_rows
        self._max_cols = sysconfig.option_parser.max_cols
        self._twrapper = None
        self._template_slide_start = sysconfig.template_slide_start
        self._template_slide_end = sysconfig.template_slide_end
        if self._max_cols:
            self._twrapper = textwrap.TextWrapper(width=self._max_cols,
                                                  break_on_hyphens=False)

    def __len__(self):
        return len(self.lines)

    def should_finish(self):
        return self._should_finish

    def finish(self):
        self._should_finish = True

    def _smart_wrap_line(self, line):
        lines = []
        nlines = int(len(line) / self._max_cols \
                 + ((len(line) % self._max_cols) > 0))

        for i in range(0, nlines):
            idx = int(len(line) / (nlines - i))
            r = line.find(' ', idx)
            l = line.rfind(' ', 0, idx)
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
        ret = ['\\begin{frame}']
        with codecs.open(
                sysconfig.template_file_get(self._template_slide_start),
                encoding='utf-8', mode='r') as f:
            ret.extend(f.readlines())

        # ensure we don't mix lines with theme
        if ret[-1][-1:] != '\n':
            ret.append('\n')

        # All the meat goes here.
        for l in self.lines:
            if (l == ''):
                ret.append('\\vskip 20pt\n')
            else:
                ret.append(''.join([l, '\\\\\n']))

        # Finalize slide with the theme and \end{frame}
        with codecs.open(
                sysconfig.template_file_get(self._template_slide_end),
                encoding='utf-8', mode='r') as f:
            ret.extend(f.readlines())

        # ensure we don't mix lines with theme
        if ret[-1][-1:] != '\n':
            ret.append('\n')
        ret.extend(['\\end{frame}', '\n', '\n'])

        return ret

    def empty(self):
        return not (len(self.lines))

    def prepend_finished(self, line):
        if not self._should_finish:
            raise Exception("prepend_finished is only allowed for a " \
                            "finished slide")
        self.lines.insert(0, line)

    def pop_finished(self):
        if not self._should_finish:
            raise Exception("append_finished is only allowed for a " \
                            "finished slide")
        return self.lines.pop()

class TitleSlide(Slide):
    def __init__(self):
        Slide.__init__(self)
        self._template_slide_start = sysconfig.template_title_start
        self._template_slide_end = sysconfig.template_title_end
