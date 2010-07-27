#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sysconfig

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

