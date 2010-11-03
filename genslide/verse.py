#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import sysconfig
from .slide import Slide
from .slide import TitleSlide

class Block:
    def __init__(self):
        self.startslide = None
        self.startline = None
        self.endslide = None
        self.endline = None

class Verse:
    def __init__(self, _chorus=False, _title=False):
        self.slides = []
        self.inblock = 0 # count the number of lines in a block
        self._blocks = []
        self._chorus = _chorus
        self._toupper = sysconfig.option_parser.toupper
        self._smart_verse = sysconfig.option_parser.smart_verse
        if _title:
            self.slides.append(TitleSlide())

    def __len__(self):
        return len(self.slides)

    def chorus_set(self, _chorus):
        self._chorus = _chorus

    def chorus(self):
        return self._chorus

    def prepare_for_line_append(self):
        if len(self.slides) == 0 or self.slides[-1].should_finish():
            self.slides.append(Slide())

    def append_line(self, line):
        line = line.strip()
        if self._toupper:
            line = line.upper()

        while line or line == '':
            self.prepare_for_line_append()
            curslide = self.slides[-1]
            line = curslide.append(line)

    def append_line_inblock(self, line):
        if not self.inblock:
            b = Block()
            b.startslide = len(self.slides) - 1

            # if there's no slide, we are on the first line
            # of this verse
            if b.startslide < 0:
                b.startslide = 0
                b.startline = 0
            elif self.slides[-1].should_finish():
                b.startline = 0
                b.startslide = len(self.slides)
            else:
                b.startline = len(self.slides[-1])

            self._blocks.append(b)

        self.inblock += 1
        self.append_line(line[1:].strip())

    def close_inblock(self, line):
        if not self.inblock:
            raise Exception('Block not started, how can I close it?')

        b = self._blocks[-1]
        b.endslide = len(self.slides) - 1
        b.endline = len(self.slides[-1]) - 1
        self.inblock = 0

    def empty(self):
        return (len(self.slides) == 0 or \
                self.slides[0].empty())

    def finish(self):
        #only the last slide might not be finished yet
        self.slides[-1].finish()

        #Title is not meant to be re-organized
        if self.slides and isinstance(self.slides[0], TitleSlide):
            return

        # Only the latest slide might be incomplete. By the way a Verse is
        # made, previous verses should be complete, so we verify if the
        # length of the latest slide is optimal, otherwise we start going
        # backward, popping the latest lines and prepending in the current
        # slide, until we reach a slide which has the optimal length.
        # *optimal length*: All the verses should have the same
        # length, preferring longer slides at the beginning if it's not
        # possible to divide equally among the slides of a verse
        if self._smart_verse and len(self.slides) >= 2:
            ideal_last_len = sum(map(len, self.slides))  / len(self.slides)
            for i in range(len(self.slides) - 1, 0, -1):
                while len(self.slides[i]) < ideal_last_len:
                    self.slides[i].prepend_finished(\
                            self.slides[i-1].pop_finished())

    def texify(self):
        ret = []
        for s in self.slides:
            ret.extend(s.texify())
        return ret
