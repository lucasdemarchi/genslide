#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2010 Lucas De Marchi <lucas.de.marchi@gmail.com>
"""

import sys
from URLOpener import URLOpener
from TerraHTMLParser import TerraHTMLParser
from optparse import OptionParser

def main(*args):
    usage = "%prog [options] address"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if len(args) != 1:
        raise Exception('Wrong number of args')
    addr = args[0]
    html = URLOpener.open(addr)
    TerraHTMLParser.run(html)

if __name__ == "__main__":
    sys.exit(main(*sys.argv))

