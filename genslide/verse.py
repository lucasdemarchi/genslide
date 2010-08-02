#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sysconfig
from slide import Slide
from slide import TitleSlide

class Verse:
    def __init__(self, _chorus=False, _title=False):
        self.slides = []
        self._chorus = _chorus
        self._toupper = sysconfig.option_parser.toupper
        if _title:
            self.slides.append(TitleSlide())

    def chorus_set(self, _chorus):
        self.chorus = _chorus

    def chorus(self):
        return self._chorus

    def prepare_for_line_append(self):
        if len(self.slides) == 0 or self.slides[-1].should_finish():
            self.slides.append(Slide())

    def append_line(self, line):
        line = line.strip()
        if self._toupper:
            line = line.upper()

        while line:
            self.prepare_for_line_append()
            curslide = self.slides[-1]
            line = curslide.append(line)

    def empty(self):
        return (len(self.slides) == 0 or \
                self.slides[0].empty())

    def finish(self):
        #only the last slide might not be finished yet
        self.slides[-1].finish()

    def texify(self):
        ret = []
        for s in self.slides:
            ret.extend(s.texify())
        return ret
